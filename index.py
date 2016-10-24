import sys
sys.path.insert(0, 'src')

# from 'src/retrieve' import getTweets
import retrieve

tweets = retrieve.getTweets('iphone')
print(len(tweets))