import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    id: str = Field(..., example="ID") 
    city: str = Field(..., example="Broken Arrow")
    state: str = Field(..., example="Oklahoma")
    lat: float = Field(..., example=36.0365)
    long: float = Field(..., example=-95.7809) 
    title: str = Field(..., example='"Police brutality rampant in Broken Arrow!"')
    desc: str = Field(..., example='"Super crazy police brutality incidents happening in Broken Arrow, Oklahoma"')
    src: str = Field(..., example='"www.twitter.com"')
    date: str = Field(..., example= "2020-05-30")
    
    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

@router.post('/predict')
async def predict(item: Item):
    """
    Make random baseline predictions for classification problem 🔮

    ### Request Body
    - id: string
    - city: string
    - state: string
    - lat: float
    - long: float
    - title: string
    - desc: string
    - src: string
    - date: string

    ### Response
    - `prediction`: boolean, at random
    - `predict_proba`: float between 0.5 and 1.0, 
    representing the predicted class's probability

    """

    X_new = item.to_df()
    log.info(X_new)
    y_pred = random.choice([True, False])  # Used for testing purposes
    y_pred_proba = random.random() / 2 + 0.5  # Used for testing purposes
    return {
        'prediction': y_pred,
        'probability': y_pred_proba
    }
