# -*- coding: utf-8 -*-
"""
This script is forked originally from Dave Jeffery. The original implementation
was very slow and deleted around 2 tweets per second. Making it multithreaded I 
am able to delete 30-50 tweets per second. 
@author: vik-y

----------------------------------------------------------------------------

This script will delete all of the tweets in the specified account.
You may need to hit the "more" button on the bottom of your twitter profile
page every now and then as the script runs, this is due to a bug in twitter.

You will need to get a consumer key and consumer secret token to use this
script, you can do so by registering a twitter application at https://dev.twitter.com/apps

@requirements: Python 2.5+, Tweepy (http://pypi.python.org/pypi/tweepy/1.7.1)
@author: Dave Jeffery
---------------------------------------------------------
"""

import tweepy
import thread

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def deleteThread(api, objectId):
    count = 3
    while count > 0:
        try:
            api.destroy_status(objectId)
            break
        except:
            count -= 1

def deleteFav(api, objectId):
    count = 3
    while count > 0:
        try:
            api.destroy_favorite(objectId)
            break
        except:
            count -= 1
  
def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url) 
    auth.get_access_token(verify_code)
    
    return tweepy.API(auth)

def batch_delete(api):
    print "You are about to Delete all tweets from the account @%s." % api.verify_credentials().screen_name
    print "Does this sound ok? There is no undo! Type yes to carry out this action."
    do_delete = raw_input("> ")
    if do_delete.lower() == 'yes':
        flag = True
        while flag:
            count = 0
            print "Purging favs..."
            for fav in tweepy.Cursor(api.favorites).items():
                try:
                    thread.start_new_thread( deleteFav, (api, fav.id))
                except:
                    count += 1
            print "Purging tweets..."
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    thread.start_new_thread( deleteThread, (api, status.id, ) )
                except:
                    count += 1
            flag = count > 0
    print "The dark deed you have requested is done\n"


if __name__ == "__main__":
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, compression=True, retry_delay=1, retry_count=5)
    print "Authenticated as: %s" % api.me().screen_name
    
    batch_delete(api)
