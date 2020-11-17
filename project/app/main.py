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
import json
import datetime
import ast
from spacy.tokenizer import Tokenizer
#Database Imports for automatic new data
import psycopg2
import psycopg2.extras

# Use try/except to catch a pathway error that occurs differently between local environment and deployment
try: # For deployment
    from app.api import getdata, predict#, viz  # These were not used in our product. Comment back in if/when used
except: # For local environment
    from api import getdata, predict#, viz  # These were not used in our product. Comment back in if/when used


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
"""The bottom code below runs on app startup and every 24 hours to check for new data.
   Recommended to separate into more modular functions. Needs to do more testing to see if 
   it is running every 24 hours, but test shows it is working. for Lab29 to do. """
@app.on_event('startup')
@repeat_every(seconds=60*60*24)  # 24 hours Runs Function bellow every 24 hours. 
async def run_update() -> None:
    # DB Connection
    DB_CONN = os.environ.get('DBURLS') # Gets URL from Enviroment variable
    pg_conn = psycopg2.connect(DB_CONN) # Connects to DB
    pg_curs = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    Q = """SELECT * FROM police_force;"""
    pg_curs.execute(Q)
    results = pg_curs.fetchall()
    pg_curs.close()

    #Read API INFO
    API_CONN = os.environ.get('APIURL') #Gets API URL from environment 

    r = requests.get(API_CONN)
    data_info = r.json()
    # count the number of new items on the API. 
    def check_new_items(db_info,api_info):
        new_items = []
        counter = 0
        for item in api_info['data']:
            if not any(d['case_id'] == item['id'] for d in db_info):
                new_items.append(item)
                counter += 1
        return counter,new_items
    #Code on the bottom is to pre process /classify data using NLP 
        
    stop_words = ["celebrity", "child", "ederly","lgbtq+","homeless", "journalist",
                  "non-protest","person-with-disability", "medic", "politician",
                  "pregnant", "property-desctruction", " ","bystander","protester",
                  "legal-observer", "hide-badge", 'body-cam', "conceal",'elderly'
                  ]
    stop = nlp.Defaults.stop_words.union(stop_words)

    # NOTE: ALL CATEGORIES STRICTLY FOLLOW THE NATIONAL INJUSTICE OF JUSTICE USE-OF-CONTINUM DEFINITIONS
    # # for more information, visit https://nij.ojp.gov/topics/articles/use-force-continuum

    VERBALIZATION = ['threaten', 'incitement']
    EMPTY_HAND_SOFT = ['arrest', 'grab', 'zip-tie', ]
    EMPTY_HAND_HARD = ['shove', 'push', 'strike', 'tackle', 'beat', 'knee', 'punch',
                   'throw', 'knee-on-neck', 'kick', 'choke', 'dog', 'headlock']
    LESS_LETHAL_METHODS = ['less-lethal', 'tear-gas', 'pepper-spray', 'baton',
                       'projectile', 'stun-grenade', 'pepper-ball',
                       'tear-gas-canister', 'explosive', 'mace', 'lrad',
                       'bean-bag', 'gas', 'foam-bullets', 'taser', 'tase',
                       'wooden-bullet', 'rubber-bullet', 'marking-rounds',
                       'paintball']
    LETHAL_FORCE = ['shoot', 'throw', 'gun', 'death', 'live-round', ]
    UNCATEGORIZED = ['property-destruction', 'abuse-of-power', 'bike',
                 'inhumane-treatment', 'shield', 'vehicle', 'drive', 'horse',
                 'racial-profiling', 'spray', 'sexual-assault', ]

    # UNCATEGORIZED are Potential Stop Words. Need to talk to team.
    # FUNCTION STARTS HERE, OPTIMIZATION WILL BE NEEDED

    def preprocessNewData(new_data_json):
        """
        Preprocessing function recycling preprocessing functions to mimic the
        output of the initial dataframe.
        """
        # Temp, create a dataframe for easier view. **Consider converting function
        # # for use with json/dict.
        df = pd.DataFrame(data=new_data_json)
        # Rename columns/ Drop irrelevant columns
        df = df.rename(columns={'name': 'title'}).drop(labels=['edit_at', 'date_text'], axis=1)
        # Reorder column headers
        df = df[['date', 'links', 'id', 'city', 'state', 'geolocation', 'title', 'tags', 'description']]
        # Update the "date" column to timestamps and sort
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['date'] = df.date.astype(object).where(df.date.notnull(), None)
        df = df.sort_values(by='date')
        # Reset index
        df.reset_index(inplace=True)
        # Replace the Nan values with the string "None" in the description column
        # May need to create conditions for variations with the new data (consideration)
        df['description'] = df['description'].replace({np.NaN: "None"})
        # Replace the Nan values with the string "None" in the geolocation column
        # Missing geolocations are mapped as empty strings
        df['geolocation'] = df['geolocation'].replace({"": np.NaN}).replace({np.NaN: "None"})
        # Write function to create hyperlinks for the 'links' columns
        def cleanlinks(url_col):
            """ Function to convert links from json to a str. Creates hyperlink"""
            links_out = []
            for link in url_col:
                links_out.append(link['url'])
            return links_out
        # Apply function to the dataframe 'links' column
        df['links'] = df['links'].apply(cleanlinks)
        # Create a latitude (lat) and longitude (lon) column.
        # Create function to create lat and long from geolocation column
        def splitGeolocation(item):
            """
            Creates two new columns (lat and lon) by separating the dictionaries of
            geolocations into latitiude and longitude.
            :col: indexed slice of a column consisting of dictionaries/strings with
            latitiude and longitude integers
            :return: latitude column
            :return: longitude column
            """
            lat = []
            lon = []
            if isinstance(item, str) and item != 'None':
                item = item.split(',')
                lat.append(float(item[0]))
                lon.append(float(item[1]))
            elif type(item) == dict:
                lat.append(float(item['lat']))
                lon.append(float(item['long']))
            else:
                lat.append(None)  # Null values
                lon.append(None)  # Null values
            return lat, lon
        # Call Function
        df['lat'] = [splitGeolocation(item)[0][0] for item in df['geolocation']]
        df['long'] = [splitGeolocation(item)[1][0] for item in df['geolocation']]
        # Drop the geolocation columnsss
        df = df.drop(labels=['geolocation', 'index'], axis=1)
        def remove_stops(_list_):
            keywords = []
            for keyword in _list_:
                phrase = []
                words = keyword.split()
                for word in words:
                    if word in stop:
                        pass
                    else:
                        phrase.append(word)
                phrase = ' '.join(phrase)
                if len(phrase) > 0:
                    keywords.append(phrase)
            return keywords
        df['tags'] = df['tags'].apply(remove_stops)
        # Need dummy columns. Create a cleaner function to handle this problem. DJ.
        df['verbalization'], df['empty_hand_soft'], df['empty_hand_hard'], df['less_lethal_methods'], df['lethal_force'], df['uncategorized'] = df['id'], df['id'], df['id'], df['id'], df['id'], df['id']
        def Searchfortarget(list, targetl):
            for target in targetl:
                res = list.index(target) if target in list else -1  # finds index of target
                if res == -1:
                    return 0  # if target is not in list returns -1
                else:
                    return 1  # if the target exist it returns
        def UseofForceContinuumtest(col):
            for i, row in enumerate(col):
                df['verbalization'].iloc[i], df['empty_hand_soft'].iloc[i], df['empty_hand_hard'].iloc[i], df['less_lethal_methods'].iloc[i], df['lethal_force'].iloc[i], df['uncategorized'].iloc[i] = Searchfortarget(VERBALIZATION, row), Searchfortarget(EMPTY_HAND_SOFT, row), Searchfortarget(EMPTY_HAND_HARD, row), Searchfortarget(LESS_LETHAL_METHODS, row), Searchfortarget(LETHAL_FORCE, row), Searchfortarget(UNCATEGORIZED, row)
                # Apply function to the cleaned_tags columns
            UseofForceContinuumtest(df['tags'])
        return df.to_dict(orient='records')

    #Updates to database
    counter_api,new_items = check_new_items(results,data_info) #Checks for new items
    # if new_items array is not empty. add data to database
    if new_items:
        newdata = preprocessNewData(new_items)
        pg_conn = psycopg2.connect(DB_CONN)
        pg_curs = pg_conn.cursor()
        for item in newdata:
            current_dt = datetime.datetime.today()
            pg_curs.execute("""INSERT INTO police_force (dates,added_on, links, case_id, city, state,lat,long, title, description, tags,verbalization,empty_Hand_soft, empty_hand_hard, less_lethal_methods, lethal_force, uncategorized) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",(item['date'],current_dt,str(item['links']),str(item['id']),str(item['city']),str(item['state']),item['lat'],item['long'],str(item['title']),str(item['description']),str(item['tags']),item['verbalization'],item['empty_hand_soft'],item['empty_hand_hard'],item['less_lethal_methods'],item['lethal_force'],item['uncategorized']))
        pg_conn.commit()
        pg_curs.close()
        pg_conn.close()




app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
