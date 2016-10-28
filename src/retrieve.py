import requests
import json
from bs4 import BeautifulSoup
import base64

with open('config.json') as data_file:
    config = json.load(data_file)

def authenticate():
    clientKeyAndSecret = config['twitter']['client_key'] + ':' + config['twitter']['client_secret']

    postBody = {'grant_type': 'client_credentials'}
    encodedClientKeyAndSecret = str(base64.b64encode(clientKeyAndSecret.encode('ascii')))[2:-1]
    headers = {
        'Authorization': 'Basic ' + encodedClientKeyAndSecret,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    resp = requests.post(url='https://api.twitter.com/oauth2/token', data=postBody, headers=headers)
    if resp.status_code != 200:
        print(resp.status_code, resp.reason)
    else:
        bearer = resp.json()['token_type'][0:1].upper() + resp.json()['token_type'][1:]
        return bearer + ' ' + resp.json()['access_token']

def printTweets(tweets):
    for t in tweets:
        soupText = BeautifulSoup(t['text'], 'html.parser')
        soupUser = BeautifulSoup(t['user']['name'], 'html.parser')
        print(soupUser.encode('utf-8'), '\t\t', soupText.encode("utf-8"))

def getTweets(query, headers):
    url = 'https://api.twitter.com/1.1/search/tweets.json?lang=en&result_type=mixed&q='

    resp = requests.get(url=url+query, headers=headers)
    if resp.status_code != 200:
        print(resp.status_code, resp.reason)
    else:
        statuses = json.loads(resp.text)['statuses']
        return statuses