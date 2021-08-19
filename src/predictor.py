from datetime import datetime, timezone

import requests
import pandas as pd


class CryptoPricePredictor:
    """Class for cryptocurrency price predictions using public API.

        Parameters
        ----------
        ccy_pair : str
            Currency pair in 6-char format (e.g. BTCUSD)
        frequency_mins : int
            Frequency of price quotes fetched from the API
        lookback_hrs: int
            Number of hours to look back into history when fetching price quotes
        exchange: str, optional, default = 'coinbase-pro'
            Exchange to fetch quotes from.
        """

    def __init__(self, ccy_pair: str, frequency_mins: int, lookback_hrs: int,
                 exchange: str = 'coinbase-pro'):
        self.ccy_pair = ccy_pair
        self.frequency_mins = frequency_mins
        self.lookback_hrs = lookback_hrs
        self.exchange = exchange

    @staticmethod
    def timestamp_to_str(timestamp: int) -> str:
        """Convert POSIX timestamp in UTC to ISO format string."""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

    def get_historical_quotes(self) -> None:
        """Get historical quotes from the Cryptowat API."""
        base_url = f"https://api.cryptowat.ch/markets/{self.exchange}/{self.ccy_pair}/ohlc"
        periods = str(60 * self.frequency_mins)  # Based on API specification

        current_ts_int = int(datetime.now(tz=timezone.utc).timestamp())
        current_ts_str = self.timestamp_to_str(current_ts_int)
        first_ts = current_ts_int - self.lookback_hrs*60*60

        response = requests.get(url=base_url, params={"after": first_ts, "periods": periods})
        quotes = response.json().get("result").get(periods)

        result = [(current_ts_str, self.timestamp_to_str(quote[0]), quote[4]) for quote in quotes]
        self.historical_quotes = pd.DataFrame(data=result, columns=['requested_at', 'ts', 'quote'])

        return None

    def predict(self) -> float:
        """Calculate CCY pair price prediction."""
        return round(float(self.historical_quotes['quote'].mean()), 4)
