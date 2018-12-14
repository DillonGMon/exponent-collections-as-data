import numpy as np
import re
import os
import nltk
from operator import itemgetter
import regex
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from pathlib import Path
#used to combine all the txt files in the output folder intoa single file to process mulitple files simultaniously
def combineOutputs():  
    location="output"
    output = open('output.txt','w')
    for file in os.listdir(location):

        file = location+'/'+file
        print(file)
        with open(file,'r') as infile:
        
            for line in infile:
                output.write(line)
        infile.close()
    output.close()
    print('done')
            



def tokenize_sentences(sentences):
    words = []
    for word in sentences.split():
        
        print(word)
        w = extract_words(word)
        words.extend(w)
        
    words = sorted(list(set(words)))
    return words

def extract_words(sentence):
    ignore_words = ['a']
    words = re.sub("[^\w]", " ",  sentence).split()
    nltk.word_tokenize(sentence)
    words_cleaned = [w.lower() for w in words if w not in ignore_words]
    return words_cleaned    
    
def bagofwords(sentence, words):
    sentence_words = extract_words(sentence)
    # frequency word count
    bag = np.zeros(len(words))
    for sw in sentence_words:
        for i,word in enumerate(words):
            if word == sw: 
                bag[i] += 1
                
    return np.array(bag)
#reads the outputfile and then write the list of individual words used to a file
#also returns the output.txt as a  single string for later processing
def getVocab():
    sentences=''
    with open('output.txt','r') as infile:
    
        for line in infile:
            sentences = sentences+line

#print(sentences)
    print("sentences")
    vocabulary = tokenize_sentences(sentences)
    output =open('vocab.txt','w')
    for item in vocabulary:
        output.write(item+",")
    output.close()
    return sentences
#uses the vocabulary output file and checks it against the original text to get number of occurances per word
def getfreq(sentences):
    vocab = open('vocab.txt','r')
    words = vocab.read()
    words = re.split(',', words)
    bag = open('bagwords.txt','w')
    occurances = []
    for item in words:
    
        curr= [item,0]
        for word in sentences.split():
            if item==word:
                curr[1]+=1
        occurances.append(curr)
        print(curr)
   
    vocab.close()


    for item in occurances:
         bag.write(item[0] +' '+str(item[1])+'\n')
#sorts the bag of words by number of occurances, from least to greatest
def sortvals():
    keywordlist=[]
    file = open('bagwords.txt','r')
    for line in file:
        item = re.split(' ',line)
        keywordlist.append(item)
        
    stopwords = nltk.corpus.stopwords.words('english')
    extraStops=['like','rst','pm','us','go','way','one','said','also','two','e','get', 'new','ing','aer','ursday','10','things']
    for item in extraStops:
        
        stopwords.append(item)
    output = sorted(keywordlist,key=lambda x: int(x[1]))
    outputfile = open('sortedbag.txt','w')
    for item in output:
        item[0]=re.sub('\n','',item[0])
        item[1] = re.sub('\n','',item[1])
        if(item[0] not in stopwords and len(item[0])>2):
            outputfile.write(item[1]+ ' ' + item[0]+'\n')
    file.close()
    outputfile.close()
#currently unused, replaced by the venn diagram, which has essentially the same functionality
def getsames():
    first = open("sortedbag.txt","r")
    print("first open")
    second = open("2016_data/sortedbag.txt","r")
    print("second open")
    out = open("similarites.txt",'w')
    print("output opened")

    for line in first:
        print(line)
        line = re.sub('\n','',line)
        items = re.split(' ', line)
        print(str(items))
        for lines in second:
            lines = re.sub('\n','',lines)
            sec = re.split(' ', lines)
            print('     '+lines)
            print('     '+str(sec))
            print(items[1],' ', sec[1])
            if items[1] == sec[1]:
                print("match")
                out.write(item[1])

    first.close()
    second.close()
    out.close()
#reads two separate bag of words and makes a venn diagram based on the words they have in common
def getVenn():
    old = set()
    new = set()
    fileflag = False
    while fileflag==False:
        firstname= input("what is the name of the first file with location if necessary to add to the diagram?\n")
        firstpath = Path(firstname)
        if firstpath.is_file():
            first = open(firstname,"r")
            fileflag = True
    print("first open")
    fileflag= False
    while fileflag == False:
        secondname= input("what is the name of the second file with location if necessary to add to the diagram?\n")
        secpath = Path(secondname)
        if secpath.is_file():
            second = open(secondname,"r")
            fileflag = True
    print("second open")
    for line in first:
        line = re.sub('\n','',line)
        line = re.split(' ',line)
        old.add(line[1])
    for line in second:
        line = re.sub('\n','',line)
        line = re.split(' ',line)
        new.add(line[1])
    setlabels = []
    label= input("how to label the first dataset?\n")
    setlabels.append(label)
    label= input("how to label the second dataset?\n")
    setlabels.append(label)
    ven = venn2([old,new], set_labels=setlabels)
    plt.title('exponent word relations')
    
    plt.show()

def main():
    flag = False
    while flag==False:
        inpt= input("press 0 to combine the files in the output folder first, 1 to get the bag, 2 to get the chart, or 3 to exit \n")
        print(inpt)

        if inpt=='0':
            combineOutputs()
            sentences = getVocab()
            getfreq(sentences)
            sortvals()
        elif inpt=='1':
            sentences = getVocab()
            getfreq(sentences)
            sortvals()
            
        #getsames()
        elif inpt=='2':
            getVenn()
        elif inpt =='3':
            flag = True

    print('done')
    #bagofwords(sentences, vocabulary)
main()

##from sklearn.feature_extraction.text import CountVectorizer
##vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000) 
##train_data_features = vectorizer.fit_transform(sentences)
##vectorizer.transform(["Machine learning is great"]).toarray()
##print(vocabulary)
