from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
#client = MongoClient('ds245228.mlab.com',45228)
db = client["twitter-elections"]
#db.authenticate("tw-user","tw123456")
parties = ["Twitter_LeU", "Twitter_M5S", "Twitter_CentroSinistra", "Twitter_CentroDestra"]
max_favorites = {}
max_retweets = {}

for party in parties:
    max_favorites_party = (0,0)
    max_retweets_party = (0,0)

    collection = db[party]
    
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
        tupla_favorites = (favorites[-1],tweet["id_str"])
        if tupla_favorites[0] > max_favorites_party[0]:
            max_favorites_party = tupla_favorites
            
        tupla_retweets = (retweets[-1],tweet["id_str"])
        if tupla_retweets[0] > max_retweets_party[0]:
            max_retweets_party = tupla_retweets
        
        for i in range(len(favorites)):
            favorites_dict[i].append(favorites[i])
        for i in range(len(retweets)):
            retweets_dict[i].append(retweets[i])
    
    max_favorites[party] = max_favorites_party
    max_retweets[party] = max_retweets_party
    #Number of elements in each collection
    number_tweets = collection.count()
    #Average Favorites        
    average_favorites_tweet = [np.mean(favorites_dict[i]) for i in range(len(favorites_dict)) if len(favorites_dict[i]) != 0]
    
    fig = plt.figure()     
    plt.plot(average_favorites_tweet)
    plt.xticks(range(0,len(average_favorites_tweet)), fontsize = 7, rotation = 90)
    plt.xlabel("Hours after first tweet")
    plt.ylabel("Average Favorites")
    plt.title("Average Growth of a"+ party+" (Favorites)")
    fig.savefig(party+ "_favorites" + ".png", dpi=fig.dpi)  
    
    
    #Average Retweets
    average_retweets_tweet = [np.mean(retweets_dict[i]) for i in range(len(retweets_dict)) if len(retweets_dict[i]) != 0]
    
    fig = plt.figure()   
    plt.plot(average_retweets_tweet)
    plt.xticks(range(0,len(average_retweets_tweet)), fontsize = 7, rotation = 90)
    plt.xlabel("Hours after first tweet")
    plt.ylabel("Average Retweets")
    plt.title("Average Retweets"+party+" (Retweets)")
    fig.savefig(party+ "_retweets" + ".png", dpi=fig.dpi)
    
    print(party+" has "+ str(number_tweets) +" tweets") 
    
    
#Plot a given tweet
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
        plt.xticks(range(0,len(favorites)), fontsize = 7, rotation = 90)
        plt.xlabel("Hours after first tweet")
        plt.title(tweet["user"]["screen_name"] + " " + tweet["id_str"])
        fig.savefig(tweet["id_str"] + "_favorites" + ".png", dpi=fig.dpi)
        #plot retweets
        fig = plt.figure()
        retweets = tweet["retweets"]
        plt.plot(retweets)
        plt.xticks(range(0,len(retweets)), fontsize = 7, rotation = 90)
        plt.xlabel("Hours after first tweet")
        plt.ylabel("Retweets")
        plt.title(tweet["user"]["screen_name"] + " " + tweet["id_str"])
        fig.savefig(tweet["id_str"] + "_retweets" + ".png", dpi=fig.dpi)
        break
        
    
    
#Most Popular Tweets (Favorites)
for party in max_favorites:
    tweet_id = max_favorites[party][1]
    collection = db[party]
    tweet = collection.find_one({"id_str": tweet_id})
    print(tweet["text"])
    #plot favorites
    fig = plt.figure()
    favorites = tweet["favorites"]
    plt.plot(favorites)
    plt.xticks(range(0,len(favorites)), fontsize = 7, rotation = 90)
    plt.xlabel("Hours after first tweet")
    plt.title(tweet["user"]["screen_name"] + " " + tweet["id_str"])
    fig.savefig(tweet["id_str"] + "_favorites" + ".png", dpi=fig.dpi)

#Most Popular Tweets (Retweets)
for party in max_retweets:
    tweet_id = max_retweets[party][1]
    collection = db[party]
    tweet = collection.find_one({"id_str": tweet_id})
    print(tweet["text"])
    #plot retweets
    fig = plt.figure()
    retweets = tweet["retweets"]
    plt.plot(retweets)
    plt.xticks(range(0,len(retweets)), fontsize = 7, rotation = 90)
    plt.xlabel("Hours after first tweet")
    plt.ylabel("Retweets")
    plt.title(tweet["user"]["screen_name"] + " " + tweet["id_str"])
    fig.savefig(tweet["id_str"] + "_retweets" + ".png", dpi=fig.dpi)

