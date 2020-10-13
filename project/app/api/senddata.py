from fastapi import APIRouter, FastAPI
import os
import pandas as pd
locs_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'all_sources_geoed.csv')

router = APIRouter()

df = pd.read_csv(locs_path)

@router.post("/senddata/")
async def send_data():
    """

    Convert data to useable json format 

    ### Response
    dataframe: JSON String
    """

    return df.to_json(orient="split")

