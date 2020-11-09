from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
# from .update import backlog_path  # Use this when able to get the backlog.csv filled correctly
from ast import literal_eval
import os
import json
import ast
import psycopg2
import psycopg2.extras

router = APIRouter()

@router.get('/getdata')
async def getdata():
    '''
    Get jsonified dataset from Database
    '''

    # Path to dataset used in our endpoint
    # locs_path = os.path.join(os.path.dirname(
    #     __file__), '..', '..', 'all_sources_geoed.csv')

    router = APIRouter()
    #DB_URL = os.getenv('DBURL')
    #print(DB_URL)

    # df = pd.read_csv(locs_path)
    DB_CONN = os.environ['DBURLS']
    pg_conn = psycopg2.connect(DB_CONN)
    pg_curs = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    Q = """SELECT * FROM police_force;"""
    pg_curs.execute(Q)
    results = json.dumps(pg_curs.fetchall(),indent=2,default=str)
    pg_curs.close()
    pg_conn.close()
    # print(results)
    # Fix issue where "Unnamed: 0" created when reading in the dataframe
    # df = df.drop(columns="Unnamed: 0")

    # Removes the string type output from columns src and tags, leaving them as arrays for easier use by backend
    # for i in range(len(df)):
    #     df['src'][i] = ast.literal_eval(df['src'][i])
    #     df['tags'][i] = ast.literal_eval(df['tags'][i])


    """
    Convert data to useable json format
    ### Response
    dateframe: JSON object
    """
    # Initial conversion to json - use records to jsonify by instances (rows)
    # result = df.to_json(orient="records")
    # Parse the jsonified data removing instances of '\"' making it difficult for backend to collect the data
    parsed = json.loads(results.replace('\"', '"'))
    return parsed
