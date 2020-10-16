from fastapi import APIRouter, HTTPException
import pandas as pd
# from .update import backlog_path
from ast import literal_eval
import os
import json

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

# df = pd.read_csv(locs_path)

# result = df.to_json(orient="records")
# parsed = json.loads(result.replace('\"', '"'))
# dumped = json.dumps(parsed)
# print(f"Result: {result}")
# print()
# print(f"Parsed: {parsed}")
# print()
# print(f"Dumped: {dumped}")