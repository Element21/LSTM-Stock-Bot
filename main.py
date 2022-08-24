import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
import scrape_data
import predictor
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.formatted_text import HTML
import tensorflow as tf
import datetime as dt

MARKET_OPEN = dt.time(9, 30)
MARKET_CLOSE = dt.time(16, 0)

chosen_tickers = scrape_data.screen_for_stocks(strategy="yf_screener")

# scrape_data.get_bar_data("AAPL").to_csv("AAPL.csv")

price_predictor = predictor.Price_Predictor()
# data = scrape_data.get_chart_data(chosen_tickers[0])
data = pd.read_csv("AAPL.csv", index_col=0)
print(data)
price_predictor.scale_data(data)
price_predictor.create_model()
price_predictor.save_model("AAPL")

# with ProgressBar(title='Fitting models') as pb:
#     for ticker in pb(chosen_tickers):
#         data = scrape_data.get_chart_data(ticker)
#         scaled_data = utils.scale_data(data)
#         dataset = utils.create_timeseries_dataset(scaled_data)
#         price_predictor = predictor.Price_Predictor(dataset=dataset)
#         model = price_predictor.create_model()
#         model.save(f'{ticker}.h5')
