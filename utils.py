import utils
import scrape_data
import pandas as pd
import tensorflow as tf

# def find_symbols(
#     sector_performance_df: pd.DataFrame,
#     nasdaq_symbol_df: pd.DataFrame,
#     sector_col: str = "RT",
#     symbol_col: str = "Symbol",
#     amount: int = 100,
# ):
#     """Given the amount of tickers to output, this function will find the top performing stocks (intraday change) in the highest performing sector (current day)"""
#     sector_performance_df.rename(columns={"Unnamed: 0": "Sector"}, inplace=True)
#     sector_performance_df.sort_values([sector_col], ascending=False, inplace=True)
#     best_sector = sector_performance_df["Sector"].iloc[
#         0
#     ]  # Best sector by realtime (current day's) change
#     ticker_descriptions = scrape_data.get_ticker_overview(
#         nasdaq_symbol_df[symbol_col].values
#     )
#     return ticker_descriptions


def create_timeseries_dataset(
    dataframe: pd.DataFrame,
    is_ticker_crypto: bool = False,
    batch_size: int = 128,
    sequence_len: int = 30,
) -> tf.data.Dataset:
    if is_ticker_crypto:
        data = dataframe.drop(["Close"], axis=1)
        targets = dataframe["Close"]
    else:
        data = dataframe.drop(["Adj Close"], axis=1)
        targets = dataframe["Adj Close"]
    dataset = tf.keras.utils.timeseries_dataset_from_array(
        data,
        targets,
        sequence_len,
        batch_size=batch_size,
    )
    return dataset
