# ![twitter-json-examples](https://user-images.githubusercontent.com/31849276/36726614-b31538a8-1bba-11e8-9f3e-0a6d597a47aa.png)
# Twitter-Elections

The general election of Sunday 4 March 2018 is approaching, to renew the Chamber of Deputies and the Senate of the Republic. This year the Italians will go to the polls with the new electoral law, the 'Rosatellum'.

The 4 main parties that will take to the field can be classified as follows:
### Centrodestra
- Forza Italia lead by Silvio Berlusconi
- Lega lead by Matteo Salvini
- Fratelli d’Italia lead by Giorgia Meloni
- Noi con l’Italia lead by Raffaele Fitto
- Energie per l’Italia lead by Stefano Parisi
- Udeur lead by Clemente Mastella

### Centrosinistra
- Partito Democratico lead by Matteo Renzi
- Civica Popolare lead by Beatrice Lorenzin
- Lista + Europa lead by Emma Bonino

### Sinistra
- Liberi e Uguali lead by Pietro Grasso

### Other political formations
- Movimento 5 Stelle guidato da Luigi Di Maio

We want to collect the tweets related to each party and then perform different statistical analyzes:
1. Tweet Spread: observing the growth of favorites and retweets.
2. Most Used Words
3. Ratio between point 1 and 2 :question: :question: :question:

## Code
![cattura](https://user-images.githubusercontent.com/31849276/36729392-4c826f3e-1bc4-11e8-9303-bbb460b6dc7e.PNG)


# Extract data
## First Part

Initially we decided to extract the people followed by the pages of the 4 major coalitions.

For example, the "Centro_Destra" list was created by collecting the ids of the following pages:
"forza_italia" (Forza Italia party), "LegaSalvini" (Lega party), "FratellidItaIia" (Fratelli d'Italia party), "noiconitaliaudc" (Noi con l'Italia party).

We used an Api key, which identifies our twitter app, and defined the "limit_handled" function to prevent "RateLimitError" errors.
However for the individual coalitions we have noticed the presence of characters misleading as Barack Obama or pages as the "Financial Times", to avoid this problem we defined "clean_from_trash" function by identifying surely for each "id" if it is an outlier or a correct page ( ex: for "Centro Destra" we used ["fi", "forza", "lega"]). After this we decided to enrich our identity lists from the candidates of each party. 
In fact, by consulting the site "http://www.ilgiornale.it/news/politica/elezioni-politiche-2018-ecco-tutti-i-candidati-1492269.html" we have taken the csv file related to the list of uninominal candidates for the Chamber of Deputies and for the Senate. Certainly we have not forgotten that some of the most important exponents are not candidated (ex: M5S "Beppe Grillo" and "AlessandrodiBattista").
At this point we have defined a third function "trova_candidati", which allowed us to join the list of employees on political pages with profiles of political exponents.
Finally we eliminated further outliers, like "Fiorello", in the "Centro Destra" because they presented in their "screen_name" one of the words considered by us key for the party, in this case "fi".
To save the id lists we used the "pickle" library that allows us to save/extract a file while keeping the python format used.

# Streaming With Tweepy

To start collecting tweets in real time from all the actors in our political lists we use Tweepy, which makes easier to use the twitter streaming api by handling authentication, connection. API authorization is required to access Twitter streams. 

The Twitter streaming API is used to download twitter messages in real time. It is useful for obtaining a high volume of tweets.
The streaming api is quite different from the REST api because the REST api is used to pull data from twitter but the streaming api pushes messages to a persistent session. This allows the streaming api to download more data in real time than could be done using the REST API.

In Tweepy, an instance of tweepy.Stream establishes a streaming session and routes messages to StreamListener instance. The on_data method of a stream listener receives all messages and calls functions according to the message type. The default StreamListener can classify most common twitter messages and routes them to appropriately named methods, but these methods are only stubs.

Therefore using the streaming api has three steps.

A. Create a class inheriting from StreamListener
B. Using that class create a Stream object
C. Connect to the Twitter API using the Stream.

## Step 1: Creating a StreamListener
This simple stream listener prints status text. The on_data method of Tweepy’s StreamListener conveniently passes data from statuses to the on_status method. Create class MyStreamListener inheriting from StreamListener and overriding on_status.:

import tweepy
#override tweepy.StreamListener to add logic to on_status
(foto del codice
class listener(StreamListener):

    def on_status(self, status):
        print(status.text)
)
## Step 2: Creating a Stream
 Once we have an api and a status listener we can create our stream object :

(foto del codice
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener()) 
)

## Step 3: Starting a Stream
A number of twitter streams are available through Tweepy. In our code we used filter to stream all tweets made by the ids on the list given as value to follow.

(foto del codice twitterStream.filter(follow = LeU + M5S + Centro_Sinistra + Centro_Destra))



## Handling Errors
When using Twitter’s streaming API one must be careful of the dangers of rate limiting. If we exceed a limited number of attempts to connect to the streaming API in a window of time, we receive error 420. The amount of time a we has to wait after receiving error 420 will increase exponentially each time we make a failed attempt.

# Text Analysis
In the second point of the statistical analysis we observe the words used in the tweets.
We have defined the normalise function, which allows us to eliminate the stopwords, to do the stemming and to normalize the words that we retrieve from the MongoDb through the query:

"tweet_evolution = collection.find ()
    #print (tweet_evolution)
    for tweet in tweet_evolution:
        #print (tweet)
        for elem in normalise (tweet ["text"]):
    "foto codice

At this point for each party we can create the dictionary in which we identify the words used most frequently. 
Once you get the dictionary "Most_used" we can draw three types of graph:

#### Histogram
When plotting the histogram, we look at the first 20 most used words, highlighting the most present word in green.

#### WordCloud
In the first type of wordcloud we use all the words in the tweets of a party to get a general overview of the issues addressed and more recurring

![cattura](file:///C:/Users/user/Desktop/Twitter-Elections/First_PLOT_Twitter_LeU.png)

#### WordCloud with shape
In the last plot we decided to recreate the wordcloud, personalizing it for each party, filling the acronym of the strongest component for each coalition. We identified Centro Destra as "FI", Centro Sinistra as "PD", Movimento 5 Stelle as "M5S" and Liberi e Uguali as "Leu".
