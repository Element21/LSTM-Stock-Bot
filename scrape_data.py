import requests
import pandas as pd
import pandas_datareader.data as web
import datetime as dt


def get_quote(tickers: list) -> pd.DataFrame:
    return web.YahooQuotesReader(
        tickers, start=dt.datetime.today(), end=dt.datetime.today()
    ).read()


def get_chart_data(
    tickers: list, interval: str = "d", adjust_price=True
) -> pd.DataFrame:
    # interval can be 'd' (daily), 'w' (weekly), 'm' (monthly)
    return (
        web.YahooDailyReader(
            tickers,
            adjust_price=adjust_price,
            start=dt.datetime(1970, 1, 1),
            end=dt.datetime.today(),
        )
        .read()
        .iloc[::-1]
    )


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
