import sys
import json
import arrow
import pandas
from datetime import datetime

sys.path.insert(0, 'src')
import retrieve
import stockHist as history
import training as train

with open('terms.json') as data_file:
    comps = json.load(data_file)

headers = {
    'Content-Type': 'application/json',
    'Authorization': retrieve.authenticate()
}

if (len(sys.argv) > 1):
    tSet = train.getTrainingSet()
    print(tSet)

else:
    tweetList, stockData = retrieve.getAllTweets(headers)
    stockData = history.getStockData(stockData)
    print(stockData)