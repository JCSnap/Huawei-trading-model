import pandas as pd

output_file = "./allStockNames.csv"

target_vol = 100

input_file = "./tickdata/tickdata_20220805.csv"

symbol_list = []
tick_data = pd.read_csv(input_file, index_col=None)
symbol = list(tick_data['COLUMN02'].unique())
symbol.sort()
for s in symbol:
  symbol_list.append([s]);

symbol_list = pd.DataFrame(symbol_list, columns=['symbol'])
symbol_list.to_csv(output_file, index=False)

