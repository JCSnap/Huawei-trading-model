import pandas as pd
import os
import csv
from pathlib import Path

directory = "../../tickdata/"
stocklistDir = "~/allStockNames.csv"
stocklistData = pd.read_csv(stocklistDir, index_col=None)
stockList=list(stocklistData['symbol'])
for f in os.scandir(directory):
    pricesArr = []
    
    with open(f) as fileObj:
        readerObj = csv.DictReader(fileObj)
        for row in readerObj:
            currBuyPrice = row['COLUMN58']
            
