from typing_extensions import Self
import tensorflow as tf
from tensorflow import keras
from keras import layers
import pandas as pd


class LSTM:
    def __init__(self, lstm_units_per_layer: int = 64) -> None:
        self.lstm_units_per_layer = lstm_units_per_layer

    def create_model(self):
        model = keras.Sequential(  # 12 stacked lstm layers with a droupout layer of 0.2 following each
            [
                layers.LSTM(
                    self.lstm_units_per_layer, input_shape=(1, 5), return_sequences=True
                ),
                layers.Dropout(0.2),
                layers.LSTM(self.lstm_units_per_layer, return_sequences=True),
                layers.Dropout(0.2),
                layers.LSTM(self.lstm_units_per_layer, return_sequences=True),
                layers.Dropout(0.2),
                layers.LSTM(self.lstm_units_per_layer, return_sequences=True),
                layers.Dropout(0.2),
                layers.LSTM(self.lstm_units_per_layer),
                layers.Dropout(0.2),
                layers.Dense(1, activation="sigmoid"),
            ]
        )
        model.compile(optimizer="adam", loss="mse")
        return model
