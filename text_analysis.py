# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:55:41 2018

@author: user
"""
import nltk
from pymongo import MongoClient
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pylab import figure

from os import path
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator

client = MongoClient('localhost', 27017)
db = client["twitter-elections"]

def normalise(lyric):
    
    #print(lyric.split())
    ##Rimuovere nel tweet la parola che inizia per https
    lyric = " ".join(filter(lambda x:x[0] != 'h', lyric.split()))
    #print(lyric)
    
    #remove punctuation
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    lyric_sw = tokenizer.tokenize(lyric) #split the lyric in to tokens

    #Normalizing to lower
    lyric_sw = [token.lower() for token in lyric_sw]
    
    #Removing stop words and small words
    stops = set( nltk.corpus.stopwords.words('italian'))
    minlength = 2
    lyric_sw = [token for token in lyric_sw if ((not token in stops) and len(token) >= minlength)]
 
    #Stemming
    porter = nltk.PorterStemmer()
    lyric_sw = [porter.stem(token) for token in lyric_sw]
    
    #return ' '.join(lyric_sw)
    return (lyric_sw)



parties = ["Twitter_LeU", "Twitter_M5S", "Twitter_CentroSinistra", "Twitter_CentroDestra"]

for party in parties:
    collection = db[party]
    #Create the empy dictionary about occurrences for each parties 
    diz_occ = {}
    tweet_evolution = collection.find()
    #print(tweet_evolution)
    for tweet in tweet_evolution:
        #print(tweet)
        for elem in normalise(tweet["text"]) :
            if elem in diz_occ:
                diz_occ[elem] += 1
            else:
                diz_occ[elem] = 1
     
    #Extract the fifteen(or more) most used terms     
    Most_used = dict(Counter(diz_occ).most_common())
    
    #If you want to see the words used by each parties mostly
    #print(Most_used, party ,"\n")
    
    #Creating the histogram for the most used words 
    print('Generating the bar graph of the most used words ...')
    
    # this is the  histogram of the number of songs per Artist
    values = [x for x in Most_used.values()]
    #fig=figure(figsize=(20,10))
    barlist = plt.bar(range(len(values[:20])),values[:20], color = 'c')
    plt.title('Number of occurrences for the most used words by ' + party)
    plt.xlabel("Words")
    plt.ylabel("Number of occurrences")
    cathegorie = [y for y in Most_used]
    plt.xticks(range(len(cathegorie[:20])), cathegorie[:20], rotation='vertical')
    barlist[0].set_color('g')
    plt.savefig("number_of_occurrences_per_words_for" + party + ".png", dpi = 300)
    plt.show()

    
    #Create a list with the keys of dictionary occurrences
    l =[elem for elem in Most_used.keys()]
    #Argument of WorldCloud is a string but in a increasing order
    l = ' '.join(l)



##########   First Type of PLOT   ########## 
    
    print('\nWordCloud of the most common words used in ',party)
    plt.figure(figsize = (8,10),facecolor='k')
    wordcloud = WordCloud(background_color = 'black', mode = 'RGB', width = 1000, height = 800).generate(l)
    plt.title('Number of occurrences for the most used words by ' + party)   
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("First_PLOT_" + party + ".png", dpi = 300)
    plt.show()

##########   Second Type of PLOT   ########## 
    
    #d = path.dirname(__file__)
    d = "C:/Users/user/Desktop/Twitter-Elections"
    # Read the whole text.
    text = l
    # read the mask / color image taken from
    # http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
    alice_coloring = np.array(Image.open(path.join(d, party+".png")))
    
    wc = WordCloud(background_color="black", max_words=2000, mask=alice_coloring,
             max_font_size=50, random_state=10)
    # generate word cloud
    wc.generate(text)
    
    # create coloring from image
    image_colors = ImageColorGenerator(alice_coloring)
    
    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    fig=figure(figsize=(8,10),facecolor='k')
    #It is not the right code for saving this fig 
    #plt.savefig("Second_PLOT_" + party + ".png",  dpi=fig.dpi)
    plt.figure()
             
