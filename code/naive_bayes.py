from __future__ import division
import sys
import os
import time
import math
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from nltk.stem.lancaster import LancasterStemmer
import nltk
import itertools
import collections
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import operator
from collections import defaultdict
from collections import OrderedDict
import string
from nltk.stem.wordnet import WordNetLemmatizer
import numpy
from collections import Counter
from nltk.probability import FreqDist
from decimal import *
punctuations = list(string.punctuation)
ps=PorterStemmer()
lmtzr = WordNetLemmatizer()


#.........................  Reading files and removing stopwords and doing lemmatization

fp = open('test1.txt', 'w')
f1 = open('positiveword.txt', 'w')
f2 = open('negativeword.txt', 'w')

data_dir = "/home/macky/Documents/python/isiproject/review_polarity/txt_sentoken/"
classes = ['pos', 'neg']


for curr_class in classes:
	dirname = os.path.join(data_dir, curr_class)
	count=0;
	for fname in os.listdir(dirname):
	    with open(os.path.join(dirname, fname), 'r') as f:
	    	for line in f :
			    for word in line.split(): # simple tokenization
			        if word not in stopwords.words('english') and  word not in  punctuations :	
			        	temp2=ps.stem(word)
			        	fp.write(lmtzr.lemmatize(temp2))
			        	fp.write('\n')
		        		if curr_class == 'pos' and (count<=600 and count <  800 ): 
		        			f1.write(lmtzr.lemmatize(temp2))
		        			f1.write('\n')
	        			if curr_class == 'neg'and (count<=600 and count <  800 ): 
		        			f2.write(lmtzr.lemmatize(temp2))
		        			f2.write('\n')
		count = count + 1	
		
fp.close()
f1.close()
f2.close()


#.................................  creati;88ng  Feature vector ................
fp= open('test1.txt')
raw = fp.read()
fp.close()
tokens = nltk.word_tokenize(raw)
fdist = nltk.FreqDist(tokens)
temp= FreqDist(fdist)
x=Counter(temp)
temp=x.most_common(1000)
feature =  dict(temp)


total = 0
fp= open('positiveword.txt')
raw = fp.read()
fp.close()
tokens1 = nltk.word_tokenize(raw)
posprob = defaultdict(int)
fdist1 = nltk.FreqDist(tokens1)
for row in temp:
	if row[0] in fdist1.keys():
  		val = fdist1[row[0]]
  		total = total + val	
	else:
  		total = total + 0
total = float(total)
for row in temp:
	if row[0] in fdist1.keys():
  		val = fdist1[row[0]]
  		getcontext().prec = 10
		if total != 0.0 :
  			posprob[row[0]]=  ( (val) / (total) )
	else:
		if total != 0.0 :
  			posprob[row[0]]=  ( (0) / (total) )


total1 = 0
fp= open('negativeword.txt')
raw = fp.read()
fp.close()
tokens2 = nltk.word_tokenize(raw)
negprob = defaultdict(int)
#compute frequency distribution for all the bigrams in the text
fdist2 = nltk.FreqDist(tokens2)


#temp1=fdist1.most_common()


for row in temp:
	if row[0] in fdist2.keys():
  		val = fdist2[row[0]]
  		total1 = total1 + val	
	else:
  		total1 = total1 + 0
total1 = float(total1)
for row in temp:
	if row[0] in fdist2.keys():
  		val = fdist2[row[0]]
  		getcontext().prec = 10
  		if total1 != 0.0  :
  			negprob[row[0]]=  ( (val) / (total1) )
  		#fp.write(str(val))
  		#fp.write('\n')
	else:
		if total1 != 0.0 :
  			negprob[row[0]]=  ( (0) / (total1) )

#print negprob
#print total1 
true_positive=0
true_negative=0
false_negative=0
false_positive=0
fptr = open('sentiment_output4.txt','w')
for curr_class in classes:
	dirname = os.path.join(data_dir, curr_class)
	count=0;
	for fname in os.listdir(dirname):
		with open(os.path.join(dirname, fname), 'r') as f:
			if (count>=600 and count <  800 ) :
				
				fp1 = open('test_data.txt','w')
				for line in f:
					for word in line.split(): # simple tokenization
						if word not in stopwords.words('english') and  word not in  punctuations :	
							temp2=ps.stem(word)
							fp1.write(lmtzr.lemmatize(temp2))
							fp1.write('\n')
				
				prob1=0.0 
				prob2=0.0
				fp = open('test_data.txt','r')
				
				prob1=0.0 
				prob2=0.0
				raw =  fp.read()
				tokens3 = nltk.word_tokenize(raw)
				test = defaultdict(int)
				fdist3 = nltk.FreqDist(tokens3)
				temp3= FreqDist(fdist3)
				x=Counter(temp3)
				temp3=x.most_common()
				#temp3=fdist3.most_common()
				for row in temp3:
					if row[0] in feature.keys():
						if row[0] in fdist1.keys():
							if(posprob[row[0]] == 0.0):
								prob1 = prob1 + ( row[1] * math.log('0.00000000001') )
							else:
								prob1 = prob1 + ( row[1] * math.log(posprob[row[0]]) )
						if row[0] in fdist2.keys():
							if(negprob[row[0]] == 0.0) :
								prob2 = prob2 + ( row[1] * math.log('0.00000000001') )
							else:
								prob2 = prob2 +	( row[1]  * math.log(negprob[row[0]]) )
				if prob1 >= prob2 :
					fptr.write("Sentiment is positive")
					if curr_class ==  'pos':
						true_positive = true_positive + 1
					else:
						false_negative=false_negative + 1
					#print prob1
				else :
					fptr.write("Sentiment is negative  ")
					if curr_class ==  'neg':
						true_negative = true_negative + 1
					else :
						false_positive=false_positive + 1
					#print prob2
				fptr.write(str(prob1))
				fptr.write('\n')
				fptr.write(str(prob2))
				fptr.write('\n')
				
		count = count + 1	 
print true_positive
print true_negative
print false_negative
print false_positive
print (true_positive/(true_positive + false_negative))
print (true_negative/(true_negative + false_positive))
print (true_positive/(true_positive + false_positive))
print (true_negative/(true_negative +false_negative))