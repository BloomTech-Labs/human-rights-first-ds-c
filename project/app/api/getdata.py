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
import datetime

router = APIRouter()

@router.get('/getdata')
async def getdata(date_added: str = None):
    print(date_added)
    '''
    Get jsonified dataset from Database
    '''
    DB_CONN = os.environ.get('DBURLS')
    pg_conn = psycopg2.connect(DB_CONN)
    pg_curs = pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if date_added == None:
        Q = """SELECT * FROM police_force;"""
    else:
        Q = f"""SELECT * FROM police_force WHERE added_on >= '{date_added}';"""
    print(date_added)
    print(Q)
    pg_curs.execute(Q)
    results = pg_curs.fetchall()
    pg_curs.close()
    pg_conn.close()

    """
    Convert data to useable json format
    ### Response
    dateframe: JSON object
    """
    #parsed = []
    for item in results:
        item['links'] = ast.literal_eval(item['links'])
        item['tags'] = ast.literal_eval(item['tags'])
        #parsed.append(item)
    return results
