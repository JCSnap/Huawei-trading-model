import glob 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from joblib import dump
import variables

# refers to ALL the files that end with .csv 
path = "../tickdata/tickdata_20221229.csv"

files = glob.glob(path)

rows = variables.rows
columns = variables.columns 

# store data for all the files
df_list = [] 
count = 0;
for file in files:
    count = count + 1
    print("Processing file " + str(count) + "...")
    df = pd.read_csv(file, index_col=None)
    # get unique stock code
    symbol = list(df['COLUMN02'].unique())
    symbol.sort()

    # End goal is to add a new column called "difference" to feed into the model 
    # and to replace all stock codes (which are in string) to ascii since the model can only take numbers

    # creating a new list to store the values of "right answers" to feed into ML
    difference_list = list()
    # creating a new list to store the ascii representations
    ascii_symbol_list = list()
    # dictionary with stock index as key, last sell price and ascii as list
    stock_dict = {}
    # keep track of stock and their corresponding ascii representation
    ascii_dict = {}

    print("Starting to find latest selling price for each stock")
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
    for idx, buy_price in zip(df['COLUMN01'], df['COLUMN28']):
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
    # compile dataframes of each file into one giant list
    df_list.append(df)

# concatenate all dataframes into a single dataframe
data = pd.concat(df_list, axis=0, ignore_index=True)

# select all columns excluding "difference"
X_train = df.drop('difference', axis=1).values[:rows]
X_train2 = X_train[:, columns]
# only select the "difference" column
Y_train = df.loc[:, 'difference'].values[:rows]

print("Starting model training")
model = DecisionTreeClassifier()
model = model.fit(X_train2, Y_train);

dump(model, 'model_10000.joblib')
print("Ended model training")


