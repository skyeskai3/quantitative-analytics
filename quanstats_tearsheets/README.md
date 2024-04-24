# About
This project was created to produce tearsheets by means of utilizing Quantstats. The tearsheets were fundamental in creating a complete view of critical metrics surrounding each of our trading accounts. The metrics provided by the output tearsheets influenced the trading strategies that were being utilized on each account. Many of the csv files have been obfuscated for proprietary reasons. Additionally, the commands below may not perform due to the alterations put in place to protect proprietary data. 

# Required dependencies for development
 `sudo apt install -y docker.io make curl`
# Getting started with docker
- run `make build` to build the image
- run `make run` to launch a new container

# Installing Docker Compose
`sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose`

`sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`


# Run Locally
`docker-compose up -d`

## Set up and view the results of the tearsheet

Execute bash on the tearsheet container

`docker exec -it tearsheets-db-1 bash`


### Check mysql to ensure the table runstat was created 

`mysql -u root -p tearsheets`

`SHOW tables;`

Insert into table 'runstat' an id=1 (or whatever id you are planning on passing as your header in your curl)
* NOTE: Table 'activestat' can also be viewed and tested in this environment following similar commands

`INSERT INTO table1 (id,begin_bal,url1) VALUES (1,1000,'test/html2.test');`


After running the test.csv via the curl check runstat for updated metrics

`SELECT * FROM table1 WHERE id=1;`


### Check redis for keys and content

`docker exec -it tearsheets-redis-1 redis-cli`

Show all keys 

`KEYS *`

Grab the content from a key 

`GET <keyname>`

## Running the test.csv
Go to the directory where you have brought in the tearsheet repository 
Make sure when you are passing a test json that you specify the correct time frame

Available Time Frames:
- minute 
  - default
- hour
- day
- week
- month
  


With aum and id
Default aum is $1000


`curl -X PUT -H 'aum:100000' -H 'id:1' -H 'active:None' --data-binary @test.csv  http://0.0.0.0:3778/day`

# Run Production
Make sure the that you are passing json as the datatype and that you are passing the appropriate time frame for the endpoint. Make sure you are using the `PUT` request.
