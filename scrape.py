import twitter
import string
from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, 
					access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

tweet_file = open('tweets.txt', 'w')

def fetch():
    data = {}
    max_id = None
    total = 0
    while True:
        exclude = ['"',',','.',"'",'!',]
        statuses = api.GetUserTimeline(api.GetUser, count=200, max_id=max_id, include_rts=False, exclude_replies=True)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                if not s.text.startswith('My Top'):
                    tweet_file.write('>')
                    s = s.text.encode('utf-8').lower()
                    s = ''.join(ch for ch in s if ch not in exclude)
                    tweet_file.write(s)
                    tweet_file.write('|\n')
                newCount += 1
        total += newCount
        print "Fetched %d/%d/%d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()

fetch()

tweet_file.close()