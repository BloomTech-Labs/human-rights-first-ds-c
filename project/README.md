# Project

This directory contains all files directly important to the final product including important csv files, pickled predictive models, and API directory and files.

## Contents

*• latest_incidents.csv* —— csv file containing dataset created in the "Data_Final.ipynb" notebook found in the [labs27_notebooks directory](https://github.com/Lambda-School-Labs/Labs27-C-HRF-DS/tree/main/labs27_notebooks) created by the labs 27 team.

*• cities_states.csv* —— csv file containing United States city names, state names, lattitude code, and longitude code. Used to create lat/lon geocodes for the backlog.csv, all_sources.csv, and all_sources_geoed.csv files.

*• backlog.csv* —— csv file containing new data pulled from Reddit, cleaned, and feature engineered to include city, state, and geocode. Created by the labs 25 team. Not used by the labs 27 team.

*• all_sources.csv* —— csv file containing id, title, city, state, lat, long, date, desc, src features and data from the latest_incidents.csv file after some cleaning and minor changes by the labs 27 team.

*• all_sources_geoed.csv* —— csv file containing more cleaned up data from the all_sources.csv file. This is the final dataset created by the labs 27 team and sent to web. 

*• Dockerfile* —— File that contains the instructions needed to automatically build images for Docker.

*• hrfc_rfmodel_v1.pkl* —— File containing the pickled predictive model created in the 'Model_RF_V1.ipnb' in the [labs27_notebooks directory](https://github.com/Lambda-School-Labs/Labs27-C-HRF-DS/tree/main/labs27_notebooks) created by labs 27 team.

*• model.pkl* —— File containing the pickled predictive model created by the labs 25 team.

*• requirements.txt* —— .txt file containing the installments required for the DS app to run correctly.

*• set_data_lat_long.py* —— File used to locally clean up some of the data in the "latest_injcidents.csv" and "all_sources.csv" files.

*• app* —— Directory containing all of the directories and files directly used in creating the DS app and API. 
