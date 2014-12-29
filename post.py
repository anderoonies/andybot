import twitter
from chain import *
from secret import POST_CONSUMER_KEY, POST_CONSUMER_SECRET, POST_ACCESS_TOKEN, POST_ACCESS_TOKEN_SECRET
api = twitter.Api(consumer_key=POST_CONSUMER_KEY, consumer_secret=POST_CONSUMER_SECRET, 
					access_token_key=POST_ACCESS_TOKEN, access_token_secret=POST_ACCESS_TOKEN_SECRET)


m = Markov('tweets.txt')

tweet = m.make_tweet()
print(tweet)
print '-----'
status = api.PostUpdate(tweet)
# print status

