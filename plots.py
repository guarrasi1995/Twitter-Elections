from pymongo import MongoClient
import time
import numpy as np
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
#client = MongoClient('ds245228.mlab.com',45228)
db = client["twitter-elections"]
#db.authenticate("tw-user","tw123456")
collection = db["Twitter_LeU"]

new_time = time.time() - (60*3)*1000*60


favorites_dict = {}
for i in range(50):
    favorites_dict[i] = []
retweets_dict = {}
for i in range(50):
    retweets_dict[i] = []

tweet_evolution = collection.find()
for tweet in tweet_evolution:
    #plot favorites
    fig = plt.figure()
    favorites = tweet["favorites"]
    plt.plot(favorites)
    plt.xticks(range(0,len(favorites)))
    plt.xlabel("Hours after first tweet")
    plt.ylabel("Favorites")
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
    
    for i in range(len(favorites)):
        favorites_dict[i].append(favorites[i])
    for i in range(len(retweets)):
        retweets_dict[i].append(retweets[i])

#Number of elements in each collection
number_tweets = collection.count()
#Average Favorites        
average_favorites_tweet = [np.mean(favorites_dict[i]) for i in range(len(favorites_dict)) if len(favorites_dict[i]) != 0]
     
plt.plot(average_favorites_tweet)
plt.xticks(range(0,len(average_favorites_tweet)))
plt.xlabel("Hours after first tweet")
plt.ylabel("Average Favorites")
plt.title("Average Growth of a LeU Tweet (Favorites)")
fig.savefig("LeU"+ "_favorites" + ".png", dpi=fig.dpi)  


#Average Retweets
average_retweets_tweet = [np.mean(retweets_dict[i]) for i in range(len(retweets_dict)) if len(retweets_dict[i]) != 0]
   
plt.plot(average_retweets_tweet)
plt.xticks(range(0,len(average_retweets_tweet)))
plt.xlabel("Hours after first tweet")
plt.ylabel("Average Retweets")
plt.title("Average Growth of a LeU Tweet (Retweets)")
fig.savefig("LeU"+ "_retweets" + ".png", dpi=fig.dpi)

print("LeU has "+ str(number_tweets) +" tweets") 