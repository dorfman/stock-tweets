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
    tSet = train.getTrainingSetDates()
    train.getTrainingSetTweets(tSet)
    # print(tSet)
    # retrieve.getAllTweets

else:
    tweetList, stockData = retrieve.getAllRecentTweets(headers)
    stockData = history.getStockData(stockData)
    print(stockData)