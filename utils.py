import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler


def scale_data(input_df: pd.DataFrame, feature_range=(0, 1)):
    scaler = MinMaxScaler(feature_range=feature_range)
    return pd.DataFrame(scaler.fit_transform(input_df), columns=input_df.columns)


def create_timeseries_dataset(
    dataframe: pd.DataFrame,
    batch_size: int = 128,
    sequence_len: int = 30,
) -> tf.data.Dataset:
    data = dataframe.drop(["Close"], axis=1)
    targets = dataframe["Close"]
    return tf.keras.utils.timeseries_dataset_from_array(
        data,
        targets,
        sequence_len,
        batch_size=batch_size,
    )
