#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import os,sys,json
import pandas as pd
import mysql.connector
import logging as ilog
import yfinance as _yf
from dateutil import tz
import quantstats as qs
from loguru import logger
import matplotlib.pyplot as plt
from http.server import BaseHTTPRequestHandler, HTTPServer
import redis

ilog.getLogger('matplotlib.font_manager').setLevel(ilog.ERROR)

import warnings
warnings.filterwarnings("ignore")

logger.remove()
logger.add(sys.stdout,
        level=os.getenv("LOG_LEVEL"),
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

VERSION = '0.1.0'

def DB():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        database=os.getenv("DB_DATB"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

def RedisInsert(id:str, content:str, active:str):
    if active=='active':
        id = "tearsheets:" + id + ":active:" +active
    else:
        id = "tearsheets:" + id
    if content == None or content == '':
        logger.error("Empty content passed")
    pool = redis.ConnectionPool(host=os.getenv("RDS_HOST"), password=os.getenv("RDS_PASS"), port=os.getenv("RDS_PORT"), db=os.getenv("RDS_DATB"))
    r = redis.Redis(connection_pool=pool)    
    #verify r is open and connected
    if r.ping() == False:
        logger.error("Unable to connect to redis database")
        return
    r.set(id,content)
    get = r.get(id)
    if get == None:
        logger.error("Content not properly stored in redis")
    #verify response is not empty (response!="b" or return NoneType)
    #r.close close the redis connection

# find a way to process AUM if needed
# do something with MakeTearsheet(csvfile)
# remove csvfile
# return tearsheet.file_extension
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/test":
            self.wfile.write(bytes("test", "utf-8"))
            return
        if self.path == "/version":
            self.wfile.write(bytes(VERSION, "utf-8"))
            return
        if self.path == "/output":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open('output.html', 'rb') as file:
                self.wfile.write(file.read())
        if self.path == "/":
            self.wfile.write(bytes("Yeshua is Lord", "utf-8"))

    def do_PUT(self):
        aum = 1000
        filename: str = os.path.basename(self.path)
        if os.path.exists(filename):
            os.remove(filename)
        local_aum = self.headers['aum']
        if local_aum != None:
            aum = local_aum
        id = self.headers['id']
        active = self.headers['active']
        if id == None:
            self.send_response(400); self.end_headers()
            self.wfile.write(bytes("required header 'id' missing.", "utf-8"))
            return
        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created'); self.end_headers()
        mktr = MakeTearsheet(filename,id,aum,active=active) 
        logger.debug("AUM be "+str(aum)+" id be "+str(id)+" actstat be "+str(active))
        if mktr != None:
            self.wfile.write(bytes(mktr, "utf-8"))
            return
        with open('output.html', 'rb') as file:
            f=file.read()
            self.wfile.write(f)
            RedisInsert(id,f,active)

    def log_request(self, format, *args):
        logger.debug("{} {} ".format(self.path, self.address_string()))
        return


def StartWeb():
    webServer = HTTPServer(("0.0.0.0", 3778), MyServer)
    logger.info("Server started http://%s:%s" % ("0.0.0.0", "3778"))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logger.info("Server stopped.")


def MakeTearsheet(csvfile, id, aum=1000, timeframe=None, active=None):
    logger.debug("AUM is "+str(aum)+" for id "+str(id)+" actstat is "+str(active))
    try:
        if timeframe == None:
            timeframe = csvfile
        df = pd.read_csv(csvfile)
        if df.empty:
            logger.error('DataFrame is empty!')
            return 'DataFrame is empty!'
        df['min'] = pd.to_datetime(df['min'], format='%a %m/%d/%y %H:%M %p')

        strat = df[['min', 'profit']]
        strat.columns = ['Date', 'profit']
        strat = strat.set_index('Date')

        strat["Close"] = 0.0
        strat["Close"].iloc[0] = float(aum) + strat["profit"].iloc[0]

        logger.debug("id: "+str(id)+" df")
        logger.debug(df)

        for x in range(1, len(strat)):
            strat["Close"].iloc[x] = strat["Close"].iloc[
                x - 1] + strat["profit"].iloc[x]

        logger.debug("id: "+str(id)+" strat")
        logger.debug(strat)
        strat.drop('profit', axis=1, inplace=True)
        end_bal=strat["Close"].iloc[-1]

        qs.extend_pandas()

        our_pc = strat["Close"].pct_change() #TODO check if div by zero
        our_pc = our_pc.fillna(0)

        # Update risk free rate based on https://ycharts.com/indicators/3_month_t_bill August 21,2023 value
        rfr = 0.053

        # Periods if data is passed in daily
        global period
        period = 252
        hourly_period = 2016 # based on 8 hours in a day and 252 trading days in a year
        daily_period = 252 # based on number of tradable days in a year
        monthly_period = 12 # based on number of months in a year
        #yearly_period = 1 # 1 year

        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        interval = "1m"
        if timeframe == "hour":
            interval = "1h"
            period = hourly_period
        elif timeframe == "day":
            interval = "1d"
            period = daily_period
        elif timeframe == "week":
            interval = "1wk"
        elif timeframe == "month":
            interval = "1mo"
            period = monthly_period

        p = {"period": "max", "interval": interval, "start": our_pc.index[0], "end": our_pc.index[-1]}
        logger.debug(id,p)
        aaa = _yf.Ticker("SPY").history(**p)['Close'].pct_change() #TODO check if div by zero
        aaa.index = aaa.index.astype('datetime64[ns]')
        aaa = aaa.fillna(0)
        our_pc.index = our_pc.index.to_series().dt.normalize()
        aaa.index = aaa.index.to_series().dt.normalize()
        our_pc = our_pc.groupby(our_pc.index).mean()
        aaa = aaa.groupby(aaa.index).mean()
        our_pc.to_csv('our_returns.csv', header=True)
        aaa.to_csv('benchmark_returns.csv', header=True)

        filename = 'output.html'  # come up with a way to create proper names for this
        qs.reports.html(our_pc,#our_pc.squeeze(),
                        aaa,
                        output=filename,
                        rf=rfr,
                        periods_per_year=period,
                        download_filename=filename)
        nfo = {}
        nfo['sharpe'] = qs.stats.sharpe(our_pc,rf=rfr,periods=period, annualize=True)
        nfo['avg_loss'] = qs.stats.avg_loss(our_pc)
        nfo['avg_return'] = qs.stats.avg_return(our_pc)
        nfo['avg_win'] = qs.stats.avg_win(our_pc)
        nfo['consecutive_losses'] = qs.stats.consecutive_losses(our_pc).tolist()
        nfo['consecutive_wins'] = qs.stats.consecutive_wins(our_pc).tolist()
        nfo['win_rate'] = qs.stats.win_rate(our_pc)
        nfo['win_loss_ratio'] = qs.stats.win_loss_ratio(our_pc)
        nfo['best'] = qs.stats.best(our_pc)
        nfo['worst'] = qs.stats.worst(our_pc)
        nfo['max_drawdown'] = qs.stats.max_drawdown(our_pc).tolist()
        nfo['monthly_returns'] = {} # json.loads(qs.stats.monthly_returns(our_pc).to_json())
        nfo['volatility'] = qs.stats.volatility(our_pc,periods=period,annualize=True).tolist()
        logger.debug(json.dumps(nfo))
        cumulative_return = qs.stats.comp(our_pc)*100 #TODO check if div by zero
        db = DB()
        c = db.cursor()

        if active!='active':
            sql = "UPDATE table1 SET end_bal=%s, cumulative_return=%s, sharpe=%s, avg_loss=%s, avg_return=%s, avg_win=%s, consecutive_losses=%s, consecutive_wins=%s, win_rate=%s, win_loss_ratio=%s, best=%s, worst=%s, max_drawdown=%s, volatility=%s WHERE id=%s"
            val = (end_bal, cumulative_return, nfo['sharpe'], nfo['avg_loss'], nfo['avg_return'], nfo['avg_win'], 
                nfo['consecutive_losses'], nfo['consecutive_wins'], nfo['win_rate'], 
                nfo['win_loss_ratio'], nfo['best'], nfo['worst'], nfo['max_drawdown'], 
                nfo['volatility'], int(id))
            c.execute(sql, val)
        elif active=='active':
            sql = "UPDATE table2 SET cumulative_return=%s, sharpe=%s, avg_loss=%s, avg_return=%s, avg_win=%s, consecutive_losses=%s, consecutive_wins=%s, win_rate=%s, win_loss_ratio=%s, best=%s, worst=%s, max_drawdown=%s, volatility=%s WHERE id=%s"
            val = (cumulative_return, nfo['sharpe'], nfo['avg_loss'], nfo['avg_return'], nfo['avg_win'], 
                nfo['consecutive_losses'], nfo['consecutive_wins'], nfo['win_rate'], 
                nfo['win_loss_ratio'], nfo['best'], nfo['worst'], nfo['max_drawdown'], 
                nfo['volatility'], int(id))
            c.execute(sql, val)

        db.commit()
        c.close()
        db.close()

        return None

    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return str(e)

if __name__ == "__main__":
    StartWeb()
