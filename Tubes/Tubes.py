# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 23:35:08 2018

@author: rizkyfalih
"""

# Importing the libraries
import pandas as pd
import re

# Importing nltk libraries
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Importing xml libraries
from xml.dom import minidom

# Importing classification libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB

def label_to_binary(data):
    for i in data.index:
        if(data.loc[i,'Label'] == "YES"):
            data.loc[i, 'Binary'] = 1
        else:
            data.loc[i, 'Binary'] = 0
    return data

def get_headline_training(filename):
    xmldoc = minidom.parse('Dataset/Training-Set/'+ filename + '.xml')
    headlineList = xmldoc.getElementsByTagName('headline')
    headline = ""
    for i in range(0, len(headlineList)):
        headline += headlineList[i].firstChild.nodeValue
    
    return headline
 
def get_article_training(filename):
    xmldoc = minidom.parse('Dataset/Training-Set/'+ filename + '.xml')
    paragraphList = xmldoc.getElementsByTagName('p')
    paragraph = ""
    for i in range(0, len(paragraphList)):
        paragraph += paragraphList[i].firstChild.nodeValue
    
    return paragraph

def get_headline_testing(filename):
    xmldoc = minidom.parse('Dataset/Testing-Set/'+ filename + '.xml')
    headlineList = xmldoc.getElementsByTagName('headline')
    headline = ""
    for i in range(0, len(headlineList)):
        headline += headlineList[i].firstChild.nodeValue
    
    return headline
 
def get_article_testing(filename):
    xmldoc = minidom.parse('Dataset/Testing-Set/'+ filename + '.xml')
    paragraphList = xmldoc.getElementsByTagName('p')
    paragraph = ""
    for i in range(0, len(paragraphList)):
        paragraph += paragraphList[i].firstChild.nodeValue
    
    return paragraph

def join_all_text_training(filename):
    corpus = ""
    # Get headline
    corpus += get_headline_training(filename)
    # Get article and join with headline
    corpus = " " + get_article_training(filename)
    
    return corpus

def join_all_text_testing(filename):
    corpus = ""
    # Get headline
    corpus += get_headline_testing(filename)
    # Get article and join with headline
    corpus = " " + get_article_testing(filename)
    
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

def get_data_training(data):
    for i in data.index:
        data.loc[i, 'Corpus'] = join_all_text_training(str(data.loc[i, 'Filename']))
        
    return data       

def get_data_testing(data):
    for i in data.index:
        data.loc[i, 'Corpus'] = join_all_text_testing(str(data.loc[i, 'Filename']))
        
    return data       

def bag_of_words(corpus):
    cv = CountVectorizer(max_features = 1237)
    X = cv.fit_transform(corpus).toarray()
    
    return X

# Initialize Data Training
trainingSet = get_data_training(label_to_binary(pd.read_csv('Dataset/Label/Label-Training.txt', delimiter = ' ')))
corpusTraining = cleaned_text(trainingSet)
X_train = bag_of_words(corpusTraining)
y_train = trainingSet.iloc[:, 2].values

# Initialize Data Testing
testingSet = get_data_testing(label_to_binary(pd.read_csv('Dataset/Label/Label-Testing.txt', delimiter = ' ')))
corpusTesting = cleaned_text(testingSet)
X_test = bag_of_words(corpusTesting)
y_test = testingSet.iloc[:, 2].values

# Classifier Multinomial Naive Bayes
classifier = MultinomialNB()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

cm1 = confusion_matrix(y_test, y_pred)
accuracy1 = ((cm1[0][0]+cm1[1][1])/len(X_test))*100
print("Accuracy Multinomial = " + str(accuracy1))

# Classifier Naive Bayes
classifier = GaussianNB()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

cm2 = confusion_matrix(y_test, y_pred)
accuracy2 = ((cm2[0][0]+cm2[1][1])/len(X_test))*100
print("Accuracy Naive Bayes = " + str(accuracy2))