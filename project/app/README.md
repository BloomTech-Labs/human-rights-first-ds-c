# app

This directory contains all directories and files used in the creation of the DS app and API through the use of FastAPI and AWS Elastic Beanstalk.

## Contents

*main.py* —— File containing the app and its instance call. Also includes an on-startup and 24-hour call to pull data from reddit, clean the data, feature engineer the geocodes, and save the data to the "backlog.csv" file. Created by labs 25 and modified by labs 27, with labs 27 not using the latter.

*__init__.py* —— File that initializes the app and ties in all the modules found within the app directory.

*tests* —— Directory created by labs 25 and used to test API endpoints.

*api* —— Directory that stores all files and directories used in the creation of the API as well as the API's connection to the main DS app.

*.elasticbeanstalk* —— File used to save Elastic Beanstalk configurations