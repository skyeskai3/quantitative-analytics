FROM python:3.10-buster
WORKDIR /usr/app
# RUN pip install pandas yfinance quantstats loguru mysql-connector-python redis ipython
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD [ "python", "main.py" ]
