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

cfg = {
    "consumer_key" :"RquN0zhitB82NARp79NC9xXHb",
    "consumer_secret":"77TJqc5dfBkdLso3uhx7UV5zHGPdbPUdxnlpn8KHCcINFGJAY8",
    "access_token" :"931887582190895104-OXDeNHFHHwNTkQLIojdDvzvg7jGXgAg",
    "access_token_secret" :"04why4jJLITZMAMjTS0YIsdp85dO37Kgsx7ekhp5YsElZ"}

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
        
        
#FIND INTERSECTIONS BETWEEN LISTS
        
#Now we find the instersections between the previous lists
#for i in set(Centro_Sinistra).intersection(set(M5S)):
    #print (i)
    #u = api.get_user(i)
    #print (u.screen_name)
    
## Observations:
## mirella liuzzi , spokeswoman of M5S, so we delete her id from Centro_Sinistra's list
Centro_Sinistra.remove(11945512)
## While the others intersections can be deleted from both lists

#Now we find the instersections between the previous lists
#for i in set(Centro_Sinistra).intersection(set(LeU)):
#    print (i)
#    u = api.get_user(i)
#    print (u.screen_name)

##Observations:
#Deleting from Centro_Sinistra :
# 430169858 Arturo_Scotto, 1111162884 MichelaRostan, 120053510 Sannicandro_A,447432073 PetrisDe,
# 2398174219 Paolo_Font, 458503181 CelesteCost, 390868112 GAiraudo, 420335251 LuisaBlive, 331005596 robersperanza, 
# 871317662 DZoggia, 586037920 Fornaro62, 1071332641 PietroGrasso, 29185572 cicci1, 14108472 civati,1063940029 filippobubbico, 
# 321302337 CarloPegorer, 1354063814 robertagostini_,37631819 NichiVendola, 97734603 rossipresidente, 493854798 CorradinoMineo,
# 234844623 fralaforgia, 371315536 AntonioPanzeri, 1074572754 mceciguerra,1069530966 MGranaiola, 2913705688 CassonVenezia,
# 221902171 lauraboldrini, 89286622 Cofferati, 2370772835 MassimoPaolucc6, 53944421 flaviozanonato, 3233406309 LucrezRicchiuti,
# 28528873 SI_sinistra, 1962143210,LodovicoSonego 494475884, GotorMiguel,492371310 Piero_Martino,52352494 pbersani,
# 1139458160 LevaDanilo, 1028678899 simoni_elisa, 422168826 NicoStumpo, 1133749243 gu_epifani, #390007456 filippofossati

#40 Elements will be delete

ListaEsclusi= [430169858, 1111162884, 120053510, 447432073, 2398174219, 458503181, 390868112, 420335251, 331005596, 871317662, 
               586037920, 1071332641, 29185572, 14108472, 1063940029, 321302337, 1354063814, 37631819, 97734603, 493854798,
               234844623, 371315536, 1074572754, 1069530966, 2913705688, 221902171, 89286622, 2370772835, 53944421, 3233406309,
               28528873, 1962143210, 494475884, 492371310 ,52352494, 1139458160, 1028678899, 422168826, 1133749243, 390007456]

for elem in ListaEsclusi:
    Centro_Sinistra.remove(elem)
    
#Centro_Sinistra = [elem for elem in Centro_Sinistra if elem not in ListaEsclusi]

#Deleting from LEU:
#13294452 pdnetwork
LeU.remove(13294452)

#Now we find the instersections between the previous lists
#for i in set(M5S).intersection(set(LeU)):
#    print (i)
#    u = api.get_user(i)
#    print (u.screen_name)

## Observations:
## giuliocavalli , is an exponent of LeU so we delete his id from M5S's list
M5S.remove(32624061)

#for i in set(Centro_Sinistra).intersection(set(Centro_Destra)):
    #print (i)
 #  u = api.get_user(i)
    #print (u.screen_name)
    
    #434839840
#lauracesaretti1  Element of leu has to be removed from both lists
    
## Observations:
## Mara Carfagna ,Stefano Maullu and Mario Abbruzzese they are members of the political party FI, 
#so we delete them from PD's list

#123920914 Libero_official,NicoloMardegan 10228272, 214476890 adolfo_urso, 485586578 vfeltri, 72511663 monnalisa19, 89668286
#MarioAbbruzzese, 240642244 gianpierozinzi,212364488 giorgiomule ,526448857 BelpietroTweet, 373423842 Maurizio_Lupi,
#460264679 alesallusti, 594879721 OnAntonioGuidi, 429231339 CarloGarzia, 407543535 mariogiordano5, 104485125 mara_carfagna,
#399004979 NicolaPorro, 50246469 andreadisorte, 334321591 N_DeGirolamo, 585661410 splitalia , 190660606 Tocqueville_it
#434839840 lauracesaretti1 


Centro_Sinistra.remove(23740839)
Centro_Sinistra.remove(123920914)
Centro_Sinistra.remove(22130220)
Centro_Sinistra.remove(214476890)
Centro_Sinistra.remove(485586578)
Centro_Sinistra.remove(72511663)
Centro_Sinistra.remove(89668286)
Centro_Sinistra.remove(240642244)
Centro_Sinistra.remove(212364488)
Centro_Sinistra.remove(526448857)
Centro_Sinistra.remove(373423842)
Centro_Sinistra.remove(460264679)
Centro_Sinistra.remove(594879721)
Centro_Sinistra.remove(429231339)
Centro_Sinistra.remove(407543535)
Centro_Sinistra.remove(104485125)
Centro_Sinistra.remove(399004979)
Centro_Sinistra.remove(50246469)
Centro_Sinistra.remove(334321591)
Centro_Sinistra.remove(585661410)
Centro_Sinistra.remove(190660606)
Centro_Sinistra.remove(434839840)



#Matteo Renzi 18762875 is the leader for the political party PD, so we delete him from ForzaItalia's list
#109573130 unitaonline,33196091 beppesevergnini, 17287244 YouDem , 54988878 DavidSassoli , 45937235 andreasarubbi, 
# 148352085 democratica_web, 76616277 Deputatipd, 274093178 petergomezblog, 441863803 StefanoCeccanti,496437886 AndreaOrlandosp
#74707629 RadioRadicale,535887576 GiuliaCortese1, 35298549 serracchiani, 163567416 giulianopisapia, 150196030 Radicali,
#68941121 rosy_bindi, 14569308 alessiamosca, 13294452 pdnetwork , 61154684 dariofrance, 61291398 massimodonadi , 
#404045211 FinocchiaroAnna, 100218289 pierofassino, 107505580 emmabonino, 47663009 MarcoPannella,311539656 antoniopolito1,
#104960470 nomfup, 406869976 PaoloGentiloni, 138736601 ilriformista, 484982241 graziano_delrio, 267174899 mariolavia ,
#36374014 Pierferdinando, 434839840 lauracesaretti1



Centro_Destra.remove(18762875)
Centro_Destra.remove(109573130)
Centro_Destra.remove(33196091)
Centro_Destra.remove(17287244)
Centro_Destra.remove(54988878)
Centro_Destra.remove(45937235)
Centro_Destra.remove(148352085)
Centro_Destra.remove(76616277)
Centro_Destra.remove(274093178)
Centro_Destra.remove(441863803)
Centro_Destra.remove(496437886)
Centro_Destra.remove(74707629)
Centro_Destra.remove(535887576)
Centro_Destra.remove(35298549)
Centro_Destra.remove(163567416)
Centro_Destra.remove(150196030)
Centro_Destra.remove(68941121)
Centro_Destra.remove(14569308)
Centro_Destra.remove(13294452)
Centro_Destra.remove(61154684)
Centro_Destra.remove(61291398)
Centro_Destra.remove(404045211)
Centro_Destra.remove(100218289)
Centro_Destra.remove(107505580)
Centro_Destra.remove(47663009)
Centro_Destra.remove(311539656)
Centro_Destra.remove(104960470)
Centro_Destra.remove(406869976)
Centro_Destra.remove(138736601)
Centro_Destra.remove(484982241)
Centro_Destra.remove(267174899)
Centro_Destra.remove(36374014)
Centro_Destra.remove(434839840)

#for i in set(Centro_Destra).intersection(set(M5S)):
    #print (i)
    #u = api.get_user(i)
    #print (u.screen_name)
    
#Observation:
#19067940 beppe_grillo,he was the first leader of M5S
Centro_Destra.remove(19067940)

#for i in set(Centro_Destra).intersection(set(LeU)):
    #print (i)
    #u = api.get_user(i)
    #print (u.screen_name)
    
#Observations 
# The print above returns only names which belong to the LeU so we delete them from the Centro_Destra's List (8 elements will be deleted)
for i in set(Centro_Destra).intersection(set(LeU)):
    Centro_Destra.remove(i)
    
    
#813286 BarackObama
#732819391 Quirinale
#36624443 AmbasciataUSA
#2278995820 Montecitorio
#22123270 Nova24Tec
#15254807 Internazionale
#5893702 SkyTG24
#25676606 Adnkronos
#10228272 YouTube
#14711301 zdizoro
#47626792 cgilnazionale
#70216875 anpirimini
#301472434 StefanoFassina
#131173948 AnpiBarona
#440943555 SusannaCamusso
#73087558 liberiegiusti
#51678300 Anpinazionale
#18949452 FT
#25512578 Greenpeace_ITA
#146448681 valigiablu
#23615081 emergency_ong
#200028163 Lettera43
#416428550 Apndp
#546791475 OmnibusLa7
#522078771 cjmimun
#165489209 twittopolis
#70971449 _DAGOSPIA_
#36624443 AmbasciataUSA
#210573372 davidallegranti
#145225789 gadlernertweet
#150725695 Agenzia_Ansa
#27456576 masechi
#608747590 Pubblico
#420351046 sole24ore
#5893702 SkyTG24
#394313 pandemia
#25100373 luca_conti


#6276292 gianlucaneri
#501813967 PieroSansonetti
#29416653 LaStampa
#37621971 Europarl_IT
#153725655 zipsternews
#365462238 eziomauro
#307423967 giucruciani
#94072544 RepubblicaTv
#419946721 tiritwittoio
#49954018 ilfoglio_it
#85639608 reuters_italia
#382238648 SalvatoreMerlo
#248176574 askanews_ita
#732819391 Quirinale
#2430152420 MipaafSocial
#5894372 SkySport
#14060262 RaiNews
#196097766 spinpolitics
#239760107 YTCreators
#106772715 qn_lanazione
#25508589 ilgiornale
#69959408 Tg3web
#317769975 agorarai
#33994488 ItalianPolitics
#85852409 espressonline
#599114492 ItalyMFA
#202261245 SONDAITALIA
#121424128 La7tv
#102703874 lavoceinfo
#69237508 trapanimartino
#22123270 Nova24Tec
#840370952 PagellaPolitica
#802635019 L_Economia
#41667342 spinozait
#56341776 rtl1025
#100459284 LUltimaParola
#149060372 angealfa
#15254807 Internazionale
#588587293 VincinoWeb
#9300262 politico
#68421930 corriereveneto
#372273460 myrtamerlino
#58768691 fabiochiusi
#72248630 Agenzia_Italia
#89193275 TheFrontPageRV
#35525950 Affaritaliani
#1488372031 MEF_GOV
#400293698 peregopaola
#1092735302 MinSviluppo
#380473676 PierluigiBattis
#404064077 you_trend
#92030800 corrieremilano
#331617619 MediasetTgcom24
#543774554 HuffPostItalia
#73192285 lademocrazia_it
#1142954335 Omniromanews
#18935802 repubblica
#16433508 liquida
#52424550 fattoquotidiano
#201658727 VittorioSgarbi
#804354408 TgrRai
#2278995820 Montecitorio
#20910977 lucasofri
#9479042 micheleficara
#16735106 journalismfest
#478720395 ferrarailgrasso
#127200141 agenzia_stampa
#17814938 Storify
#44487069 chedisagio
#94335911 RaiRadio2
#1433286055 RaiTre
#307927464 RomaCapitaleNW
#372344749 andreavianel
#215728045 Linkiesta
#673203 stefanoepifani
#85639608 reuters_italia
#382238648 SalvatoreMerlo
#248176574 askanews_ita
#732819391 Quirinale
#41570239 Cla_Gagliardini
#7912442 tigella
#384192964 MinisteroDifesa
#481154512 minambienteIT
#828717014 TgLa7
#395218906 Corriere
#197536731 Scenaripolitici
#58453980 PiazzapulitaLA7
#384927198 gparagone
#16246240 luigicrespi
#2865677793 bussolarai
#33502178 MiBACT
#40006630 smenichini
#373287402 DanieleKeshk
#89411566 Il_Centro
#100610543 lucatelese
#558661103 PPolicy_News
#236629498 tecneitalia
#89674237 simonespetia
#31093748 FrancoBechis
#14073332 lucabecattini
#28081142 Primaonline
#55212559 mariocalabresi
#17488916 twitorino
#526530582 tg2rai
#126680070 AcquaBeneComune
#618222602 LaRetrovia
#420942860 RaiBallaro
#44926477 RaiPlay
#76615199 TermometroPol
#31762979 BlitzQuotidiano
#82886693 mattinodinapoli
#73971750 riotta
#7404632 lucadebiase
#292197467 comuni_anci
#465390684 Ariachetira
#14516324 robertosaviano
#1171761254 mitgov
#381369966 SteAlbamonte
#36079217 ilmessaggeroit
#228089463 panepolitica
#452361847 PaolaDiCaro
#67006079 1giornodapecora
#126677638 Radio24_news
#151029385 PietroSalvatori
#2585782921 Viminale
#122014351 Tommasolabate
#14420623 donatotesta
#335953039 DeBortoliF
#1091721366 BrunoVespa
#404127899 tweetpolitica
#328635035 sarahvaretto
#167679645 EdmunDoDuBrasiL
#1307016348 poke_dem
#963938472 Palazzo_Chigi
#133790890 ilpost
#882235051 MiurSocial
#35740848 Cepernich
#58430129 ignaziomarino
#1377373874 SenatoStampa
#29045944 claudiocerasa



lista = [813286,732819391,36624443,2278995820,22123270,15254807,5893702,25676606,10228272,14711301,47626792,70216875,301472434,
         440943555,73087558,51678300,18949452,25512578,146448681,23615081,200028163, 416428550,546791475,522078771,165489209,
         70971449,36624443,210573372,145225789,150725695,27456576,608747590,
    420351046,5893702,394313, 25100373,6276292,501813967,29416653 ,37621971 ,153725655 ,365462238 ,307423967 ,94072544 ,419946721 ,49954018 ,85639608 ,382238648 ,
248176574,732819391 ,2430152420 ,5894372 ,14060262 ,196097766 ,239760107,106772715 ,25508589 ,69959408,317769975 
,33994488 ,85852409 ,599114492 ,202261245 ,121424128,102703874 ,69237508 ,22123270,840370952 ,802635019,41667342,56341776 
,100459284 ,149060372 ,15254807 ,588587293 ,9300262 ,68421930 ,372273460 ,58768691 
,72248630 ,89193275 ,35525950,1488372031 ,400293698,1092735302 ,380473676 ,404064077 ,92030800 ,331617619 ,543774554 ,73192285 
,1142954335 ,18935802 ,16433508 ,52424550,201658727 ,804354408 
,2278995820,20910977 ,9479042 ,16735106 ,478720395 ,127200141 ,17814938 ,44487069 ,94335911 ,1433286055 ,307927464 ,372344749 
,215728045 ,673203,85639608 ,382238648 
,248176574 ,732819391 ,41570239,7912442 ,384192964 ,481154512 ,828717014 ,395218906 ,197536731 ,58453980 ,384927198 ,16246240
,2865677793,33502178,40006630 ,373287402 ,89411566 ,100610543,558661103,236629498 ,89674237 ,31093748 ,14073332 ,28081142 
,55212559 ,17488916,526530582 ,126680070 ,618222602 ,420942860,44926477 ,76615199 ,31762979 ,82886693 ,73971750,7404632 ,
292197467 ,465390684 ,14516324 ,1171761254 ,381369966 ,36079217,228089463 ,452361847 ,67006079 ,126677638,151029385 ,2585782921 
,122014351,14420623,335953039 ,1091721366 ,404127899 ,328635035 ,167679645,1307016348,963938472 ,133790890,882235051 ,
35740848,58430129 ,1377373874 ,29045944 ]

for i in list(set(lista)) :
    #print(i)
    if i in Centro_Sinistra:
        Centro_Sinistra.remove(i)
    if i in M5S:
        M5S.remove(i)
    if i in Centro_Destra:
        Centro_Destra.remove(i)
    if i in LeU:
        LeU.remove(i)
        
def process_or_store(tweet):
    return json.dumps(tweet)

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
start= "ValerioGuarrasi  "
count= 0

Voto_Totale = election(start, count, queue, User)



##PULIZIA CENTRO DESTRA

word_dx = ["fi","forza","lega"]
conto = 0
togliere_dx = []
for i in Centro_Destra:
    prova = True
    while prova == True:
        try:
            screen_name = (api.get_user(i).screen_name).lower()
            prova = False
        except:
            print("I'm waiting for ", i, "conto", conto)
            time.sleep(15 * 60)
    conto +=1
    boole = False
    for elem in word_dx :
        if elem in screen_name :
            boole = True
    if boole == False:
        togliere_dx.append(i)
    
        
for e in togliere_dx:
    Centro_Destra.remove(e)



print("WE HAVE FINISHED FOR Centro Destra")

##PULIZIA CENTRO SINISTRA

conto = 0

par = ["pd","popolare","radical","insieme","europa","psi"]
#Remember that lorenzin is the name of a member of this political party , then she will be removed
togliere_sx = []
for i in Centro_Sinistra:
    prova = True
    while prova == True:
        try:
            screen_name = (api.get_user(i).screen_name).lower()
            prova = False
        except:
            print("I'm waiting for ", i , "conto", conto)
            time.sleep(15 * 60)
    conto +=1
    boole = False
    for elem in par :
        if elem in screen_name :
                boole = True
    if boole == False:
        togliere_sx.append(i)
    
        
for e in togliere_sx:
    Centro_Sinistra.remove(e)


print("WE HAVE FINISHED FOR Centro Sinistra")




##Prova

user = api.get_user(screen_name = 'saimadhup')
user.id
s = api.get_user(id = "civica_popolare ")
s = process_or_store(s._json)
json_acceptable_string = s.replace("'","/")
d = json.loads(json_acceptable_string)
d['id']

if 13294452 in Centro_Sinistra:
    print("i")
    
if 946705126911369216 in Centro_Sinistra:
    print("i")  
    