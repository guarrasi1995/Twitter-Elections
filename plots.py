from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import pickle

client = MongoClient('localhost', 27017)
#client = MongoClient('ds245228.mlab.com',45228)
db = client["twitter-elections"]
#db.authenticate("tw-user","tw123456")
parties = ["Twitter_LeU", "Twitter_M5S", "Twitter_CentroSinistra", "Twitter_CentroDestra"]
color = ["red","orange","green","blue"]
partiti = ["LeU", "M5S", "Centro Sinistra", "Centro Destra"]
max_favorites = {}
max_retweets = {}
r=0
secondo = []

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
    if r == 0:
        fig = plt.figure()
    plt.plot(average_favorites_tweet,color=color[r],linewidth= 4.0, label = partiti[r])
   
    #Average Retweets
    secondo.append([np.mean(retweets_dict[i]) for i in range(len(retweets_dict)) if len(retweets_dict[i]) != 0])
    
    #plt.plot(average_retweets_tweet)
    r += 1
    
#Average Favorites      
plt.xticks(range(0,len(average_favorites_tweet)), fontsize = 7, rotation = 90)
plt.xlabel("Hours after first tweet")
plt.ylabel("Average Favorites")
plt.title("Average Growth of Favorites ")
ax = plt.subplot()
ax.xaxis.get_children()[1].set_size(100)
for label in ax.xaxis.get_ticklabels()[::2]:  
    label.set_visible(False) 
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig.savefig("Average_favorites" + ".png", dpi=300)    
plt.show()

#Average Retweets
fig = plt.figure()
for i in range(len(secondo)):
    plt.plot(secondo[i],color=color[i],linewidth= 4.0, label = partiti[i])
plt.xticks(range(0,len(secondo[0])), fontsize = 7, rotation = 90)
plt.xlabel("Hours after first tweet")
plt.ylabel("Average Retweets")
plt.title("Average Growth of Retweets")
ax = plt.subplot()
ax.xaxis.get_children()[1].set_size(100)
for label in ax.xaxis.get_ticklabels()[::2]:  
    label.set_visible(False) 
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig.savefig("Average_retweets" + ".png", dpi=300)
plt.show()
    
    
#Plot a given tweet
tweet_id = str(input("Insert a Tweet id: "))
for party in parties:
    collection = db[party]
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
fig = plt.figure()
r = 0
for party in max_favorites:
    tweet_id = max_favorites[party][1]
    collection = db[party]
    tweet = collection.find_one({"id_str": tweet_id})
    print(tweet["text"], "\n")
    #plot favorites
    favorites = tweet["favorites"]
    plt.plot(favorites, color=color[r],linewidth= 4.0, label = tweet["user"]["screen_name"] + " " + tweet["id_str"])
    r += 1
plt.xticks(range(0,len(favorites)), fontsize = 7, rotation = 90)
plt.xlabel("Hours after first tweet")
plt.ylabel("Favorites")
plt.title("The Favorited Tweets")
for label in ax.xaxis.get_ticklabels()[::2]:  
    label.set_visible(False)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig.savefig("Popular_favorites" + ".png", dpi=300)
plt.show()

#Most Popular Tweets (Retweets)
fig = plt.figure()
r = 0
for party in max_retweets:
    tweet_id = max_retweets[party][1]
    collection = db[party]
    tweet = collection.find_one({"id_str": tweet_id})
    print(tweet["text"], "\n")
    #plot retweets
    retweets = tweet["retweets"]
    plt.plot(retweets, color=color[r],linewidth= 4.0, label = tweet["user"]["screen_name"] + " " + tweet["id_str"])
    r += 1
plt.xticks(range(0,len(retweets)), fontsize = 7, rotation = 90)
plt.xlabel("Hours after first tweet")
plt.ylabel("Retweets")
plt.title("The Most Retweeted Tweets")
for label in ax.xaxis.get_ticklabels()[::2]:  
    label.set_visible(False)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig.savefig("Popular_retweets" + ".png", dpi=300)
plt.show()


# Pie Charts
#Number of Tweets for each Party
values = []
labels = []
r = 0
for party in parties:
    collection = db[party]
    values.append(collection.count())    
    labels.append((partiti[r]+" ("+ str(values[r]))+")") 
    r += 1
    
plt.pie(values, labels=labels, wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white' }, colors = color)

# add a circle at the center
my_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
 
plt.show()

#Number Profiles for each Party
parties_profiles = []
with open("LeU.txt", "rb") as fp:   # Unpickling
    parties_profiles.append(pickle.load(fp))
with open("M5S.txt", "rb") as fp:   # Unpickling
    parties_profiles.append(pickle.load(fp))
with open("Centro_Sinistra.txt", "rb") as fp:   # Unpickling
    parties_profiles.append(pickle.load(fp))
with open("Centro_Destra.txt", "rb") as fp:   # Unpickling
    parties_profiles.append(pickle.load(fp))

values = []
labels = []
r = 0
for party in partiti:
    values.append(len(parties_profiles[r]))    
    labels.append((party+" ("+ str(values[r]))+")") 
    r += 1
    
plt.pie(values, labels=labels, wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white' }, colors = color)

# add a circle at the center
my_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
 
plt.show()


# Time Plots
