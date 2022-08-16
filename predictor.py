from typing_extensions import Self
import tensorflow as tf
from tensorflow import keras
from keras import layers


class Price_Predictor:
    def __init__(
        self,
        dataset: tf.data.Dataset = None,
        lstm_units_per_layer: int = 64,
        epochs=100,
        sequence_len = 30,
        fit_model = True
    ) -> None:
        if dataset is None:
            raise Exception("Dataset must be specified!")
        self.dataset = dataset
        self.lstm_units_per_layer = lstm_units_per_layer
        self.epochs = epochs
        self.sequnce_len = sequence_len
        self.fit_model = fit_model

    def create_model(self):
        model = keras.Sequential(
            [
                layers.LSTM(
                    self.lstm_units_per_layer,
                    input_shape=(1, self.sequnce_len),
                    return_sequences=True
                ),
                layers.Dropout(0.2),
                layers.LSTM(
                    self.lstm_units_per_layer,
                    return_sequences=True
                ),
                layers.Dropout(0.2),
                layers.LSTM(
                    self.lstm_units_per_layer,
                    return_sequences=True
                ),
                layers.Dropout(0.2),
                layers.LSTM(
                    self.lstm_units_per_layer
                ),
                layers.Dropout(0.2),
                layers.Dense(1, activation="sigmoid"),
            ]
        )
        model.compile(optimizer="adam", loss="mse", run_eagerly=True)
        if self.fit_model:
            model.fit(self.dataset, epochs=self.epochs, verbose=0)
        return model

    def fit_model(self, input_model):
        input_model
