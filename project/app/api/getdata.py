from fastapi import APIRouter, HTTPException
import pandas as pd
from .update import backlog_path
from ast import literal_eval
import os

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

    df = df.drop(columns="Unnamed: 0").reset_index()

    """
    Convert data to useable json format
    ### Response
    dateframe: JSON String
    """

    return df.to_json(orient="records")
