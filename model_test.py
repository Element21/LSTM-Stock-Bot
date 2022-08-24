import scrape_data
import tensorflow as tf
from tensorflow import keras
from keras import layers
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

# df = scrape_data.get_chart_data("AAPL")
df = pd.read_csv("AAPL.csv")
scaled_data = pd.DataFrame(scaler.fit_transform(df.values), columns=df.columns)
data = scaled_data.drop(["Close"], axis=1)
targets = scaled_data["Close"]

target_scaler.fit(df["Close"].values.reshape(-1, 1))

# dataset = tf.keras.utils.timeseries_dataset_from_array(
#     data=data, targets=targets, sequence_length=30
# )

# model = keras.Sequential(
#     [
#         layers.GRU(32, input_shape=(30, 5), return_sequences=True),
#         layers.Dropout(0.2),
#         layers.GRU(32, return_sequences=True),
#         layers.Dropout(0.2),
#         layers.GRU(32, return_sequences=True),
#         layers.Dropout(0.2),
#         layers.GRU(32),
#         layers.Dropout(0.2),
#         layers.Dense(1, activation="sigmoid"),
#     ]
# )

# model.compile(optimizer="adam", loss="mse")
# model.fit(dataset, epochs=100)
# model.save('AAPL.h5')


# Load
model = keras.models.load_model("AAPL.h5")

print(model.predict(data.iloc[1:31].values.reshape(-1, 30, 5)))

print(
    f"Ticker: AAPL, Actual Price: {df['Close'].iloc[0]}, Predicted Close Price: {target_scaler.inverse_transform(model.predict(data.iloc[1:31].values.reshape(-1, 30, 5)).reshape(1, -1)).reshape(-1)[0]}"
)
