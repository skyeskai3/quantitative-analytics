# Data Integration CSV

The following is designed to create a CSV file containing a collection of proprietary trade signals. The result of this project was to produce a csv file that included transformed values of proprietary trade signals, along with ways to test. The data was transformed according to the specs laid out by the receiving client. Some of the files have been obfuscated for proprietary reasons. 

# AI Integration Test
* Note the following commands may not run as intended due to obfuscation in associated files

After cloning the repository, run the following commands:

```
make build
```
This will build the containers
```
make run
```
This will create the necessary containers for the mysql instance and the python environment
```
make sql
```
This will allow the user to login to the sql instance using password 'test'
```
SHOW tables;
```
```
SELECT COUNT(*) FROM tableX;
```
These are helpful base SQLs to ensure the data was inserted into the database upon building the containers for the test environment

To pass a specific ticker to be exported run the following 
```
docker-compose run python_app --ticker SPY --connection live.json
```


