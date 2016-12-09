import sys
import json
import arrow
import pandas
from datetime import datetime
from time import sleep

sys.path.insert(0, 'src')
import stockHist as history
import retrieve

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

with open('training-config.json') as data_file:
    config = json.load(data_file)

with open('terms.json') as data_file:
    terms = json.load(data_file)
tickers = [t['tickers'][0] for t in terms]

def getAllStocks():
    stockData = {}
    for company in tickers:
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

def getTrainingSetDates():
    stockConfig = getAllStocks()
    data = history.getStockData(stockConfig)
    getHighsAndLows(data)
    trainSet = getSignificantDates(data)

    return trainSet

def getTweets(term, begin, end):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(term).setSince(begin).setUntil(end).setMaxTweets(10)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    return tweets

# headers not needed. using github lib
def loopTermTweets(terms, begin, end):
    companyTweets = []
    for term in terms:
        tweets = getTweets(term, begin, end)
        if len(tweets) > 0:
            print(tweets[0].text)
        companyTweets = list(tweets + companyTweets)
        sleep(0.125)
    return list({ct['id']:ct for ct in companyTweets}.values()) # removes duplicate tweets

def getTrainingSetTweets(setDates):
    for company in terms:
        for dates in setDates[company['tickers'][0]]:
            dates['tweets'] = loopTermTweets(retrieve.getTerms(company), dates['begin'], dates['end'])
        df = pandas.DataFrame(setDates[company['tickers'][0]])
        df.to_csv(company['name'] + '.csv')
        df.to_json(company['name'] + '.json')
    return setDates