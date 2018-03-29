#!/usr/bin/env python

import tweepy #https://github.com/tweepy/tweepy

# options
test_mode = False

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
deletion_count = 0
tweets_to_delete = [
:q]
for tweet in tweets_to_delete:
	print "Deleting %d" % (tweet)
	if not test_mode:
		api.destroy_status(tweet)
	deletion_count += 1
print "Deleted %d tweets" % (deletion_count)
