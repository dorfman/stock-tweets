import sys
import json

sys.path.insert(0, 'src')
import retrieve
import stockHist as history
import training as train

with open('terms.json') as data_file:
    comps = json.load(data_file)


if (len(sys.argv) > 1):
    tSet = train.getTrainingSetDates()
    tset = train.getTrainingSetTweets(tSet)

else:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': retrieve.authenticate()
    }

    tweetList, stockData = retrieve.getAllRecentTweets(headers)
    stockData = history.getStockData(stockData)
    print(stockData)