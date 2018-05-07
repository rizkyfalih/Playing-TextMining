# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 23:35:08 2018

@author: rizkyfalih
"""

# Importing the libraries
import pandas as pd
from pandas import DataFrame
import re

# Importing nltk libraries
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Importing xml libraries
from xml.dom import minidom

# Importing classification libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score

def label_to_binary(data):
    for i in data.index:
        if(data.loc[i,'Label'] == "YES"):
            data.loc[i, 'Binary'] = 1
        else:
            data.loc[i, 'Binary'] = 0
    return data

def get_headline_set(filename):
    xmldoc = minidom.parse('Dataset/Data-Set/'+ filename + '.xml')
    headlineList = xmldoc.getElementsByTagName('headline')
    headline = ""
    for i in range(0, len(headlineList)):
        headline += headlineList[i].firstChild.nodeValue
    
    return headline
 
def get_article_set(filename):
    xmldoc = minidom.parse('Dataset/Data-Set/'+ filename + '.xml')
    paragraphList = xmldoc.getElementsByTagName('p')
    paragraph = ""
    for i in range(0, len(paragraphList)):
        paragraph += paragraphList[i].firstChild.nodeValue
    
    return paragraph

def join_all_text_set(filename):
    corpus = ""
    # Get headline
    corpus += get_headline_set(filename)
    # Get article and join with headline
    corpus = " " + get_article_set(filename)
    
    return corpus

def cleaned_text(data):
    newCorpus = []
    for i in data.index:
        corpus = re.sub('[^a-zA-Z]', ' ', data.loc[i, 'Corpus'])
        corpus = corpus.lower()
        corpus = corpus.split()
        ps = PorterStemmer()
        corpus = [ps.stem(word) for word in corpus if not word in set(stopwords.words('english'))]
        corpus = ' '.join(corpus)
        newCorpus.append(corpus)
    return newCorpus

def get_data_set(data):
    for i in data.index:
        data.loc[i, 'Corpus'] = join_all_text_set(str(data.loc[i, 'Filename']))
        
    return data         

def bag_of_words(corpus):
    cv = CountVectorizer()
    X = cv.fit_transform(corpus).toarray()
    
    return X

# Initialize Data Set
dataSet = get_data_set(label_to_binary(pd.read_csv('Dataset/Label/Label-Set.txt', delimiter = ' ')))
corpusSet = cleaned_text(dataSet)
X = bag_of_words(corpusSet)

X_train = X[:577]
y_train = dataSet.iloc[:577, 2].values

X_test = X[577:]
y_test = dataSet.iloc[577:, 2].values

# Classifier Multinomial Naive Bayes
classifier1 = MultinomialNB()
classifier1.fit(X_train, y_train)
y_pred1 = classifier1.predict(X_test)

accuracy1 = accuracy_score(y_test, y_pred1) * 100
print("Accuracy Multinomial = " + str(accuracy1))
print("F1 Score Multinomial = " + str(f1_score(y_test,y_pred1)))

# Classifier Naive Bayes
classifier2 = GaussianNB()
classifier2.fit(X_train, y_train)
y_pred2 = classifier2.predict(X_test)

accuracy2 = accuracy_score(y_test, y_pred2) * 100
print("Accuracy Naive Bayes = " + str(accuracy2))
print("F1 Score Naive Bayes = " + str(f1_score(y_test,y_pred2)))