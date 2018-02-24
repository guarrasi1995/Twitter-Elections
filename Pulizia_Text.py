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

client = MongoClient('localhost', 27017)
db = client['Twitter_Prova']


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
    
    for tweet in tweet_evolution:
        for elem in normalise(tweet["text"]) :
            if elem in diz_occ:
                diz_occ[elem] += 1
            else:
                diz_occ[elem] = 1
     
    #Extract the fifteen(or more) most used terms     
    Most_used = dict(Counter(diz_occ).most_common(40))
    
    #Create a list with the keys of dictionary occurrences
    l =[elem for elem in Most_used.keys()]
    #Argument of WorldCloud is a string but in a increasing order
    l = ' '.join(l)

##First Type of Plot ##    
    
    print('\nWordCloud of the most common words used in ',parties)
    plt.figure(figsize = (20,10))
    wordcloud = WordCloud(background_color = 'black', mode = 'RGB', width = 2000, height = 1000).generate(l)
    plt.title('Wordcloud of the most common words in the cluster')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    

### Second type of PLOT ###
    
    
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)
d = 'C:/Users/user/Desktop'

# Read the whole text.
text = l

# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = np.array(Image.open(path.join(d, "Renzi.png")))
stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="black", max_words=2000, mask=alice_coloring,
         max_font_size=60, random_state=20, margin = 10)
# generate word cloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()
                



                                                            