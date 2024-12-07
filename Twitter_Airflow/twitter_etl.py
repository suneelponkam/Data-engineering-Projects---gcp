import tweepy 
import pandas as pd 
import json
from datetime import datetime

def run_twitter_etl():

    access_key = "GH4YESOXsrmuSQMnxP2vxxv9w" 
    access_secret = "lA736blDRM27n2fyIBZWJtAlybtWhX0c4EC4e6KSaZMh3KLNwr" 
    consumer_key = "1675874167076405249-7ji0adRyWiFA2SEyYal0fJEkrwsu0T"
    consumer_secret = "m85XDOfNpOF0fEcb5xTI4Hsx6EYWFXEScDBHeVh0CmXXt"


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=2,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
    )
    print(tweets)