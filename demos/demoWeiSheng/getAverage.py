import pandas as pd
import os
import csv
from pathlib import Path

directory = "../../tickdata/"
stocklistDir = "~/allStockNames.csv"
stocklistData = pd.read_csv(stocklistDir, index_col=None)
stockList=list(stocklistData['symbol'])
for f in os.scandir(directory):
    stockAverageInfo = {}
    stockDict = {}
    for stock in stockList:
        tmp = {
          'Stock': stock, 
          'BuyPrice': 0, 
          'BuyVolume': 0, 
          'SellPrice': 0,
          'SellVolume': 0
          }
        stockDict[stock] = tmp;

    with open(f) as fileObj:
        readerObj = csv.DictReader(fileObj)
        fileName = './avePrices/' + Path(f).stem + '.csv'
        if path.exists(fileName) and len(pd.read_csv(fileName)) >= 501:
            continue;
        for row in readerObj:
            stock = row['COLUMN02']
            aveBuyPrice = int (row['COLUMN54'])
            aveSellPrice = int (row['COLUMN55'])
            aveBuyVol = int (row['COLUMN48'])
            aveSellVol = int (row['COLUMN49'])
        
            stockDict[stock]['BuyPrice'] = stockDict[stock]['BuyPrice'] + aveBuyPrice * aveBuyVol
            stockDict[stock]['BuyVolume'] = stockDict[stock]['BuyVolume'] + aveBuyVol 
            stockDict[stock]['SellPrice'] = stockDict[stock]['SellPrice'] + aveSellPrice * aveSellVol
            stockDict[stock]['SellVolume'] = stockDict[stock]['SellVolume'] + aveSellVol

        for stock in stockList:
            stockDict[stock]['BuyPrice'] = stockDict[stock]['BuyPrice'] / stockDict[stock]['BuyVolume']
            stockDict[stock]['SellPrice'] = stockDict[stock]['SellPrice'] / stockDict[stock]['SellVolume']

        stockListProcessed = []
        for stock in stockList:
            stockListProcessed.append(stockDict[stock])

        df = pd.DataFrame(stockListProcessed)
        df.to_csv(fileName, index=False, header=True)

