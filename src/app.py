import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.predictor import CryptoPricePredictor

pd.set_option("display.max_rows", 500)


class RequestBody(BaseModel):
    lookback_hrs: int = Field(default=1, gt=0)
    frequency_mins: int = Field(default=1, gt=0)
    ccy_pair: str = Field(default="BTCUSD", max_length=6, min_length=6)


app = FastAPI()


# Custom endpoint for programmatic purposes with customizable params
@app.post('/predictions/custom',
          summary="BTC/USD price prediction endpoint with custom parameters",
          tags=["BTC Price Prediction"])
def predict_btcusd_custom(req: RequestBody):
    model = CryptoPricePredictor(
        ccy_pair="BTCUSD",
        lookback_hrs=req.lookback_hrs,
        frequency_mins=req.frequency_mins
    )
    model.get_historical_quotes()

    response = {
        'requested_at': model.historical_quotes.requested_at[0],
        'ccy_pair': model.ccy_pair,
        'lookback_hrs': model.lookback_hrs,
        'frequency_mins': model.frequency_mins,
        'prediction': model.predict()
    }

    with open(file="./logs/responses.txt", mode='a') as f:
        f.write(str(response) + '\n')

    return response


# Default endpoint for visulisation purposes with fixed params
@app.get('/predictions/default',
         summary="BTC/USD price prediction endpoint with default parameters",
         tags=["BTC Price Prediction"],
         response_class=HTMLResponse)
def predict_btcusd_default():
    model = CryptoPricePredictor(ccy_pair="BTCUSD", lookback_hrs=1, frequency_mins=1)
    model.get_historical_quotes()

    response = {
        'requested_at': model.historical_quotes.requested_at[0],
        'ccy_pair': model.ccy_pair,
        'lookback_hrs': model.lookback_hrs,
        'frequency_mins': model.frequency_mins,
        'prediction': model.predict()
    }
    return str(response) + "\n\n" + str(model.historical_quotes)
