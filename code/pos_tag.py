'''
Finding the POS tag for a text file in unsupervised learngin
'''
from __future__ import division
import sys
import nltk
import os
from nltk import word_tokenize
from os import listdir
from os.path import isfile, join
import random
import time
import urllib
import json
from math import log
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
proxies = {'http': 'http://manish.sharma:qwerty987@202.141.80.19:3128'}

def POS_tag():
	#onlyfiles = os.listdir('../../data/review_polarity/txt_sentoken/pos')
	onlyfiles = [f for f in listdir('../../data/review_polarity/txt_sentoken/pos') if isfile(join('../../data/review_polarity/txt_sentoken/pos', f))]
	for files in onlyfiles:
		with open('../../data/review_polarity/txt_sentoken/pos/'+ files, 'r') as myfile:
			data=myfile.read()
			#print data
			text = word_tokenize(data)
			tags = nltk.pos_tag(text)
			#get_phrases(tags)
			break
	#print tags
	return tags
def get_phrases(tags):
	#for tag in tags:
	#	if (tag[1] == "JJ") or (tag[1] == "JJR") or (tag[1] == "JJS") or (tag[1] == "RB") or (tag[1] == "RBR") or (tag[1] == "RBS") :
	#		print tag[0]
	phrase_list = []
	for first, second in zip(tags,tags[1:]):
		if ((first[1] == "JJ") or (first[1] == "JJR") or (first[1]=="JJS")) and ((second[1] == "NN") or (second[1] == "NNS")):
			phrase_list.append(first[0] + " "+second[0])
		if ((first[1] == "RB") or (first[1] == "RBR") or (first[1] == "RBS")) and ((second[1] == "JJ")):
			phrase_list.append(first[0]+" "+second[0])
		if first[1] == "JJ" and second[1] == "JJ":
			phrase_list.append(first[0]+" "+second[0])
		if ((first[1] == "NN") or (first[1] == "NNS")) and second[1] == "JJ":
			phrase_list.append(first[0]+" "+second[0])
		if ((first[1] == "RB") or (first[1] == "RBR") or (first[1] == "RBS")) and ((second[1] == "VB") or (second[1] == "VBD") or (second[1] == "VBN") or (second[1] == "VBG")):
			phrase_list.append(first[0]+" "+second[0])

	#print phrase_list
	return phrase_list

# This portion of the code calculates the PMI-IR of the phrases using Google
def hits(word1,word2=""):
    query = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s"
    if word2 == "":
        results = urllib.urlopen(query % word1,proxies=proxies)
        print results
    else:
        results = urllib.urlopen(query % word1+" "+"AROUND(10)"+" "+word2,proxies=proxies)
        print results
    time.sleep(random.choice((1,3,3,2,4,1,0)))
    pauseDur = 4 + random.random()*15
    print "sleeping for: %d seconds" % pauseDur
    time.sleep(pauseDur)
    json_res = json.loads(results.read())
    print json_res
    google_hits=int(json_res['responseData']['cursor']['estimatedResultCount'])
    print google_hits
    return google_hits


def so(phrase):
    num = hits(phrase,"excellent")
    #print num
    den = hits(phrase,"poor")
    #print den
    ratio = num / den
    #print ratio
    sop = log(ratio)
    return sop

if __name__ == '__main__':
	tags = POS_tag()
	phrase_list = get_phrases(tags)
	print phrase_list
        avg_so = 0
	for phrase in phrase_list:
		print phrase
		print so(phrase)
		avg_so += so(phrase)
	print avg_so
