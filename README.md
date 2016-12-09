# stock-tweets
Looks for a correlation between tweets and stocks.

Uses the Yahoo Finance and Twitter APIs to retrieve stock information and tweets
that were posted within the last week, respectively.
Uses the [GetOldTweets](https://github.com/Jefferson-Henrique/GetOldTweets-python)
project to retrieve tweets that were posted over a week ago.

## Requirements
- Python 3.5.2
- Python 2.7.10 (a dependency for collecting the training set only works in Python 2)

## Install
> pip install -r requirements.txt

## Run
> python index.py

## To Collect Training Set Data
> python index.py --training

## Modification to GetOldTweets-python-master
- Added parentheses to `print` calls
- Added conditional logic check what Python version is in use to import proper `got` module