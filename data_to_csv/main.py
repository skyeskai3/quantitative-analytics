import pymysql
import csv
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import logging
import sys
import time
import json
import argparse

class DatabaseConnector:
    def __init__(self, host, user, password, database, port):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }
        self.connection = None

    def connect_to_database(self):
        try:
            self.connection = pymysql.connect(**self.db_config)
            logging.debug("Connected to database")
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def close_connection(self):
        if self.connection and self.connection.open:
            self.connection.close()
            logging.debug("Closed database connection")
        else:
            print("Connection is already closed or not established")


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Creates a complete list of trading signals for a specified ticker')

    parser.add_argument('--connection', default='live.json', help='Specify which JSON configuration file to pass to connect to a SQL database. Default is local.json')

    args = parser.parse_args()
    print("Connection is ", args.connection)
    with open(args.connection, 'r') as file:
        config_data = json.load(file)
        db_config = config_data.get('db', {})

    db_connector = DatabaseConnector(**db_config)

    try:
        db_connector.connect_to_database()

        parser.add_argument('--ticker', default='SPY', help='Specify the ticker symbol that you want signals for. Default is SPY')

        args = parser.parse_args()
        global ticker
        ticker = args.ticker
        print(f"Ticker: {ticker}")

        '''
        if len(sys.argv) > 1:
            global ticker
            ticker = sys.argv[1]
            print(f"Ticker: {ticker}")
        else:
            ticker = 'SPY'
            print("No ticker provided, using default: SPY")
        '''

        filled_df = perform_query(db_connector)
        print("Here is the filled dataframe\n", filled_df.head(10))

        transformed_df = transform_candles(filled_df)
        print("Here is the transformed dataframe\n", transformed_df.head(10))
        print("The dataframe has length of ", len(transformed_df))
        non_zero_order_rows = len(transformed_df[transformed_df['orderx'] != 0])
        print(f"There are {non_zero_order_rows} non-zero order rows in the transformed dataframe")
        file_path = '/app/SPY_v2_hourly.csv'
        create_csv(file_path, transformed_df)

    finally:
        db_connector.close_connection()


def perform_query(db_connector):
    try:
        db_connector.connect_to_database()

        connection = db_connector.connection
        cursor = connection.cursor()

        query = '''SELECT * FROM table '''.format(ticker) # obfuscated for proprietary reasons
        
        cursor.execute(query)

        results = cursor.fetchall()
        # columns obfuscated for proprietary reasons
        columns = ['val1','val2','val3','val4','val5','val6','val7','val8','val9','val10','val11','val12','val13','val14','val15','val16','val17','val18','val19','val20',
                   'val21','val22','val23','val24','val25','val26','val27','val28','val29','val30']
        df = pd.DataFrame(results, columns=columns)
        
        df['orderx'] = df['orderx'].replace({'Buy': 1, 'Sell': -1})
        df['utctime'] = pd.to_datetime(df['utctime'])
        df['utctime'] = df['utctime'].dt.strftime('%Y-%m-%d %H:00:00')
        df['utctime'] = pd.to_datetime(df['utctime'])

        date_range = pd.date_range(start=df['utctime'].min(), end=df['utctime'].max(), freq='H')
        date_range_df = pd.DataFrame(index=date_range)
        date_range_df['utctime'] = date_range_df.index
        date_range_df.reset_index(drop=True, inplace=True)

        full_df = pd.merge(date_range_df, df, on='utctime', how='left')
        full_df.fillna(0, inplace=True)

    except pymysql.Error as err:
        print(f"Error: {err}")

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            db_connector.close_connection()

    return full_df

def transform_candles(df):
# redacted for proprietary reasons
    return df

def create_csv(file_path, dataframe):
    # headers obfuscated for proprietary reasons
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # obfuscated for proprietary reasons
           
    writer.writerow(['']) # obfuscated for proprietary reasons


if __name__ == "__main__":
    start=time.time()
    main()
    end = time.time()
    print(f"Script took {end-start} seconds")
