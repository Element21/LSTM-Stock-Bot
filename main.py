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

chosen_tickers = scrape_data.screen_for_stocks(strategy="trending")

with ProgressBar(
    title=HTML(
        f'Fitting models for <style bg="yellow" fg="black">{len(chosen_tickers)} tickers...</style>'
    )
) as pb:
    for ticker in pb(chosen_tickers):
        data = scrape_data.get_chart_data(ticker)
        scaled_data = utils.scale_data(data)
        dataset = utils.create_timeseries_dataset(scaled_data)
        price_predictor = predictor.Price_Predictor(dataset=dataset)
        model = price_predictor.create_model()
        model.save(f'{ticker}.h5')