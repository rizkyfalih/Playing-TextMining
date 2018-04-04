# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 23:35:08 2018

@author: rizkyfalih
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import xml.etree.ElementTree as ET
from xml.dom import minidom


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

def get_data_training(data):
    for i in data.index:
        data.loc[i, 'Headline'] = get_headline_training(str(data.loc[i, 'Filename']))
        data.loc[i, 'Article'] = get_article_training(str(data.loc[i, 'Filename']))

    return data        
        
trainingSet = get_data_training(label_to_binary(pd.read_csv('Dataset/Label/Label-Training.txt', delimiter = ' ')))
x
    