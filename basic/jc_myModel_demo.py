#!/usr/bin/env python 
# -*- coding:utf-8 -*

import pandas as pd
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]
target_vol = 100

tick_data = pd.read_csv(input_file, index_col=None)
# get unique stock code
symbol = list(tick_data['COLUMN02'].unique())
symbol.sort()


def get_time_rate(tm):
    hhmmss = tm // 1000
    ms = (hhmmss // 10000 * 3600 + (hhmmss // 100 % 100) * 60 + hhmmss % 100) * 1000 + tm % 1000
    ms_from_open = ms - 34200000  # millisecond from stock opening
    if tm >= 130000000:
        ms_from_open -= 5400000
    return ms_from_open / 14400000


# simple time average strategy

# array to keep track of buy and sell
od_book = [] 
buy_weighted_ave = {}
sell_weighted_ave = {}
for sym in symbol:
    # column that belongs to the stock code
    sym_data = tick_data[tick_data['COLUMN02'] == sym]
    
    # buy
    od_nCount = 5
    od_vol = target_vol // od_nCount
    # index to "track" od_book
    od_idx = 0
    # total volume bought
    cum_vol = 0
    for i, tm, buy, b_price in zip(sym_data['COLUMN01'], sym_data['COLUMN03'], sym_data['COLUMN53'], sym_data['COLUMN28']):
        threshold = 0
        if sys not in buy_weighted_ave:
            threshold = buy
        else :
            threshold = buy_weighted_ave[sys]

        # had to stop before 3pm 
        if tm < 145000000: 
            tm_rate = get_time_rate(tm)
            if tm_rate > od_idx / od_nCount and b_price < threshold:
                od_book.append([sym, 'B', i, od_vol])
                od_idx += 1
                cum_vol += od_vol
        elif target_vol - cum_vol > 0:  # force complete before market closes
            od_book.append([sym, 'B', i, target_vol - cum_vol])
        buy_weighted_ave[sys] = buy

    # sell
    od_nCount = 10
    od_vol = target_vol // od_nCount
    od_idx = 0
    cum_vol = 0
    for i, tm, sell, s_price in zip(sym_data['COLUMN01'], sym_data['COLUMN03'], sym_data['COLUMN54'], sym_data['COLUMN08']):
        threshold = 0
        if sys not in sell_weighted_ave:
            threshold = sell
        else :
            threshold = sell_weighted_ave[sys]

        if tm < 145000000:
            tm_rate = get_time_rate(tm)
            if tm_rate > od_idx / od_nCount and s_price > threshold:
                od_book.append([sym, 'S', i, od_vol])
                od_idx += 1
                cum_vol += od_vol
        elif target_vol - cum_vol > 0:  # force complete before market closes
            od_book.append([sym, 'S', i, target_vol - cum_vol])
        sell_weighted_ave[sys] = sell

od_book = pd.DataFrame(od_book, columns=['symbol', 'BSflag', 'dataIdx', 'volume'])
od_book.to_csv(output_file, index=False)
