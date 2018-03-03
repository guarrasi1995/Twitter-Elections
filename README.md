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
3. Relationship between point 1 and 2 

## Code
![cattura](https://user-images.githubusercontent.com/31849276/36729392-4c826f3e-1bc4-11e8-9303-bbb460b6dc7e.PNG)


# Extract data
## First Part

Initially we decided to extract the people followed by the pages of the 4 major coalitions.

For example, the "Centro_Destra" list was created by collecting the ids of the following pages:
"forza_italia" (Forza Italia party), "LegaSalvini" (Lega party), "FratellidItaIia" (Fratelli d'Italia party), "noiconitaliaudc" (Noi con l'Italia party).

    #Centro Destra

    ForzaItalia= []
    for following in limit_handled(tweepy.Cursor(api.friends_ids, id= "forza_italia").items()):
        ForzaItalia.append(following)
        
    LegaNord= []
    for following in limit_handled(tweepy.Cursor(api.friends_ids, id= "LegaSalvini").items()):
        LegaNord.append(following)
        
    FratellidItalia= []
    for following in limit_handled(tweepy.Cursor(api.friends_ids, id="FratellidItaIia").items()):
            FratellidItalia.append(following)
            
    NoiConItalia= []
    for following in limit_handled(tweepy.Cursor(api.friends_ids, id= "noiconitaliaudc").items()):
            NoiConItalia.append(following)

    Centro_Destra = list(set(ForzaItalia + LegaNord + FratellidItalia + NoiConItalia   )) 


We used an Api key, which identifies our twitter app, and defined the "limit_handled" function to prevent "RateLimitError" errors.

    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                time.sleep(15 * 60)
                
However for the individual coalitions we have noticed the presence of characters misleading as Barack Obama or pages as the "Financial Times", to avoid this problem we defined "clean_from_trash" function by identifying surely for each "id" if it is an outlier or a correct page ( ex: for "Centro Destra" we used ["fi", "forza", "lega"]). 

    ##PULIZIA CENTRO DESTRA
    word_dx = ["fi","forza","lega"]
    Centro_Destra,tolti_Centro_Destra = clean_from_trash(Centro_Destra, word_dx)
    print("WE HAVE FINISHED FOR Centro Destra")


After this we decided to enrich our identity lists from the candidates of each party.
In fact, by consulting the site "http://www.ilgiornale.it/news/politica/elezioni-politiche-2018-ecco-tutti-i-candidati-1492269.html" we have taken the csv file related to the list of uninominal candidates for the Chamber of Deputies and for the Senate. 
Certainly we have not forgotten that some of the most important exponents are not candidated (ex: M5S "Beppe Grillo" and "AlessandrodiBattista").
At this point we have defined a third function "trova_candidati", which allowed us to join the list of employees on political pages with profiles of political exponents.

    ##Find Candidates Centro_Destra
    Centro_Destra = find_candidates(candidati_centrodestra, tolti_Centro_Destra, Centro_Destra)


Finally we eliminated further outliers, like "Fiorello", in the "Centro Destra" because they presented in their "screen_name" one of the words considered by us key for the party, in this case "fi".
To save the id lists we used the "pickle" library that allows us to save/extract a file while keeping the python format used.

    Centro_Destra = [str(elem) for elem in Centro_Destra] 
    with open("Centro_Destra.txt", "wb") as fp:   #Pickling
        pickle.dump(Centro_Destra, fp)


# Streaming With Tweepy

To start collecting tweets in real time from all the actors in our political lists we use Tweepy, which makes easier to use the twitter streaming api by handling authentication, connection. API authorization is required to access Twitter streams. 

    cfg = {
    "consumer_key" :"RquN0zhitB82NARp79NC9xXHb",
    "consumer_secret":"77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8",
    "access_token" :"931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg",
    "access_token_secret" :"04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"}

The Twitter streaming API is used to download twitter messages in real time. It is useful for obtaining a high volume of tweets.
The streaming api is quite different from the REST api because the REST api is used to pull data from twitter but the streaming api pushes messages to a persistent session. This allows the streaming api to download more data in real time than could be done using the REST API.

Therefore using the streaming api has three steps.

1. Create a class inheriting from StreamListener
2. Using that class create a Stream object
3. Connect to the Twitter API using the Stream.

## Step 1: Creating a StreamListener
This simple stream listener prints status text. The on_data method of Tweepy’s StreamListener conveniently passes data from statuses to the on_status method. Create class MyStreamListener inheriting from StreamListener and overriding on_status.:
    
    class listener(StreamListener):
        def on_data(self, data):
            data = data.replace("'", "")
            json_acceptable_string = data.replace("'", "\"")
            d = json.loads(json_acceptable_string)
        return (True)

## Step 2: Creating a Stream
 Once we have an api and a status listener we can create our stream object :

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener()) 

## Step 3: Starting a Stream
A number of twitter streams are available through Tweepy. In our code we used filter to stream all tweets made by the ids on the list given as value to follow.

    twitterStream.filter(follow = LeU + M5S + Centro_Sinistra + Centro_Destra)


## Errors 420
When using Twitter’s streaming API one must be careful of the dangers of rate limiting. If we exceed a limited number of attempts to connect to the streaming API in a window of time, we receive error 420. The amount of time a we has to wait after receiving error 420 will increase exponentially each time we make a failed attempt.

# Tweet Updating
After having initialized the mongodb, while the streamer continues to collect new tweets, we run tweet_analysis.py which allows us to collect the interested data of each collected tweet. Always through the relative API we continuosly check every hour (for 48 times = up to 2 days) how many favorites and retweets the tweet has reached. Once the data is collected, we update the database by adding the relative values to the relative voices "favorites" and "retweets".

For each party you enter into its collection. Subsequently, for each Count (the number of hours passed since the publication of the tweet) we collect tweets that satisfy 3 conditions: whether it is an hour after the last update ("last check"), that the check we are doing is in the 48 ("count") and that the tweet is not it has been eliminated before 48 hours ("deleted").
    
    while True:
    for party in parties:
        print(party, "-------------------------")
        collection = db[party]
        for count in range(min_count, max_count):
            print("look-up", count)
            tweet_evolution = collection.find({"last_check": {"$lte": int((time.time() - 60*60) * 1000)},
                                               "check": count,
                                               "deleted": False})

Later, through the ID of the tweet, let's see on twitter the variations of favorites and retweets.
However, there could be two types of errors: the tweet was deleted or Twitter blocked us. To avoid the block of the code, we resolved these exceptions in this way:

     except Exception as ex:
        print(ex)
        if str(ex) == "[{'code': 144, 'message': 'No status found with that ID.'}]":
            print("tweet was deleted")
            delete = True
            break
        else:
            print(ex, "sto aspettando 15 minuti perchè twitter mi ha bloccato")
            time.sleep(15 * 60)
                            
Every time before updating the database on MongoDB you have to check if the tweet has been deleted or not. If you verify that the tweet has been deleted, change the key "deleted" to True.

    if not delete:
        print("trovato")
        tweet["favorites"].append(tweet_new["favorite_count"])
        tweet["retweets"].append(tweet_new["retweet_count"])
        tweet["last_check"] = int(time.time() * 1000)
        tweet["check"] = count + 1
        collection.save(tweet)
    else:
        tweet["deleted"] = True
        tweet["last_check"] = int(time.time() * 1000)
        tweet["check"] = count + 1
        collection.save(tweet)

# Statistics

From the data collection, the number of reference profiles for each party are:

![media8](https://user-images.githubusercontent.com/31849300/36934242-ec8a8aa0-1ee6-11e8-92d8-92c0b9f272ac.PNG)

As we can see, Centro Sinistra and Centro Destra, being the largest parties, have a total of 73% of the pages considered.
In the 8 days before the elections we have collected a total of ___ tweets. Here we can see how they are distributed among the various parties:
# ![media7](https://user-images.githubusercontent.com/31849300/36934241-ec6ceb58-1ee6-11e8-9c90-77f50ffaeca7.PNG)
We can see that the party that is most active on the social network is ___ , although it is not the one with the largest number of reference profiles.

## Plots
In this part we want to exploit the collected data to make statistical analyzes on the growth of favorites and retweets over a period of 48 hours. So we decided to represent 3 types of plots:
1. for each party the average growth of favorites and retweets
2. given an input tweet, the growth of favorites and retweets
3. for each party the most popular tweet based on favorites and retweets
4. see how many tweets are published by every party in each day
5. see if there is a pattern in witch part of the day ai party publishes its tweets

For the first type, for each party we collected favorites and retweets for every hour saving them in a dictionary with key = the relative hour and for value = the list of number of favorites or retweets at that hour. Then we made a mean of these lists and then plotted them:

![media1](https://user-images.githubusercontent.com/31849300/36934253-ef1c01a4-1ee6-11e8-95a7-06d2118a590d.PNG)
![media2](https://user-images.githubusercontent.com/31849300/36934236-ebc51d2e-1ee6-11e8-9372-da3192647c80.PNG)

On the x axis we have the number of hours passed and on the y axis the average number of favorites reached or retweets achieved.

We can see that M5S is the party that reaches the average maximum number of favorites and also for the maximum average number of retweets. It can be noted that the highest growth rate is between 0 hours and 11 hours after the creation of the tweet. Instead from 27 hours from the creation onwards, growth is no longer so dominant. This makes us understand that a tweet is lost in the web after 2 days or at most grows in favorites and retweets of some units. From these graphs we can deduce that the party that collects the most success in the Twitter world is M5S .

But these averages could be altered by tweets that have had little success on the web, especially from political profiles that have few followers. By doing a cleanup of these tweets, putting a minimum threshold of favorites and retweets equal to 5, we get the following plots:

![media3](https://user-images.githubusercontent.com/31849300/36934237-ebe438c6-1ee6-11e8-9a13-95a5918818e6.PNG)
![media4](https://user-images.githubusercontent.com/31849300/36934238-ec01c3be-1ee6-11e8-9048-20e9201c61e6.PNG)

We can rightly see that the average trend reaches higher levels and decreases the gap from the first analysis.


For the second type, we ask the user to enter the ID of a desired tweet. It is searched in the database and if it is found its growth of favorites and retweets of every hour is plotted.

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
           
For example for the tweet with id = 968396173479481344 we have:

![quinto](https://user-images.githubusercontent.com/31849300/36874562-a93a7494-1dac-11e8-8df6-c1ee2bd8055a.PNG)
![sesto](https://user-images.githubusercontent.com/31849300/36874563-a96a9fac-1dac-11e8-88d0-6aa171240dd8.PNG)

On the x axis we have the number of hours passed and on the y axis the number of favorites reached or retweets achieved.

For the third type, we represent the same type of plot of the second type, but here we predict the tweet for each party with more favorites or with more retweets.

# ![media5](https://user-images.githubusercontent.com/31849300/36934239-ec331d24-1ee6-11e8-93ae-adb5beb79379.PNG)
# ![media6](https://user-images.githubusercontent.com/31849300/36934240-ec508d96-1ee6-11e8-9a6c-82a232df87fd.PNG)

On the x axis we have the number of hours passed and on the y axis the number of favorites reached or retweets achieved.
We can see that  ___ is the party that has the tweet that is the most successful for the favorites and ___ is the party that has the tweet that is the most successful for retweets. Observing the most clicked tweets, however, you can not deduce anything concrete even if (or since) before M5S was the party that media would have won the election. But we can see that, for all the parties, the tweet that has the most favorites is also the tweet with the most retweets. So we can say that as the favorites grow, also the retweets grow.

For the fourth type, we wanted to show how many tweets each party got published every day. We would like to see if the parties followed the same strategy on the amount of tweets to be published in the days around the elections.

# ![media9](https://user-images.githubusercontent.com/31849300/36934243-ed98367c-1ee6-11e8-8541-e741d298af55.PNG)

On the x axis we have the days in which the tweets were pubblished and on the y axis the number of tweets published.
We can see that proportionally, all the parties follow the same trend for how many tweets they publish from a day to another. We can see in the days that we analysed the number of tweets increase and decrease alternatively. The 3rd of March there should be electoral silence, we can see that it was(n't) ___  respected.

For the fifth type, we wanted to see if there was a particular pattern in posting tweets from parties in particular hours. Here we can see for every hour of the day how many tweets in total have been posted by each party.

# ![media10](https://user-images.githubusercontent.com/31849300/36934244-edb6e676-1ee6-11e8-9b7c-65a76d6fcc16.PNG)

On the x axis we have the hours of the day in which the tweets were pubblished and on the y axis the number of tweets published from each party.
We can see that the most of the tweets are published from 10 a.m. up to 8 p.m.
It would be interesting to see if the success of a tweet depends on which hour of the day it was posted or even on the day it was posted on.

# Text Analysis
In the second point of the statistical analysis we observe the words used in the tweets.
We have defined the normalise function, which allows us to eliminate the stopwords, to do the stemming and to normalize the words that we retrieve from the MongoDb through the query:

    parties = ["Twitter_LeU", "Twitter_M5S", "Twitter_CentroSinistra", "Twitter_CentroDestra"]

    for party in parties:
        collection = db[party]
        #Create the empy dictionary about occurrences for each parties 
        diz_occ = {}
        tweet_evolution = collection.find ()
            for tweet in tweet_evolution:
                for elem in normalise(tweet ["text"]):
                    if elem in diz_occ:
                        diz_occ[elem] += 1
                    else:
                        diz_occ[elem] = 1
                    
        Most_used = dict(Counter(diz_occ).most_common())
    
At this point for each party we have created the dictionary in which we identify the words used most frequently. 
Using "Most_used" dictionary we drew three types of graph:

#### Histogram.1
When plotting the histogram, we look at the first 20 most used words, highlighting the most present word in green.

![l1](https://user-images.githubusercontent.com/31849276/36913007-dae568d6-1e48-11e8-9851-70099c7781aa.PNG)
![m1](https://user-images.githubusercontent.com/31849276/36913015-dbaeb43e-1e48-11e8-8c65-1b85d2c49214.PNG)
![s1](https://user-images.githubusercontent.com/31849276/36913134-3e3a4082-1e49-11e8-85ed-7a1d7e6788ff.PNG)
![d1](https://user-images.githubusercontent.com/31849276/36913003-da89190a-1e48-11e8-995f-4c8aa65de3c2.PNG)

#### WordCloud.2
In the first type of wordcloud we use all the words in the tweets of a party to get a general overview of the issues addressed and more recurring.  

    WordCloud of "Liberi e Uguali"
                                        
![l2](https://user-images.githubusercontent.com/31849276/36913008-daffc8ac-1e48-11e8-9675-d212118aa11f.PNG)

    WordCloud of "Movimento 5 Stelle"
                                        
![m2](https://user-images.githubusercontent.com/31849276/36913016-dbc8f6dc-1e48-11e8-8d13-f226fd7aef37.PNG)

    WordCloud of "Centro Sinistra"
                                        
![s2](https://user-images.githubusercontent.com/31849276/36913001-da4e9b40-1e48-11e8-84e9-cf38a508897c.PNG)

    WordCloud of "Centro Destra"
                                        
![d2](https://user-images.githubusercontent.com/31849276/36913005-dab0b5a0-1e48-11e8-8852-7f4234f2b619.PNG)

#### WordCloud with shape.3
In the last plot we decided to recreate the wordcloud, personalizing it for each party, filling the acronym of the strongest component for each coalition. We identified Centro Destra as "FI", Centro Sinistra as "PD", Movimento 5 Stelle as "M5S" and Liberi e Uguali as "Leu".

![l3](https://user-images.githubusercontent.com/31849276/36913009-db19840e-1e48-11e8-93db-17cbc733ddcd.PNG)
![m3](https://user-images.githubusercontent.com/31849276/36913000-da27d212-1e48-11e8-9905-70298f153a7f.PNG)
![s3](https://user-images.githubusercontent.com/31849276/36913002-da6d6192-1e48-11e8-9fa3-478411b32e2a.PNG)
![d3](https://user-images.githubusercontent.com/31849276/36913006-dacb6c10-1e48-11e8-8dbd-21cb6596a542.PNG)

# Themes Growth

Observing the main themes, used by the various parties in their tweets, we notice the growth in favorites and retweets of tweets that speak of the five hottest topics of the electoral campaign. This analysis is the combination of previous graphs with WordCloud. (Remember that the analysis is based on the last eight days of the election campaign). The chosen themes are:
- Work
- Future
- EUR
- Italy
- Immigration

For each party we have chosen as reference point the 3 major exponents:
- LeU = Pietro Grasso, Laura Boldrini, Roberto Speranza 
- Centro_Destra = Matteo Salvini, Giorgia Meloni, Silvio Berlusconi 
- M5s = Luigi Di Maio, Alessandro Di Battista, Beppe Grillo 
- Centro_Sinistra = Matteo Renzi, Paolo Gentiloni, Carlo Calenda 

For each theme, we choose the most viral tweets, from the point of view of favorites and retweets, showing their performance over a 48 hour period.

![media11](https://user-images.githubusercontent.com/31849300/36934245-ede9fe44-1ee6-11e8-9bf2-c89e8cedf547.PNG)
![media12](https://user-images.githubusercontent.com/31849300/36934246-ee0c60f6-1ee6-11e8-9239-cc6ffcbaa0c1.PNG)
![media13](https://user-images.githubusercontent.com/31849300/36934247-ee3dc3d0-1ee6-11e8-8862-8a83936a5d88.PNG)
![media14](https://user-images.githubusercontent.com/31849300/36934248-ee60e86a-1ee6-11e8-904e-fb543efdd312.PNG)
![media15](https://user-images.githubusercontent.com/31849300/36934249-ee7f124a-1ee6-11e8-8e77-252760dd50d4.PNG)
![media16](https://user-images.githubusercontent.com/31849300/36934250-eea7e030-1ee6-11e8-8883-e35864e923bb.PNG)
![media18](https://user-images.githubusercontent.com/31849300/36934251-eec9a922-1ee6-11e8-9d97-94fd7de0fe37.PNG)
![media19](https://user-images.githubusercontent.com/31849300/36934252-eefc0bba-1ee6-11e8-979d-215db0c32151.PNG)

To conclude, we note that all parties receive more attention (Favorites and Retweets) when they offend and criticize their rivals rather than in exposing their ideas and innovations. In general, hatred and insult are the primary tools for the dissemination of their tweets.

Twitter analysis has strengths and weaknesses. Twitter users are not representative of the wider public. Twitter users tend to be highly
motivated, younger than average and are likely more often men when engaged in political debate. So any insights are partial. That said, Twitter can be a reflection of spontaneous, motivated behaviour. Analysing Twitter narratives helps us to see where those
highly motivated individuals position themselves in relation to the debate.
