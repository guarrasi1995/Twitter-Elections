# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 18:24:34 2018

@author: user
"""
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
import time
import heapq
import pickle

#Davide
#consumer key, consumer secret, access token, access secret.
#ckey="RquN0zhitB82NARp79NC9xXHb"
#csecret="77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8"
#atoken="931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg"
#asecret="04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"

#Valerio
#consumer key, consumer secret, access token, access secret.
ckey = "5n8QsFqTsfiaB9aqJJvGm01rn"
csecret = "QoKiYt9fAQkgRSeBMmFOokxBLYpmxJm4VDVLKMooWlPBnE5Jsp"
atoken =  "938705179284819968-3Sv1npwRRqbH2gcFiyAqwkH3gedDJqK"
asecret="62oNP7DxrDjWW1Dhb1Ud6HYEFaDrnJnQ4mt4vJKXI9AnA"


client = MongoClient('localhost', 27017)
#client.drop_database('Twitter_Prova') #drop database if already exists
db = client['Twitter_Prova']
collection = db['Twitter_Davide']
h = []
with open("LeU.txt", "rb") as fp:   # Unpickling
    LeU = pickle.load(fp)

class listener(StreamListener):

    def on_data(self, data):
        try:
            with open("heap.txt", "rb") as fp:   # Unpickling
                h = pickle.load(fp)
        except:
            h = []
        
        data = data.replace("'", "")
        json_acceptable_string = data.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        print(d)
        if len(d) != 1:
            userid = d["user"]["id"]
            
            if str(userid) in LeU and "retweeted_status" not in d:
            #if str(userid) == "938705179284819968" and "retweeted_status" not in d:
                posts = db.Twitter_Renzi
                posts.insert_one(d)
                print("ok")
                
                id_tweet_da_analizare = d["id_str"]
                
                original = db.Twitter_Renzi.find_one({"id_str" : id_tweet_da_analizare})
                
                tweet_evolution = {"id_str": original["id_str"],
                                   "id_user": original["user"]["id_str"],
                                   "screen_name": original["user"]["screen_name"],
                                   "created_at": original["created_at"],
                                   "text": original["text"],
                                   "favorites": [],
                                   "retweets": [],
                                   "last_check": time.time(),
                                   "check" : 0}
                heapq.heappush(h,(tweet_evolution["last_check"],tweet_evolution["id_str"]))
                db.tweets.insert_one(tweet_evolution)
                
                with open("heap.txt", "wb") as fp:   #Pickling
                    pickle.dump(h, fp)
                
        return(True)

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())

twitterStream.filter(follow = LeU)
#twitterStream.filter(follow = ["938705179284819968"])


#13294452 @pdnetwork
#931887582190895104 @Davide
#938705179284819968 @Valerio
#Matteo Renzi 18762875