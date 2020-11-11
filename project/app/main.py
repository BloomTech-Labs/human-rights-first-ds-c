from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel, Field, validator
import pandas as pd
import praw
import os
import requests
from bs4 import BeautifulSoup
import re
import pickle
from newspaper import Article
import spacy
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
# Use try/except to catch a pathway error that occurs differently between local environment and deployment
try: # For deployment
    from app.api import getdata, predict#, viz  # These were not used in our product. Comment back in if/when used
except: # For local environment
    from api import getdata, predict#, viz  # These were not used in our product. Comment back in if/when used

# set up various things to be loaded outside of the function
# pathway for geolocation data set up[]
locs_path = os.path.join(os.path.dirname(
    __file__), '..', 'cities_states.csv')
locs_df = pd.read_csv(locs_path)

# Function to lowercase all text to avoid varying case issues
def lowerify(text):
    # fix up geolocation dataframe a little
    return text.lower()

# Drop 'Unnamed: 0' column and 'country' column from dataframe
locs_df = locs_df.drop(columns=['Unnamed: 0', 'country'])
# Apply lowerify function to all cities in dataframe
locs_df['city_ascii'] = locs_df['city_ascii'].apply(lowerify)
# Apply lowerify function to all states in dataframe
locs_df['admin_name'] = locs_df['admin_name'].apply(lowerify)

# Create dictionary for state/city mapping
states_map = {}
# for each state, map their respective cities
for state in list(locs_df.admin_name.unique()):
    states_map[state] = locs_df[locs_df['admin_name']
                                == state]['city_ascii'].to_list()

# police brutality indentifying nlp
model_path = os.path.join(os.path.dirname(
    __file__), '..', 'hrfc_rfmodel_v1.pkl')
model_file = open(model_path, 'rb')
pipeline = pickle.load(model_file)
model_file.close()

# local csv backlog path
# Location that any newly pulled data will be saved to
backlog_path = os.path.join(os.path.dirname(
    __file__), '..', 'backlog.csv'
)

# spacy nlp model
nlp = spacy.load('en_core_web_sm')

load_dotenv()

### Rename the following to modify the name/description/etc seen on the FastAPI documentation page 
app = FastAPI(
    title='Labs 28 Human Rights First-C DS API',
    description='Reports inicidents of police use of force in the United States.',
    version='0.6',
    docs_url='/',
)


app.include_router(predict.router)  # Not used by labs 27 but left in for future reference/use
# app.include_router(viz.router)  # Not used by labs 27 but left in for future reference/use
app.include_router(getdata.router)

# The following is run upon app startup
"""This was not thoroughly explored or used by labs 27 as our focus was on getting accurate data cleaned,
explored, and sent to web. Created by labs 25, it seems to be their method of collecting new data from Reddit,
cleaning the data and performing some feature engineering before saving it to the backlog.csv file. We ran this a
couple of times and couldn't seem to get more than 1 new instance pulled. Maybe something that can be worked on 
by future labs teams."""
@app.on_event('startup')
@repeat_every(seconds=60*60*24)  # 24 hours
def run_update() -> None:
    '''
    Update backlog database with data from reddit.
    '''

    # globalize these variables because I need to
    PRAW_CLIENT_ID = os.getenv('PRAW_CLIENT_ID')
    PRAW_CLIENT_SECRET = os.getenv('PRAW_CLIENT_SECRET')
    PRAW_USER_AGENT =  os.getenv('PRAW_USER_AGENT')

    reddit = praw.Reddit(
        client_id=PRAW_CLIENT_ID,
        client_secret=PRAW_CLIENT_SECRET,
        user_agent=PRAW_USER_AGENT
    )
    # Grab data from reddit
    data = []
    # Pull from reddit using the format: reddit.subreddit(<subreddit name>).<sort posts by keyword>(limit=<number of posts that you want to pull>)
    for submission in reddit.subreddit("news").hot(limit=100):
        data.append([submission.id, submission.title, submission.url])
    # construct a dataframe with the data
    col_names = ['id', 'title', 'url']
    df = pd.DataFrame(data, columns=col_names)

    # pull the text from each article itself using newspaper3k
    content_list = []
    date_list = []
    # go through each URL and use newspaper3k to extract data
    for id_url in df['url']:
        # use newspaper3k to extract text
        article = Article(id_url)
        article.download()
        # if the article doesn't download, the error is thrown in parse()
        try:
            article.parse()
        except:
            # add null values to show no connection
            content_list.append(None)
            date_list.append(None)
            continue
        content_list.append(article.text)
        # this will be null if newspaper3k can't find it
        date_list.append(article.publish_date)
    df['text'] = content_list
    df['date'] = date_list

    # use NLP model to filter posts
    df['is_police_brutality'] = pipeline.predict(df['title'])
    df = df[df['is_police_brutality'] == 1]
    df = df.drop(columns='is_police_brutality')

    # use spaCy to extract location tokens
    tokens_list = []
    for text in df['text']:
        doc = nlp(text.lower())
        ents = [e.text for e in doc.ents if e.label_ == 'GPE']
        tokens_list.append(ents)
    df['tokens'] = tokens_list

    # figure out which city and state the article takes place in
    city_list = []
    state_list = []
    lat_list = []
    long_list = []
    for tokens in df['tokens']:
        # set up Counter
        c = Counter(tokens)

        # count which states come back the most, if any
        state_counts = {}
        for state in states_map:
            if c[state] > 0:
                state_counts[state] = c[state]

        # get state(s) that came back the most as dict with lists
        max_count = 0
        max_state = None

        for state in state_counts:
            if state_counts[state] > max_count:
                max_count = state_counts[state]
                max_state = {state: {}}
            elif state_counts[state] == max_count:
                max_state[state] = {}

        # if no state is found
        if max_state is None:
            city_list.append(None)
            state_list.append(None)
            lat_list.append(None)
            long_list.append(None)
            continue

        max_city = None
        # get any cities in tokens based on states
        for state in max_state:  # ideally this should only run once
            city_counts = {}
            for city in states_map[state]:
                if c[city] > 0:
                    city_counts[city] = c[city]
            max_state[state] = city_counts

            # get the city/state combo that came back the most
            max_count = 0
            for city in city_counts:
                if city_counts[city] > max_count:
                    max_count = city_counts[city]
                    max_city = (city, state)

        # if no city is found
        if max_city is None:
            city_list.append(None)
            state_list.append(None)
            lat_list.append(None)
            long_list.append(None)
            continue

        # the city and state should be known now

        city_list.append(max_city[0].title())
        state_list.append(max_city[1].title())
        # now get the geolocation data
        row = locs_df[(
            (locs_df['city_ascii'] == max_city[0]) &
            (locs_df['admin_name'] == max_city[1])
        )]
        row = row.reset_index()
        if row.empty:
            pass
        else:
            lat_list.append(row['lat'][0])
            long_list.append(row['lng'][0])

    # loop ends, add cities and states onto dataframe
    df['city'] = city_list
    df['state'] = state_list
    df['lat'] = lat_list
    df['long'] = long_list

    # drop any columns with null entries for location
    df = df.dropna()
    df = df.reset_index()
    df = df.drop(columns='index')

    # cleanup to match 846 api
    def listify(text):
        return [text]
    df['src'] = df['url'].apply(listify)
    df['desc'] = df['text']
    df = df.drop(columns=['tokens', 'text'])
    df = df[[
        'id', 'state', 'city',
        'date', 'title', 'desc',
        'src', 'lat', 'long'
    ]]

    # save the file to a local csv
    df.to_csv(backlog_path, index=False, )
    return HTTPException(
        200,
        "Backlog Updated at %s with %s entries" % (datetime.now(), df.shape[0])
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
