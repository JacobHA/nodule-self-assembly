# Converts a csv file to a numpy array
import numpy as np
import pandas as pd


def convert_csv_to_nparray(csv_filename: str) -> np.ndarray:
    """
    Converts a csv file to a numpy array
    """
    df = pd.read_csv(csv_filename, header=None)
    np_array = df.to_numpy()
    # print(np_array)
    return np_array
