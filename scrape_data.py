from sqlite3 import Time
import requests
import pandas as pd
import datetime as dt
from alpaca_trade_api.rest import REST, TimeFrame

API_KEY = "PKKBMM1AYSSXPDLLRLUD"
API_SECRET = "JEw43h923In1Z9y9VlhfJovw86QcQLEN9YWjiPq1"
BASE_URL = "https://paper-api.alpaca.markets"

alpaca = REST(API_KEY, API_SECRET, BASE_URL)


def get_bar_data(
    ticker: str | list[str],
    interval: TimeFrame = TimeFrame.Hour,
    adj="all",
    lmt: int = int(10e12),
) -> pd.DataFrame:
    return alpaca.get_bars(
        ticker, interval, "2000-01-01T00:00:00Z", adjustment=adj, limit=lmt, feed="sip"
    ).df


def screen_for_stocks(
    strategy: str,
    yf_screener_id: str = "day_gainers",
    region: str = "US",
    count: int = 25,
    api_key: str = "6NWi8AzVGgadJZBPv1BGY3Fyn6yG7QuU8T70fvEm",
) -> list:
    output = []
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }
    valid_strategies = ["yf_screener", "trending"]
    valid_regions = ["US", "AU", "CA", "FR", "DE", "HK", "US", "IT", "ES", "GB", "IN"]
    if strategy not in valid_strategies:
        raise Exception(
            f"{strategy} is not a valid strategy! 'strategy' must be one of: {valid_strategies}"
        )
    if region not in valid_regions:
        raise Exception(
            f"{region} is not a valid region! 'region' must be one of: {valid_regions}"
        )
    if strategy == "yf_screener":
        querystring = {"count": count, "scrIds": yf_screener_id}
        r = requests.get(
            "https://yfapi.net/ws/screeners/v1/finance/screener/predefined/saved",
            headers=headers,
            params=querystring,
        )
        return r.text
    elif strategy == "trending":
        r = requests.get(
            f"https://yfapi.net/v1/finance/trending/{region}", headers=headers
        )
        for i in r.json()["finance"]["result"]:  # Really gross datastructure
            for ticker in i["quotes"]:
                if (
                    ticker is not None and "^" not in ticker["symbol"]
                ):  # Filter out non tradable tickers
                    output.append(ticker["symbol"])
        return output
