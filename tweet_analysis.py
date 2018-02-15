# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:14:46 2018

@author: Valerio
"""
from pymongo import MongoClient
import tweepy
from tweepy import OAuthHandler
import json
import time

cfg = {
    "consumer_key" :"RquN0zhitB82NARp79NC9xXHb",
    "consumer_secret":"77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8",
    "access_token" :"931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg",
    "access_token_secret" :"04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"}

auth =OAuthHandler(cfg["consumer_key"],cfg["consumer_secret"])
auth.set_access_token(cfg["access_token"],cfg["access_token_secret"])
api = tweepy.API(auth)

def process_or_store(tweet):
    return json.dumps(tweet)


#fare quando il tweet viene inserito nel MOngoDb Renzi
id_tweet_da_analizare = "964119751709675522"

client = MongoClient('localhost', 27017)
db = client['Twitter_Prova']

original = db.Twitter_Renzi.find_one({"id_str" : id_tweet_da_analizare})

tweet_evolution = {"id_str": original["id_str"], "id_user": original["user"]["id_str"], "screen_name": original["user"]["screen_name"], "created_at": original["created_at"], "favorites": [], "retweets": []}
db.tweets.insert_one(tweet_evolution)

#dopo un ora
tweet_evolution = db.tweets.find_one({"id_str" : id_tweet_da_analizare})
db.tweets.delete_one({"id_str" : id_tweet_da_analizare})

while True:
    try:
        tweet = api.get_status(id = int(tweet_evolution["id_str"]))
        tweet = process_or_store(tweet._json)
        json_acceptable_string = tweet.replace("'","/")
        tweet = json.loads(json_acceptable_string)
        break
    except:
        time.sleep(15*60)

tweet_evolution["favorites"].append(tweet["favorite_count"])
tweet_evolution["retweets"].append(tweet["retweet_count"])
db.tweets.insert_one(tweet_evolution)
#e poi per le altre ore