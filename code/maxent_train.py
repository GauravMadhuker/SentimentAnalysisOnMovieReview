'''
This is the training file for the max_entropy code,. Two types of model comparison is done.
There are two methods used - 1) Frequncy model 2) Presence(True or False) model
For Frequncy model use another_bow() func with maxent_freq.pkl and for 
Presence model use bag_of_words() with maxent_bow.pkl func
'''
from itertools import chain
from collections import defaultdict

import nltk
from nltk.classify import MaxentClassifier, accuracy
from nltk.corpus import movie_reviews
import pickle
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")

# Function converting the list of words to dictionary of words and the value is True or False
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

# Function converting the list of words to dictionary of words and the frequency value
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


def label_feats_from_corpus(corp, feature_detector=another_bow):
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

# To train the tagger.
print train_documents[0]
me_classifier = nltk.MaxentClassifier.train(train_documents, algorithm='gis',trace=0,max_iter=10)
print "Training completed successfully.. Now saving the classifier to pickle"
f = open('maxent_freq.pkl','wb')
pickle.dump(me_classifier,f)
#print accuracy(me_classifier, test_feats)