from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.predictor import CryptoPricePredictor


class RequestBody(BaseModel):
    lookback_hrs: int = Field(default=1, gt=0)
    frequency_mins: int = Field(default=1, gt=0)
    ccy_pair: str = Field(default="BTCUSD", max_length=6, min_length=6)


app = FastAPI()


@app.post('/predictions',
          summary="BTC/USD price prediction endpoint",
          tags=["BTC Price Prediction"])
def predict_btcusd(req: RequestBody):
    model = CryptoPricePredictor(
        ccy_pair="BTCUSD",
        lookback_hrs=req.lookback_hrs,
        frequency_mins=req.frequency_mins
    )
    model.get_historical_quotes()

    response = {
        'requested_at': model.historical_quotes.requested_at[0],
        'ccy_pair': req.ccy_pair,
        'lookback_hrs': req.lookback_hrs,
        'frequency_mins': req.frequency_mins,
        'prediction': model.predict()
    }

    with open(file="./logs/responses.txt", mode='a') as f:
        f.write(str(response) + '\n')

    return response
