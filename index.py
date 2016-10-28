import sys
import json
import arrow
import pandas
from datetime import datetime

sys.path.insert(0, 'src')
import retrieve
import stockHist as history

with open('terms.json') as data_file:
    comps = json.load(data_file)

headers = {
    'Content-Type': 'application/json',
    'Authorization': retrieve.authenticate()
}

global stockData
stockData = {}

def getAllTweets():
    allTweets = {}
    for company in comps:
        names = [c['name'] for c in company['people']]
        # concats lists and terms to search for
        terms = list(set([company['name']] + company['tickers'] + company['terms'] + company['products'] + names))

        companyTweets = []
        for term in terms:
            tweets = retrieve.getTweets(term, headers)
            companyTweets = list(tweets + companyTweets)
        companyTweets = list({ct['id']:ct for ct in companyTweets}.values()) # removes duplicate tweets

        dates = [arrow.get(tweet['created_at'], 'ddd MMM DD HH:mm:ss Z YYYY') for tweet in companyTweets]

        stockData[company['name']] = {
            'begin': min(dates),
            'end': max(dates),
            'ticker': company['tickers'][0]
        }

        allTweets[company['name']] = companyTweets
    return allTweets

tweetList = getAllTweets()
stockData = history.getStockData(stockData)
