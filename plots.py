from pymongo import MongoClient
import time
import numpy as np
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
#client = MongoClient('ds245228.mlab.com',45228)
db = client["twitter-elections"]
#db.authenticate("tw-user","tw123456")
parties = ["Twitter_LeU", "Twitter_M5S", "Twitter_CentroSinistra", "Twitter_CentroDestra"]
for party in parties:
    collection = db[party]
    
    new_time = time.time() - (60*3)*1000*60
    
    
    favorites_dict = {}
    for i in range(50):
        favorites_dict[i] = []
    retweets_dict = {}
    for i in range(50):
        retweets_dict[i] = []
    
    tweet_evolution = collection.find()
    for tweet in tweet_evolution:
        favorites = tweet["favorites"]
        retweets = tweet["retweets"]
        
        for i in range(len(favorites)):
            favorites_dict[i].append(favorites[i])
        for i in range(len(retweets)):
            retweets_dict[i].append(retweets[i])
    
    #Number of elements in each collection
    number_tweets = collection.count()
    #Average Favorites        
    average_favorites_tweet = [np.mean(favorites_dict[i]) for i in range(len(favorites_dict)) if len(favorites_dict[i]) != 0]
    
    fig = plt.figure()     
    plt.plot(average_favorites_tweet)
    plt.xticks(range(0,len(average_favorites_tweet)))
    plt.xlabel("Hours after first tweet")
    plt.ylabel("Average Favorites")
    plt.title("Average Growth of a"+ party+" (Favorites)")
    fig.savefig(party+ "_favorites" + ".png", dpi=fig.dpi)  
    
    
    #Average Retweets
    average_retweets_tweet = [np.mean(retweets_dict[i]) for i in range(len(retweets_dict)) if len(retweets_dict[i]) != 0]
    
    fig = plt.figure()   
    plt.plot(average_retweets_tweet)
    plt.xticks(range(0,len(average_retweets_tweet)))
    plt.xlabel("Hours after first tweet")
    plt.ylabel("Average Retweets")
    plt.title("Average Retweets"+party+" (Retweets)")
    fig.savefig(party+ "_retweets" + ".png", dpi=fig.dpi)
    
    print(party+" has "+ str(number_tweets) +" tweets") 
    
tweet_id = str(input("Insert a Tweet id: "))
for party in parties:
    db.collection = db[party]
    tweet = collection.find_one({"id_str": tweet_id})
    if type(tweet) == dict:
        print(tweet["text"])
        #plot favorites
        fig = plt.figure()
        favorites = tweet["favorites"]
        plt.plot(favorites)
        plt.xticks(range(0,len(favorites)))
        plt.xlabel("Hours after first tweet")
        plt.title(tweet["user"]["screen_name"] + " " + tweet["id_str"])
        fig.savefig(tweet["id_str"] + "_favorites" + ".png", dpi=fig.dpi)
        #plot retweets
        fig = plt.figure()
        retweets = tweet["retweets"]
        plt.plot(retweets)
        plt.xticks(range(0,len(retweets)))
        plt.xlabel("Hours after first tweet")
        plt.ylabel("Retweets")
        plt.title(tweet["user"]["screen_name"] + " " + tweet["id_str"])
        fig.savefig(tweet["id_str"] + "_retweets" + ".png", dpi=fig.dpi)
        break
        