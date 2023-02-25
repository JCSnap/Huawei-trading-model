#!/usr/bin/env python 
# -*- coding:utf-8 -*

import numpy as np
import pandas as pd
import sys
import joblib
import variables
import math

input_file = sys.argv[1]
output_file = sys.argv[2]
model_file = 'model_10000.joblib'
target_vol = 100
columns = variables.columns

def get_ms(tm):
    hhmmss = tm // 1000
    ms = (hhmmss // 10000 * 3600 + (hhmmss // 100 % 100) * 60 + hhmmss % 100) * 1000 + tm % 1000
    ms_from_open = ms - 34200000  # millisecond from stock opening
    if tm >= 130000000:
        ms_from_open -= 5400000
    return ms_from_open


tick_data = pd.read_csv(input_file, index_col=None)
symbol = list(tick_data['COLUMN02'].unique())
symbol.sort()
model = joblib.load(model_file)

# simple prediction strategy
od_book = []
for sym in symbol:
    sym_data = tick_data[tick_data['COLUMN02'] == sym]
    cum_vol_buy = 0  # accumulate buying volume
    unfinished_buy = 0  # unfinished buying volume in this round
    unfinished_sell = 0  # unfinished selling volume in this round

    index = sym_data['COLUMN01'].values
    ms = sym_data['COLUMN03'].apply(lambda x: get_ms(x)).values
    ms_original = sym_data['COLUMN03'].values
    price = sym_data['COLUMN07'].values

    cur_char = ""
    for char in sym:
        cur_char = cur_char + str(ord(char))
    ascii_stock = cur_char

    ascii_col = sym_data['COLUMN02'].apply(x = ascii_stock)
    sym_data['ascii_col'] = ascii_col  

    for i in range(len(ms)):
        if ms[i] < 13800000:  # before 14:50:00
            cur_row = sym_data.iloc[i + 1]
            cur_price = price[i]
            X_predict = cur_row[:, columns].values
            predicted_profit = model.predict(X_predict)
            
            if predicted_profit > 5000 and cum_vol_buy < target_vol:
                od_vol = 10
                if od_vol > target_vol - cum_vol_buy:
                    od_vol = target_vol - cum_vol_buy
                od_book.append([sym, 'B', index[i], od_vol])
        else:
            if target_vol - cum_vol_buy > 0:  # force complete before market closes
                od_book.append([sym, 'B', index[i], target_vol - cum_vol_buy])

            od_book.append([sym, 'S', index[i], target_vol])
            break

od_book = pd.DataFrame(od_book, columns=['symbol', 'BSflag', 'dataIdx', 'volume'])
od_book.to_csv(output_file, index=False)
