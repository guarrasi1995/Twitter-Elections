# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 18:24:34 2018

@author: user
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import time


#consumer key, consumer secret, access token, access secret.
ckey="RquN0zhitB82NARp79NC9xXHb"
csecret="77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8"
atoken="931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg"
asecret="04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"


connection = MongoClient('localhost', 27017)
#connection.drop_database('TwitterProva') #drop database if already exists
db = connection["TwitterProva"]
#creation or re-creation of the database called HW3ADM

class listener(StreamListener):

    def on_data(self, data):
        try:
            print(data)
            saveFile = open("tweetDB.csv","a")
            saveFile.write(data)
            saveFile.write("\n")
            saveFile.close()
            return(True)
        except BaseException:
            print("failed on data")
            time.sleep(5)

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())

twitterStream.filter(follow=["13294452"])