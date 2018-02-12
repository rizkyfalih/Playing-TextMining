from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import csv

def main():
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()
    
    text = 'I worked hard'
    words = word_tokenize(text)

    for w in words:
        print(ps.stem(w))
    print('========================')
    for i in words: 
        print(lemmatizer.lemmatize(i))

main()