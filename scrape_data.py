import requests
import pandas as pd
import pandas_datareader.data as web

def get_chart_data(
    ticker: str,
    range: str = "max",
    interval: str = "1m",
    api_key: str = "6NWi8AzVGgadJZBPv1BGY3Fyn6yG7QuU8T70fvEm"
) -> pd.DataFrame:
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }

    valid_ranges = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "ytd", "max"]
    valid_intervals = ["1m", "5m", "15m", "1d", "1wk", "1mo"]

    if range not in valid_ranges:
        raise Exception(
            f"{range} is not a valid range! 'range' must be one of: {valid_ranges}"
        )
    if interval not in valid_intervals:
        raise Exception(
            f"{interval} is not a valid interval! 'interval' must be one of: {valid_intervals}"
        )

    querystring = {
        "range": range,
        "interval": interval,
    }

    r = requests.get(f"https://yfapi.net/v8/finance/chart/{ticker}", params=querystring, headers=headers)
    print(r.url)
    ticker_json = r.text
    return ticker_json


def screen_for_stocks(strategy: str, yf_screener_id: str = "day_gainers", region: str = "US", count: int = 25, api_key: str = "6NWi8AzVGgadJZBPv1BGY3Fyn6yG7QuU8T70fvEm") -> list:
    output = []
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }
    valid_strategies = ["yf_screener", "trending"]
    valid_regions = ["US", "AU", "CA", "FR", "DE", "HK", "US", "IT", "ES", "GB", "IN"]
    if strategy not in valid_strategies:
        raise Exception(f"{strategy} is not a valid strategy! 'strategy' must be one of: {valid_strategies}")
    if region not in valid_regions:
        raise Exception(f"{region} is not a valid region! 'region' must be one of: {valid_regions}")
    if strategy == "yf_screener":
        querystring = {
            "count": count,
            "scrIds": yf_screener_id
        }
        r = requests.get('https://yfapi.net/ws/screeners/v1/finance/screener/predefined/saved', headers=headers, params=querystring)
        return r.text
    elif strategy == "trending":
        r = requests.get(f'https://yfapi.net/v1/finance/trending/{region}', headers=headers)
        for i in r.json()['finance']['result']: # Really gross datastructure
            for ticker in i["quotes"]:
                if ticker is not None and '^' not in ticker["symbol"]: # Filter out non tradable tickers
                    output.append(ticker["symbol"])
        return output