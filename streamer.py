from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json
import pickle

client = MongoClient('localhost', 27017)
#client = MongoClient('ds245228.mlab.com',45228)
#client.drop_database('twitter-elections') #drop database if already exists
db = client["twitter-elections"]
#db.authenticate("tw-user","tw123456")
collection_LeU = db["Twitter_LeU"]
collection_M5S = db["Twitter_M5S"]
collection_CentroSinistra = db["Twitter_CentroSinistra"]
collection_CentroDestra = db["Twitter_CentroDestra"]


class listener(StreamListener):
    def on_data(self, data):
        data = data.replace("'", "")
        json_acceptable_string = data.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        if len(d) != 1 and "retweeted_status" not in d:
            userid = d["user"]["id"]
            
            if str(userid) in LeU :
                d["last_check"] = int(d["timestamp_ms"])
                d["check"] = 0
                d["deleted"] = False
                d["favorites"] = [0]
                d["retweets"] = [0]
                collection_LeU.insert_one(d)
                print("ok", d["user"]["screen_name"], "LeU")
                
            elif str(userid) in M5S:
                d["last_check"] = int(d["timestamp_ms"])
                d["check"] = 0
                d["deleted"] = False
                d["favorites"] = [0]
                d["retweets"] = [0]
                collection_M5S.insert_one(d)
                print("ok", d["user"]["screen_name"], "M5S")
                
            elif str(userid) in Centro_Sinistra:
                d["last_check"] = int(d["timestamp_ms"])
                d["check"] = 0
                d["deleted"] = False
                d["favorites"] = [0]
                d["retweets"] = [0]
                collection_CentroSinistra.insert_one(d)
                print("ok", d["user"]["screen_name"], "Centro Sinistra")
                
            elif str(userid) in Centro_Destra:
                d["last_check"] = int(d["timestamp_ms"])
                d["check"] = 0
                d["deleted"] = False
                d["favorites"] = [0]
                d["retweets"] = [0]
                collection_CentroDestra.insert_one(d)
                print("ok", d["user"]["screen_name"], "Centro Destra")

        return (True)

    def on_error(self, status):
        print(status)

with open("LeU.txt", "rb") as fp:   # Unpickling
    LeU = pickle.load(fp)
with open("M5S.txt", "rb") as fp:   # Unpickling
    M5S = pickle.load(fp)
with open("Centro_Sinistra.txt", "rb") as fp:   # Unpickling
    Centro_Sinistra = pickle.load(fp)
with open("Centro_Destra.txt", "rb") as fp:   # Unpickling
    Centro_Destra = pickle.load(fp)

#LeU = ["931887582190895104","938705179284819968"]

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

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())

twitterStream.filter(follow = LeU + M5S + Centro_Sinistra + Centro_Destra)


#13294452 @pdnetwork
#931887582190895104 @Davide
#938705179284819968 @Valerio
#Matteo Renzi 18762875