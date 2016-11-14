# stock-tweets
Looks for a correlation between tweets and stocks. 

Uses the Yahoo Finance and Twitter APIs to retrieve stock information and tweets
that were posted within the last week, respectively.
Uses the [GetOldTweets](https://github.com/Jefferson-Henrique/GetOldTweets-python)
project to retrieve tweets that were posted over a week ago.

## Requirements
Python 3.5.2

## Install
> pip3 install -r requirements.txt

## Run
> python index

## To Collect Training Set Data
> python index --training

## Modification to GetOldTweets-python-master
- Added parentheses to `print` calls
- Removed `got` directory and renamed `got3` to be `got`