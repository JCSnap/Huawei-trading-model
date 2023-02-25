import glob 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
import joblib

input_file = "~/tickdata/tickdata_20221230.csv"

tick_data = pd.read_csv(input_file, index_col=None)
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
od_book = []
difference_list = list()
ascii_symbol_list = list()
for sym in symbol:
    sym_data = tick_data[tick_data['COLUMN02'] == sym]

    # buy
    latest_sell = 0;
    for i, tm, late_sell in zip(sym_data['COLUMN01'], sym_data['COLUMN03'], sym_data['COLUMN53']):
        if tm > 145900000 and tm < 150000000:
            latest_sell = late_sell

    for i, sym, tm, buy_price in zip(sym_data['COLUMN01'], sym_data['COLUMN02'], sym_data['COLUMN03'], sym_data['COLUMN28']):
        curChar = ""
        for char in sym:
            curChar = curChar + str(ord(char))
        ascii_symbol_list.append(curChar)
        diff = latest_sell - buy_price
        difference_list.append(diff)

print(ascii_symbol_list)
tick_data = tick_data.assign(difference = difference_list)
tick_data = tick_data.assign(difference = difference_list)


tick_data.to_csv("./output_test1.csv", index=False)
