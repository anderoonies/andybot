import twitter
import string
import pickle
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
					access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)


def fetch():
    data = {}
    tweets = []
    max_id = None
    total = 0
    exclude_words = ['My Top'] # words whose tweets should be excluded
    while True:
      statuses = api.GetUserTimeline(api.GetUser, count=200,
                                     max_id=max_id, include_rts=False,
                                     exclude_replies=True)
      new_count = ignored_count = 0
      for s in statuses:
        if s.id in data:
          ignored_count += 1
        else:
          if not any(word in s.text for word in exclude_words):
            tweets.append(format_tweet(s))
            new_count += 1
      total += new_count
      print "Fetched %d/%d/%d new/old/total." % ( new_count, ignored_count, total)
      if new_count == 0:
        break
      max_id = min([s.id for s in statuses]) - 1

    pickle.dump(tweets, tweet_file)
    return data.values()

def format_tweet(tweet):
  exclude_chars = ['"'] # characters to exclude

  tweet = tweet.text.encode('utf-8').replace('&amp;','&') \
                                    .replace('&lt;','<') \
                                    .replace('&gt;','>')
  tweet = ''.join(ch for ch in tweet if ch not in exclude_chars)
  tweet += '|'
  return tweet

if __name__ == '__main__':
  tweet_file = open('tweets.pickle', 'w')
  fetch()
  tweet_file.close()
