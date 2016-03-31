import twitter
from chain import *
from secret import POST_CONSUMER_KEY, POST_CONSUMER_SECRET, POST_ACCESS_TOKEN, POST_ACCESS_TOKEN_SECRET
api = twitter.Api(consumer_key=POST_CONSUMER_KEY, consumer_secret=POST_CONSUMER_SECRET,
					access_token_key=POST_ACCESS_TOKEN, access_token_secret=POST_ACCESS_TOKEN_SECRET)


m = Markov()
m.load_triples()
m.load_tweets()

if len(m.dict) == 0:
  m.make_words()
  m.populate()
  m.store_triples()

tweet = m.make_tweet()
print '{}\n----'.format(tweet)

status = api.PostUpdate(tweet)
