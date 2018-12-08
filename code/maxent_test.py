'''
This file contains the code for the test of max_entropy. The pkl file contains the trained model to 
be loaded. There are two methods used - 1) Frequncy model 2) Presence(True or False) model
Please use another_bow() func in Frequncy model with maxent_freq.pkl and bag_of_words() func with 
maxent_bow.pkl in Presence model

The output generated is the accuracy and Precision and recall

'''

from itertools import chain
from collections import defaultdict

import nltk
from nltk.classify import MaxentClassifier, accuracy
from nltk.corpus import movie_reviews
import pickle

from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")

def bag_of_words(words):
    """
    Change a document into a BOW feature vector represented by a dict object.
    """
    word_new = []
    for word in words:
        if word not in cachedStopWords:
            word_new.append(word)
    words = word_new
    return dict([(word, True) for word in words])

def another_bow(words):
    word_new = []
    for word in words:
        if word not in cachedStopWords:
            word_new.append(word)
    words = word_new
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] +=1
        else:
            dictionary[word] = 1
    return dictionary
def label_feats_from_corpus(corp, feature_detector=bag_of_words):
    """
    Change the corpus into a feature matrix. Sometimes the proceess is 
    known as vectorization. The default is the use BOW features.
    """
    label_feats = defaultdict(list)
    for label in corp.categories():
        for fileid in corp.fileids(categories=[label]):
            feats = feature_detector(corp.words(fileids=[fileid]))
            label_feats[label].append(feats)
    return label_feats


def split_label_feats(lfeats, split=0.75):
    """
    Splits corpus into train and test portion.
    This module is used after using `label_feats_from_corpus`.
    """
    train_feats = []
    test_feats = []
    for label, feats in lfeats.iteritems():
        cutoff = int(len(feats) * split)
        train_feats.extend([(feat, label) for feat in feats[:cutoff]])
        test_feats.extend([(feat, label) for feat in feats[cutoff:]])
    return train_feats, test_feats


# Extract features from corpus and for each document label it with the appropriate labels. 
label_feats = label_feats_from_corpus(movie_reviews)
'''
for label in label_feats:
    for document in label_feats[label]: 
        print label, document
        break
    break
'''

# Let's split the data up into train and test.
train_documents, test_feats = split_label_feats(label_feats) 


f = open('maxent_bow.pkl','rb')
clf = pickle.load(f)
#print len(train_documents)
#print len(test_feats)
#print accuracy(clf, test_feats)
#print type(test_feats[0][0])
#print test_feats[0][0]
#print clf.classify([fs for (fs,l) in test_feats[0]])
#print clf.classify(test_feats[0][0])
#print test_feats[0][1]
count = 0
'''
for i in xrange(len(test_feats)):
    x = clf.classify(test_feats[i][0])
    if x == test_feats[i][1]:
        count +=1
'''
#calculating the precision and recall for the pos and neg files

TP_pos = 0
TN_pos = 0
FP_pos = 0
FN_pos = 0
TP_neg = 0
FP_neg = 0
TN_neg = 0
FN_neg = 0

for i in xrange(len(test_feats)):
    x = clf.classify(test_feats[i][0])
    if test_feats[i][1] == 'pos':
        if test_feats[i][1] == x:
            TP_pos +=1
            count +=1
            FN_neg +=1
            ##same as FN_neg
        else:
            TN_pos +=1
            FP_neg +=1
            ##
    else:
        if test_feats[i][1] == x:
            TP_neg += 1
            FN_pos +=1
            count +=1
        else:
            TN_neg +=1
            FP_pos +=1
precision_pos = float(TP_pos)/(TP_pos+FP_pos)*100
recall_pos = float(TP_pos)/(TP_pos+TN_pos)*100
precision_neg = float(TP_neg)/(TP_neg+FP_neg)*100
recall_neg = float(TP_neg)/(TP_neg+TN_neg)*100
print "Accuracy - "+ str(float(count)/len(test_feats) *100)

print "For positive docs Precision = " + str(precision_pos) + " Recall: " + str(recall_pos)
print "For negative docs Precision = " + str(precision_neg) + " Recall: " + str(recall_neg) 

#print accuracy(clf,test_feats[0])
#print test_feats
#for i in test_feats:
#    print clf.classify(i)