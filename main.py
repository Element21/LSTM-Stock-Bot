import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
import scrape_data
import utils
import predictor
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.formatted_text import HTML
import tensorflow as tf
from datetime import datetime, timedelta
import time

dbg = True

if dbg:
    # sector_performance = pd.read_csv("sector_performance.csv")
    nasdaq_symbols = pd.read_csv("nasdaq_symbols.csv")
else:
    # sector_performance = scrape_data.get_sector_performance()
    nasdaq_symbols = scrape_data.get_nasdaq_symbols()

print(scrape_data.screen_for_stocks(strategy='trending'))

# scaler = StandardScaler()

# with ProgressBar(
#     title=HTML(
#         f'Fitting models for <style bg="yellow" fg="black">{ticker_daily_change_dict.shape[0]} tickers...</style>'
#     )
# ) as pb:
#     for ticker, _ in pb(ticker_daily_change_dict):
#         data = scrape_data.get_ticker_timeseries_data(ticker)
#         data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
#         dataset = utils.create_timeseries_dataset(data, is_ticker_crypto=True)
#         LSTM_Predictor = predictor.LSTM(lstm_units_per_layer=64)
#         model = LSTM_Predictor.create_model()
#         model.fit(dataset, epochs=100, verbose=0)
#         model.save(f"{ticker}.h5")
