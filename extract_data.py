# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:28:25 2018

@author: user
"""

### Twitter_Forecasting

import tweepy
from tweepy import OAuthHandler
import ast
import json
import time
import operator
import csv
import pickle

#Davide
cfg = {
    "consumer_key" :"RquN0zhitB82NARp79NC9xXHb",
    "consumer_secret":"77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8",
    "access_token" :"931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg",
    "access_token_secret" :"04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"}

#Valerio
cfg = {
    "consumer_key" :"5n8QsFqTsfiaB9aqJJvGm01rn",
    "consumer_secret":"QoKiYt9fAQkgRSeBMmFOokxBLYpmxJm4VDVLKMooWlPBnE5Jsp",
    "access_token" :"938705179284819968-3Sv1npwRRqbH2gcFiyAqwkH3gedDJqK",
    "access_token_secret" :"62oNP7DxrDjWW1Dhb1Ud6HYEFaDrnJnQ4mt4vJKXI9AnA"}

auth =OAuthHandler(cfg["consumer_key"],cfg["consumer_secret"])
auth.set_access_token(cfg["access_token"],cfg["access_token_secret"])
api = tweepy.API(auth)

##EXTRACTING PAGES CONNECTED WITH SOME POLITIC PARTIES

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

##Centro Sinistra
           
PD = []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id="pdnetwork").items()):
        PD.append(following)
        
Civicapopolare = []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id="civica_popolare").items()):
        Civicapopolare.append(following)
        
PSI = []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id="PartSocialista").items()):
        PSI.append(following)

Verdi = []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id="verditalia").items()):
        PD.append(following)
        
Insieme = []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id="insieme2018").items()):
        Insieme.append(following)


Centro_Sinistra = list(set(PD + Civicapopolare + PSI + Verdi + Insieme ))


##M5S

M5S = []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id="Mov5Stelle").items()):
        M5S.append(following)
        
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

#LEU

LeU= []
for following in limit_handled(tweepy.Cursor(api.friends_ids, id= "liberi_uguali").items()):
        LeU.append(following) 
        

def clean_from_trash(partito, words):
    togliere = []
    for i in partito:
        prova = True
        while prova == True:
            try:
                screen_name = (api.get_user(i).screen_name).lower()
                prova = False
            except:
                print("I'm waiting for ", i )
                time.sleep(15 * 60)
        boole = False
        for elem in words :
            if elem in screen_name :
                    boole = True
        if boole == False:
            togliere.append(i)
    #remove useless profiles        
    for e in togliere:
        partito.remove(e)
    return partito,togliere

##PULIZIA M5S
word_5s = ["5","stelle"]
M5S,tolti_M5S = clean_from_trash(M5S, word_5s)
print("WE HAVE FINISHED FOR M5S")

##PULIZIA CENTRO DESTRA
word_dx = ["fi","forza","lega"]
Centro_Destra,tolti_Centro_Destra = clean_from_trash(Centro_Destra, word_dx)
print("WE HAVE FINISHED FOR Centro Destra")

##PULIZIA CENTRO SINISTRA
word_sx = ["pd","popolare","radical","insieme","europa","psi","democratico"]
Centro_Sinistra, tolti_Centro_Sinistra = clean_from_trash(Centro_Sinistra, word_sx)
print("WE HAVE FINISHED FOR Centro Sinistra")

##PULIZIA LEU
word_leu = ["si","anpi","possibile","liberi"]
LeU,tolti_LeU = clean_from_trash(LeU, word_leu)
print("WE HAVE FINISHED FOR LeU")



## GET CANDIDATES

#import file
f1 = open("WCamUni.csv")
dataset_WCamUni = []

for row in csv.reader(f1, delimiter=';'):
    dataset_WCamUni.append(row)
#remove the header
dataset_WCamUni.remove(dataset_WCamUni[0])

#find the lists
liste = {}
for candidato in dataset_WCamUni:
    partito = candidato[0]
    if partito not in liste:
        liste[partito] = [candidato[5]]
    else:
        liste[partito].append(candidato[5])
        
        
f2 = open("WSenUni.csv")
dataset_WSenUni = []

for row in csv.reader(f2, delimiter=';'):
    dataset_WSenUni.append(row)
#remove the header
dataset_WSenUni.remove(dataset_WSenUni[0])

#find the lists
for candidato in dataset_WSenUni:
    partito = candidato[0]
    if partito not in liste:
        liste[partito] = [candidato[5]]
    else:
        liste[partito].append(candidato[5])


# coalitions
candidati_centrosinistra = liste["PARTITO DEMOCRATICO"] + liste[" +EUROPA"] + liste["CIVICA POPOLARE LORENZIN"] +liste["ITALIA EUROPA INSIEME"]
candidati_centrosinistra = list(set(candidati_centrosinistra))

candidati_movimento5stelle = liste["MOVIMENTO 5 STELLE"]
candidati_movimento5stelle = list(set(candidati_movimento5stelle))

candidati_centrodestra = liste["FORZA ITALIA"] + liste["LEGA"] + liste["FRATELLI D'ITALIA CON GIORGIA MELONI"] + liste["NOI CON L'ITALIA - UDC"] 
candidati_centrodestra = list(set(candidati_centrodestra))
        
candidati_leu = liste["LIBERI E UGUALI"]        
candidati_leu = list(set(candidati_leu))  

candidati = {"candidati_centrosinistra" : candidati_centrosinistra,
             "candidati_movimento5stelle" : candidati_movimento5stelle,
             "candidati_centrodestra" : candidati_centrodestra,
             "candidati_leu" : candidati_leu}

#invert name with surname
for l in candidati.values():
    for i in range(len(l)):
        l[i] = l[i].lower()
        name = l[i].split()
        if len(name) == 2:
            new = name[1] + " " + name[0]
            l[i] = new
        elif len(name) == 3 and name[0][0] == "d":
            new = name[2] + " " + name[0] + " " + name[1]
            l[i] = new

#important people not considered
candidati_centrosinistra.append("pier carlo padoan")
candidati_centrosinistra.append("paolo gentiloni")
candidati_centrosinistra.append("pierferdinandocasini")
candidati_centrosinistra.append("maria elena boschi")
candidati_centrodestra.append("michela v. brambilla")
candidati_centrodestra.append("silvio berlusconi")
candidati_leu.append("pier luigi bersani")
candidati_movimento5stelle.append("beppe grillo")
candidati_movimento5stelle.append("alessandrodibattista")



def process_or_store(tweet):
    return json.dumps(tweet)


def find_candidates(candidati, tolti, partito):
    for iden in tolti:
        while True:
            try:
                s = api.get_user(id = iden)
                s = process_or_store(s._json)
                json_acceptable_string = s.replace("'","/")
                d = json.loads(json_acceptable_string)
                candidate = d['name'].lower()
                break
            except :
                print("Bloccati")
                time.sleep(15 * 60)
        if candidate in candidati:
            partito.append(iden)
    return partito

##Find Candidates LeU
LeU = find_candidates(candidati_leu, tolti_LeU, LeU)

##Find Candidates M5S
M5S = find_candidates(candidati_movimento5stelle, tolti_M5S, M5S)

##Find Candidates Centro_Sinistra
Centro_Sinistra = find_candidates(candidati_centrosinistra, tolti_Centro_Sinistra, Centro_Sinistra)

##Find Candidates Centro_Destra
Centro_Destra = find_candidates(candidati_centrodestra, tolti_Centro_Destra, Centro_Destra)

#Remove outliers from CentroDestra (ex:FinancialTimes,Fiorello,ecc.) 
elementi_da_rimuovere_Destra = [538147915,4898091,3062021416,565410552,1364383692,93962722,702661167,
                         38175511,29963394,404045211,3062021416,98609050,32359921,36030252,37948201]
for elem in elementi_da_rimuovere_Destra:
    Centro_Destra.remove(elem)

#Add elements to M5S :
elementi_da_aggiungere_M5S =[398611235, 21330469, 708276706, 19422447, 167309694, 1326743389,                       '18449997', '634999260', '11945512', '2370221592', '968615264', '338376782', 
                             2466169957, 277460126, 978488840, 973465514, 963073442, 1908166152, 142690511, 
                             447832680, 337171830,398603525, 2343845391, 122445010, 1637833237, 221786542, 
                             1368850908, 318499634,13065292, 195689744, 143393223, 772349570, 133366702, 
                             1915200546, 1530798872, 262823808,49275896, 1107008174, 61727028, 931706882,
                             57391779, 87934587, 216003605, 605614784,127025568,1135141640, 1943781798, 
                             2195622679, 79991599, 974102796, 238909679, 620859402,64298256, 615597661, 
                             381611850, 62003557, 494953070, 720048936]

for elem in elementi_da_aggiungere_M5S:
    M5S.append(int(elem))


LeU = [str(elem) for elem in LeU] 
with open("LeU.txt", "wb") as fp:   #Pickling
    pickle.dump(LeU, fp)

M5S = [str(elem) for elem in M5S] 
with open("M5S.txt", "wb") as fp:   #Pickling
    pickle.dump(M5S, fp)

Centro_Sinistra = [str(elem) for elem in Centro_Sinistra] 
with open("Centro_Sinistra.txt", "wb") as fp:   #Pickling
    pickle.dump(Centro_Sinistra, fp)

Centro_Destra = [str(elem) for elem in Centro_Destra] 
with open("Centro_Destra.txt", "wb") as fp:   #Pickling
    pickle.dump(Centro_Destra, fp)

###############################################################################






####### Find out For who a person votes for


#DEFINING QUEUE 
    
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
#FUNCTION 

def election(start, count, queue, User):
    peso_voto = {"Centro_Sinistra":0,"Centro_Destra": 0,"M5S":0,"LeU":0}
    
    if start not in User:
        print(start)
        prova = True
        while prova == True:
            try:
                s = api.get_user(id = start)
                prova = False
            except:
                print("RateLimitError")
                time.sleep(15 * 60)
        s = process_or_store(s._json)
        json_acceptable_string = s.replace("'","/")
        d = json.loads(json_acceptable_string)
        
        if d["followers_count"] < 10**6 and (d["lang"] =="it" or d["lang"] =="in") and d["default_profile_image"] == False:
            
            print("We are looking at the retweets")
            conto_retweet = 0
            for retweet in limit_handled(tweepy.Cursor(api.user_timeline, id=start,count=100).items()):
                s = process_or_store(retweet._json)
                json_acceptable_string = s.replace("'","/")
                d = json.loads(json_acceptable_string)
                
                try:
                    #retweet.append(d["entities"]["user_mentions"][0]["screen_name"])
                    conto_retweet += 1
                    
                    if api.get_user(d["entities"]["user_mentions"][0]["screen_name"]).id in Centro_Sinistra :
                        peso_voto["Centro_Sinistra"] += 1
                    elif api.get_user(d["entities"]["user_mentions"][0]["screen_name"]).id in Centro_Destra :
                        peso_voto["Centro_Destra"] += 1
                    elif api.get_user(d["entities"]["user_mentions"][0]["screen_name"]).id in M5S:
                        peso_voto["M5S"] += 1
                    elif api.get_user(d["entities"]["user_mentions"][0]["screen_name"]).id in LeU:
                        peso_voto["LeU"] += 1
                except:
                    #print("I'm waiting 15 minutes")
                    pass
            print("Il conto_retweet è di : " + str(conto_retweet))    
            
            
            print("We are looking at the favorites")
            conto_favorite = 0
            for favorite in limit_handled(tweepy.Cursor(api.favorites, id=start,count=100).items()):
                s = process_or_store(favorite._json)
                json_acceptable_string = s.replace("'","/")
                d = json.loads(json_acceptable_string)
                
                try:
                    #like.append(d["user"]["screen_name"])
                    conto_favorite +=1
        
                    if api.get_user(d["user"]["screen_name"]).id in Centro_Sinistra :
                        peso_voto["Centro_Sinistra"] += 1
                    elif api.get_user(d["user"]["screen_name"]).id in Centro_Destra :
                        peso_voto["Centro_Destra"] += 1
                    elif api.get_user(d["user"]["screen_name"]).id in M5S:
                        peso_voto["M5S"] += 1
                    elif api.get_user(d["user"]["screen_name"]).id in LeU:
                        peso_voto["LeU"] += 1
                except:
                    #print("I'm waiting 15 minutes")
                    pass
            print("Il conto_favorite è di : " + str(conto_favorite))
            
            
            print("We are looking at the follower")
            conto_foll = 0    
            aggiunti = []
            for follower in  tweepy.Cursor(api.friends_ids, id=start).items():
                
                conto_foll += 1
                aggiunti.append(follower)
                
                
                if follower in Centro_Sinistra :
                    peso_voto["Centro_Sinistra"] += 1
                elif follower in Centro_Destra :
                    peso_voto["Centro_Destra"] += 1
                elif follower in M5S:
                    peso_voto["M5S"] += 1
                elif follower in LeU:
                    peso_voto["LeU"] += 1
            
            print("Il conto_foll è di : " + str(conto_foll))
            
            if peso_voto != {"Centro_Sinistra":0,"Centro_Destra": 0,"M5S":0,"LeU":0}:
                for foll in aggiunti:
                    queue.enqueue(foll) #si può fare enqueue di lista
                        
                Partito_Vincente = max(peso_voto.items(), key=operator.itemgetter(1))[0]
                Voto_Totale[Partito_Vincente] += 1
                User[start] = Partito_Vincente 
                count += 1
   
    if count <= 6:
        start = queue.dequeue()
        print(Voto_Totale)
        return (election(start, count, queue,User))
    else:
        return (Voto_Totale)
    

#Example
User = {}       
Voto_Totale = {"Centro_Sinistra":0,"Centro_Destra": 0,"M5S":0,"LeU":0}

queue = Queue()
start= "ValerioGuarrasi"
count= 0

Voto_Totale = election(start, count, queue, User)

