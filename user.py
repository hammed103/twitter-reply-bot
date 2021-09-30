import tweepy

from time import sleep
import logging
import random
from credentials import *
import schedule



'''consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
access_token = environ['access_token']
access_token_secret = environ['access_token_secret']'''


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#handle without the @
username = 'license2gain ' #if sigle user ('xxxyyyy')

#keywords in lowercase
keywords = ['#roll', 'kanye','dance'] #if single keyword ['xxxxxyyy']





# Twitter bot sleep time settings in seconds. For example SLEEP_TIME = 300 means 5 minutes.
# you can decrease it or increase it as you like.Please,use large delay if you are running bot all the time  so that your account does not get banned.
#how often we reply tweets
SLEEP_TIME = 100

FILE_NAME = 'last_seen.txt'


print("Twitter bot that replies {} if any of the keywords {} are found".format(username,keywords ))



print('Reply Bot Started!')
result = []
# update these for whatever tweet you want to process replies to
def reply():
    count = 0
    print ('New session')
    for tweet in tweepy.Cursor(api.user_timeline,screen_name =username  ,).items():
        try:
            if str(tweet.id) not in open('reply_history.txt', 'r').read().split('\n'):
                if not any(keyword in tweet.text.lower() for keyword in keywords) :
                    continue
                sn = tweet.user.screen_name
                m = "@{} ".format(sn) + random.choice(open('replies.txt').readlines()).strip("\n")
                api.update_status(status=m, in_reply_to_status_id = tweet.id, )
                logger.info("Replying  to tweet by {} with {}".format(sn,m))
                count  += 1
                logger.info("Replied to {} tweet in current session ".format(count))
                open('reply_history.txt', 'a').write(str(tweet.id)+'\n')
                sleep(SLEEP_TIME)
            else:
                continue

        except tweepy.TweepyException as e:
            print(e)

        except StopIteration:
            break
    logger.info(" {} new tweets by {} replied to ".format(count,username))
#Restarts program every x seconds , please make large enough to avoid ban .
# Depends on how often we expect our user to post new content
schedule.every(120).seconds.do(reply)

while True:
    schedule.run_pending()
    sleep(1)
