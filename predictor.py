from typing_extensions import Self
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras import layers
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler


class Price_Predictor:
    def __init__(
        self,
        lstm_units_per_layer: int = 64,
        epochs: int = 100,
        lookback_timesteps: int = 30,
        lookahead_timesteps: int = 24,
        batch_size: int = 128,
    ) -> None:
        self.lstm_units_per_layer = lstm_units_per_layer
        self.epochs = epochs
        self.lookback_timesteps = lookback_timesteps
        self.lookahead_timesteps = lookahead_timesteps
        self.batch_size = batch_size

    def scale_data(self, input_df: pd.DataFrame, feature_range=(0, 1)):
        self.scaler = MinMaxScaler(feature_range=feature_range)
        self.scaled_data = pd.DataFrame(
            self.scaler.fit_transform(input_df), columns=input_df.columns
        )

    def create_windows(
        self,
        input_data: np.ndarray,
        window_shape: int,
        step: int = 1,
        start_id: int = 0,
        end_id: int = None,
    ):
        input_data = (
            input_data.values.reshape(-1, 1)
            if np.prod(input_data.shape) == max(input_data.shape)
            else input_data.values
        )
        end_id = input_data.shape[0] if end_id is None else end_id

        input_data = input_data[int(start_id) : int(end_id), :]
        window_shape = (int(window_shape), input_data.shape[-1])
        step = (int(step),) * input_data.ndim
        slices = tuple(slice(None, None, st) for st in step)
        indexing_strides = input_data[slices].strides
        win_indices_shape = ((np.array(input_data.shape) - window_shape) // step) + 1

        new_shape = tuple(list(win_indices_shape) + list(window_shape))
        strides = tuple(list(indexing_strides) + list(input_data.strides))

        window_data = np.lib.stride_tricks.as_strided(
            input_data, shape=new_shape, strides=strides
        )
        return np.squeeze(window_data, 1)

    def create_timeseries_dataset(self):
        data = self.scaled_data.drop(["close"], axis=1)
        self.data_cols_len = len(data.columns)
        targets = self.scaled_data["close"]
        X_train, X_test, y_train, y_test = train_test_split(data, targets)
        return (
            self.create_windows(
                X_train, self.lookback_timesteps, end_id=-self.lookahead_timesteps
            ),
            self.create_windows(
                X_test, self.lookback_timesteps, end_id=-self.lookahead_timesteps
            ),
            self.create_windows(
                y_train, self.lookback_timesteps, end_id=-self.lookahead_timesteps
            ),
            self.create_windows(
                y_test, self.lookback_timesteps, end_id=-self.lookahead_timesteps
            ),
        )

    def create_model(self):
        X_train, X_test, y_train, y_test = self.create_timeseries_dataset()
        self.model = keras.Sequential(
            [
                layers.GRU(
                    64,
                    input_shape=(self.lookback_timesteps, self.data_cols_len),
                    return_sequences=True,
                ),  # Input shape (30, 5)
                layers.Dropout(0.2),
                layers.GRU(64, return_sequences=True),
                layers.Dropout(0.2),
                layers.GRU(64, return_sequences=True),
                layers.Dropout(0.2),
                layers.GRU(64),
                layers.Dropout(0.2),
                layers.Dense(1, activation="sigmoid"),
            ]
        )
        self.model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
        self.model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            validation_data=(X_test, y_test),
            verbose=1,
        )

    def save_model(self, ticker):
        self.model.save(f"{ticker}.h5")
