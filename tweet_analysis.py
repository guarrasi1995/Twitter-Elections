import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import json
import time

client = MongoClient('localhost', 27017)
#client = MongoClient('ds245228.mlab.com',45228)
db = client["twitter-elections"]
#db.authenticate("tw-user","tw123456")

#Davide
#consumer key, consumer secret, access token, access secret.
#ckey="RquN0zhitB82NARp79NC9xXHb"
#csecret="77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8"
#atoken="931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg"
#asecret="04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"

# #Valerio
# #consumer key, consumer secret, access token, access secret.
ckey = "5n8QsFqTsfiaB9aqJJvGm01rn"
csecret = "QoKiYt9fAQkgRSeBMmFOokxBLYpmxJm4VDVLKMooWlPBnE5Jsp"
atoken =  "938705179284819968-3Sv1npwRRqbH2gcFiyAqwkH3gedDJqK"
asecret="62oNP7DxrDjWW1Dhb1Ud6HYEFaDrnJnQ4mt4vJKXI9AnA"

#Ioannis
#consumer key, consumer secret, access token, access secret.
#ckey = "zIC0cpWQ6rRvCLiXyams9Adtp"
#csecret = "t0dHAfHezxtgUb4oEoIYJaDmek92JzJ6y0AyY91hhmvbCQ62lC"
#atoken =  "170767443-uODoE5SlERT0TAzWuBgpJdpPCpIgdW4tmdJqQZNL"
#asecret="JcAg8G46c1AJ0uAvJZS3I0QnAih8OpjpwGJccdZjwFRTa"


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

def process_or_store(tweet):
    return json.dumps(tweet)

parties = ["Twitter_LeU", "Twitter_M5S", "Twitter_CentroSinistra", "Twitter_CentroDestra"]
min_count = 0
max_count = 48

while True:
    for party in parties:
        print(party, "-------------------------")
        collection = db[party]
        for count in range(min_count, max_count):
            print("look-up", count)
            tweet_evolution = collection.find({"last_check": {"$lte": int((time.time() - 60*60) * 1000)},
                                               "check": count,
                                               "deleted": False})
            for tweet in tweet_evolution:
                print(tweet["id_str"])

                delete=False
                while True:
                    try:
                        tweet_new = api.get_status(id=int(tweet["id_str"]))
                        tweet_new = process_or_store(tweet_new._json)
                        json_acceptable_string = tweet_new.replace("'", "/")
                        tweet_new= json.loads(json_acceptable_string)
                        break

                    except Exception as ex:
                        print(ex)
                        if str(ex) == "[{'code': 144, 'message': 'No status found with that ID.'}]":
                            print("tweet was deleted")
                            delete = True
                            break
                        else:
                            print(ex, "sto aspettando 15 minuti perchè twitter mi ha bloccato")
                            time.sleep(15 * 60)

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

    time.sleep(30)
