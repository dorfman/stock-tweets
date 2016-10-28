import sys
import json
from datetime import datetime

sys.path.insert(0, 'src')
import retrieve

with open('terms.json') as data_file:
    comps = json.load(data_file)

headers = {
    'Content-Type': 'application/json',
    'Authorization': retrieve.authenticate()
}

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

        allTweets[company['name']] = companyTweets
    return allTweets

getAllTweets()
