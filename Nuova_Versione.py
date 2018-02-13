# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 18:24:34 2018

@author: user
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json

#Davide
#consumer key, consumer secret, access token, access secret.
ckey="RquN0zhitB82NARp79NC9xXHb"
csecret="77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8"
atoken="931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg"
asecret="04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"

#Valerio
#consumer key, consumer secret, access token, access secret.
#ckey = "5n8QsFqTsfiaB9aqJJvGm01rn"
#csecret = "QoKiYt9fAQkgRSeBMmFOokxBLYpmxJm4VDVLKMooWlPBnE5Jsp"
#atoken =  "938705179284819968-3Sv1npwRRqbH2gcFiyAqwkH3gedDJqK"
#asecret="62oNP7DxrDjWW1Dhb1Ud6HYEFaDrnJnQ4mt4vJKXI9AnA"


client = MongoClient('localhost', 27017)
client.drop_database('TwitterProva') #drop database if already exists
db = client['Twitter_Prova']
collection = db['Twitter_Renzi']

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        data = data.replace("'", "")
        json_acceptable_string = data.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        posts = db.Twitter_Renzi
        posts.insert_one(d)
        print("ok")

        return(True)

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())

twitterStream.filter(follow=["13294452"])
#13294452 @pdnetwork