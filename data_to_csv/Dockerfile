FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

EXPOSE 80

ENTRYPOINT ["sh", "-c", "wait-for-it -t 60 mysql:3306 && python3 main.py"]
#CMD ["sh", "-c", "wait-for-it -t 60 mysql:3306 && python3 main.py && tail -f /dev/null"]
