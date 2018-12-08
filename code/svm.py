#   File for svm classifier   classes - positive and negative
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
from decimal import *
punctuations = list(string.punctuation)
ps=PorterStemmer()
lmtzr = WordNetLemmatizer()



#.........................  Reading files and removing stopwords 
fp= open('test3.txt','w')
f1 = open('positiveword.txt', 'w')
f2 = open('negativeword.txt', 'w')
fo=open('feature.txt', 'w')
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
			        	
		        		
		        		
		        		fp.write(word)
			        	fp.write('\n')
		    
		count = count + 1	
		
fp.close()


#.................................   Feature  vector................

fp= open('test3.txt')
#f1=open('feature_count.txt','w')
feature_count=16000
raw = fp.read()
fp.close()
tokens = nltk.word_tokenize(raw)
fdist = FreqDist(tokens)
temp= FreqDist(fdist)
x=Counter(temp)
demo=x.most_common(feature_count)
final1=dict(demo)
final=OrderedDict(sorted(final1.items(), key=lambda x: x[1]))
#output matrix


fp.close()
feature_matrix=numpy.zeros((1600,feature_count))
test_matrix=numpy.zeros((400,feature_count))
positive_output=numpy.ones(800)
negative_output=numpy.zeros(800)
output_matrix=numpy.concatenate((positive_output, negative_output), axis=0)
index=0
test_index=0

# maintaing feature matrix with feature count for each test document
for curr_class in classes:
	dirname = os.path.join(data_dir, curr_class)
	count=0
	for fname in os.listdir(dirname):
		with open(os.path.join(dirname, fname), 'r') as f:
			if count <600 or count>=800:
				raw = f.read()
				tokens = nltk.word_tokenize(raw)
				fdist = FreqDist(tokens)
				feature_position=0
				temp= FreqDist(fdist)
				for key in final :
					if key in temp:
						feature_matrix[index][feature_position]=temp[key]
					feature_position = feature_position + 1
				index += 1 
			else :
				raw = f.read()
				tokens = nltk.word_tokenize(raw)
				fdist = FreqDist(tokens)
				feature_position=0
				temp= FreqDist(fdist)
				for key in final :
					if key in temp:
						test_matrix[test_index][feature_position]=temp[key]
					feature_position = feature_position + 1
				test_index += 1
		count += 1
#Doing classification using svm classifier
##################
clf = svm.SVC()
model=clf.fit(feature_matrix, output_matrix)
import pickle
f = open('svm_train.pkl','wb')
pickle.dump(clf,f)
f.close
#############################
'''
ans = model.predict(test_matrix)
true_positive=0
true_negative=0
false_negative=0
false_positive=0
total=0
for i in ans:
	if i==1 and total < 200:
		true_positive +=1
	elif i==0 and total >= 200:
		true_negative +=1
	elif i==0 and total < 200:
		false_positive +=1
	else :
		false_negative +=1
	total += 1
#printing precision and recall fpr each class 	



print true_positive
print true_negative
print false_negative
print false_positive
print (true_positive/(true_positive + false_negative))
print (true_negative/(true_negative + false_positive))
print (true_positive/(true_positive + false_positive))
print (true_negative/(true_negative +false_negative))
'''