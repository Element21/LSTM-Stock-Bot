import numpy as np


class Price_Predictor:
    def __init__(self) -> None:
        pass

    def sliding_window(self, input_data: np.ndarray) -> None:
        # Use some numpy methods
        print(input_data.shape)


pp = Price_Predictor()

i = np.array([1, 2, 3, 4, "I", "Declare", "a", "Thumb", "War"])

pp.sliding_window(i)
