import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys
import math
import keras
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from keras.layers import *
#from sklearn.preprocessing import MinMaxScale
#from sklearn.metrics import mean_squared_error
#from sklearn.metrics import mean_absolute_error
#from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping

path = "../tickdata/*.csv"
all_files = glob.glob(path)
df_list = []

use_cols = [3, 4, 5, 6, 7, 48, 49, 50, 51, 52, 53, 54, 55]
#opening price, highest, lowest, latest price
for filename in all_files:
    df = pd.read_csv(filename, use_cols)
    df_list.append(df)

data = pd.concat(df_list, axis = 0, ignore_index = True) 

def exponential_smooth(data, alpha):
    return data.ewm(alpha = alpha).mean()

data = exponential_smooth(data, 0.65)
print(data)
#def get_indicator_data(data):
#    for indicator in 
#input_file = sys.argv[1]
#output_file = sys.argv[2]
