import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score
import numpy as np
import sys
import variables

model = load('model_10000.joblib')

rows = variables.rows
columns = variables.columns

# FOR TESTING PURPOSES
# We will take a different file without the "difference" column and put it into the
# model to predict the "difference"

path = "../tickdata/tickdata_20221230.csv"
df = pd.read_csv(path, index_col=None)
ascii_symbol_list = list()

# get unique stock code
symbol = list(df['COLUMN02'].unique())
symbol.sort()

stock_dict = {}
ascii_dict = {}
for sym in symbol:
    # for each stock, get all the rows that belongs to the stock
    sym_data = df[df['COLUMN02'] == sym]

    # to track lastest selling price
    latest_sell = 0;
    for idx, tm, late_sell in zip(sym_data['COLUMN01'], sym_data['COLUMN03'], sym_data['COLUMN08']):
        # get the price right before 3pm, there are probably better ways to do it
        if tm > 112000000 and tm < 113000000 or tm > 145900000 and tm < 150000000:
            latest_sell = late_sell

        list_in_dict = list()
        # check whether we already have a record of the ascii representation
        if sym in ascii_dict:
            cur_ascii = ascii_dict[sym]
            list_in_dict.append(cur_ascii)
        # if not, we create a new record so that in the future we don't have to keep recalculating
        # the ascii for the same stock
        else:
            curChar = ""
            for char in sym:
                curChar = curChar + str(ord(char))
            ascii_dict[sym] = curChar
            list_in_dict.append(curChar)
        # record the ascii representation of each row (or index)
        stock_dict[idx] = list_in_dict
    # update latest sell price of each stock

    for idx in sym_data['COLUMN01']:
        list_in_dict = stock_dict[idx]
        list_in_dict.append(latest_sell)
        stock_dict[idx] = list_in_dict
    
print("Completed finding latest selling price for each stock")

# difference for each tick is just the difference between selling price at 3pm and current buy price

print("Starting to calculate difference for each row")
ascii_symbol_list = list()
difference_list = list()
for idx, sym, buy_price in zip(df['COLUMN01'], df['COLUMN02'], df['COLUMN28']):
    list_in_dict = stock_dict[idx]
    # index 1 stores the latest selling price for the row
    latest_sell = list_in_dict[1] 
    diff = latest_sell - buy_price
    # index 0 stores the ascii representation of the current stock code
    cur_ascii = list_in_dict[0]
    ascii_symbol_list.append(cur_ascii)
    difference_list.append(diff)
print("Completed calculating difference for each row")

df['COLUMN02'] = ascii_symbol_list
# convert the list into a data frame 
df = df.assign(difference = difference_list)

X_test = df.drop('difference', axis=1).values[:rows]
X_test2 = X_test[:, columns]
Y_actual = df.loc[:, 'difference'].values[:rows]

Y_predict = model.predict(X_test2)

accuracy = accuracy_score(Y_predict, Y_actual)

np.set_printoptions(threshold=sys.maxsize)
result = np.concatenate((Y_predict.reshape(-1, 1), Y_actual.reshape(-1, 1)), axis=1)
print(result)
print(accuracy)
