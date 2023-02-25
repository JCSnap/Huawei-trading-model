import glob 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
import joblib

input_file = "./output_test1.csv"

tick_data = pd.read_csv(input_file, index_col=None)
symbol = list(tick_data['difference'].unique())
symbol.sort()

for sym in symbol:
    print(sym)



