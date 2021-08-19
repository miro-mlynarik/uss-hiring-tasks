from datetime import datetime, timezone

import requests


class CryptoPricePredictor:

    def __init__(self, ccy_pair: str, timestep_mins: int, lookback_hrs: int,
                 exchange: str = 'coinbase-pro'):
        self.ccy_pair = ccy_pair
        self.timestep_mins = timestep_mins
        self.lookback_hrs = lookback_hrs
        self.exchange = exchange

    def get_historical_quotes(self) -> None:
        """Get historical quotes from the Cryptowat API."""
        base_url = f"https://api.cryptowat.ch/markets/{self.exchange}/{self.ccy_pair}/ohlc"
        periods = str(60 * self.timestep_mins)  # Based on API specification

        current_ts = int(datetime.now(tz=timezone.utc).timestamp())
        first_ts = current_ts - self.lookback_hrs*60*60

        response = requests.get(url=base_url, params={"after": first_ts, "periods": periods})
        quotes = response.json().get("result").get(periods)

        return quotes


if __name__ == '__main__':
    model = CryptoPricePredictor(ccy_pair="BTCUSD", timestep_mins=5, lookback_hrs=6)
    print(model.get_historical_quotes())
