import sys
import json
import arrow
import pandas
from datetime import datetime

sys.path.insert(0, 'src')
import stockHist as history
import retrieve

with open('training-config.json') as data_file:
    config = json.load(data_file)

with open('terms.json') as data_file:
    terms = json.load(data_file)
comps = [t['tickers'][0] for t in terms]

def getAllStocks():
    stockData = {}
    for company in comps:
        stockData[company] = {
            'begin': arrow.get(config['begin'], 'MM-DD-YYYY'),
            'end': arrow.get(config['end'], 'MM-DD-YYYY'),
            'ticker': company
        }
    return stockData

def getHighsAndLows(data):
    for d in data:
        stocks = data[d]['stocks']

        stocks['Highest7 Value'] = pandas.Series(0.0, index=stocks.index)
        stocks['Highest7 Date'] = pandas.Series("", index=stocks.index)
        stocks['Highest7 Change'] = pandas.Series(0.0, index=stocks.index)

        stocks['Lowest7 Value'] = pandas.Series(0.0, index=stocks.index)
        stocks['Lowest7 Date'] = pandas.Series("", index=stocks.index)
        stocks['Lowest7 Change'] = pandas.Series(0.0, index=stocks.index)

        for index in range(len(stocks)):
            row = stocks.iloc[index]

            if (index - 6 > 0):
                highs = [stocks.iloc[index - i - 1]['High'] for i in range(7)]
                maxVal = max(highs)
                stocks.set_value(index, 'Highest7 Value', maxVal)
                stocks.set_value(index, 'Highest7 Date', stocks.iloc[index - highs.index(maxVal) - 1]['Date'])
                # (High - Low)/Low
                stocks.set_value(index, 'Highest7 Change', 100 * (maxVal - stocks.iloc[index]['Low'])/stocks.iloc[index]['Low'])

                lows = [stocks.iloc[index - i - 1]['Low'] for i in range(7)]
                minVal = min(lows)
                stocks.set_value(index, 'Lowest7 Value', minVal)
                stocks.set_value(index, 'Lowest7 Date', stocks.iloc[index - lows.index(minVal) - 1]['Date'])
                # (High - Low)/High
                stocks.set_value(index, 'Lowest7 Change', 100 * (minVal - stocks.iloc[index]['High'])/stocks.iloc[index]['High'])

def getSignificantDates(data):
    change = config['absChange']
    sigDates = {}

    for d in data:
        stocks = data[d]['stocks']
        sigDates[d] = []

        for index in range(len(stocks)):

            h7 = stocks.iloc[index]['Highest7 Change']
            if h7 > change or h7 < 0:  # TODO: Check for negative high or not?
                row = stocks.iloc[index]
                sigDates[d].append({'begin': row['Date'], 'end': row['Highest7 Date'], 'change': row['Highest7 Change']})

            l7 = stocks.iloc[index]['Lowest7 Change']
            if l7 < -change or l7 > 0: # TODO: Check for positive low or not?
                row = stocks.iloc[index]
                sigDates[d].append({'begin': row['Date'], 'end': row['Lowest7 Date'], 'change': row['Lowest7 Change']})

    return sigDates

def getTrainingSet():
    stockConfig = getAllStocks()
    data = history.getStockData(stockConfig)
    getHighsAndLows(data)
    trainSet = getSignificantDates(data)

    for t in trainSet:
        # print(pandas.DataFrame(trainSet[t]).sort_values('begin', ascending=True))
        pandas.DataFrame(trainSet[t]).sort_values('begin', ascending=True).to_csv(path_or_buf='./training/'+t+'.csv')

    return trainSet
