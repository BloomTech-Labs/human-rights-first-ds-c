from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
# from .update import backlog_path
from ast import literal_eval
import os
import json
import ast

router = APIRouter()


@router.get('/getdata')
async def getdata():
    '''
    Get data from all_sources_geoed database.
    '''

    locs_path = os.path.join(os.path.dirname(
        __file__), '..', '..', 'all_sources_geoed.csv')

    router = APIRouter()

    df = pd.read_csv(locs_path)
    df = df.drop(columns="Unnamed: 0")
    for i in range(len(df)):
        df['src'][i] = ast.literal_eval(df['src'][i])
        df['tags'][i] = ast.literal_eval(df['tags'][i])

    df = df.sort_values(by="date", ascending=False)
    df = df.head(100)

    """
    Convert data to useable json format
    ### Response
    dateframe: JSON String
    """
    result = df.to_json(orient="records")
    parsed = json.loads(result.replace('\"', '"'))#.replace('"\\', '"'))  
    # return json.dumps(parsed)
    return parsed

# locs_path = os.path.join(os.path.dirname(
#         __file__), '..', '..', 'all_sources_geoed.csv')

# print(df["src"])
# result = df.to_json(orient="records")
# parsed = json.loads(result.replace('\"', '"'))

# print(f"Parsed: {parsed}")