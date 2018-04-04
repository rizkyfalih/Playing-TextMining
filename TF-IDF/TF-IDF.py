
import re
import string
from collections import OrderedDict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import xlsxwriter

listKata = []
listKataPerArtikel = []
jumPerArtikel = []
tandaBaca = set(string.punctuation)
tandaBaca.add("--")
tandaBaca.add("...")
tandaBaca.add("-")
stopWords = set(stopwords.words('english'))
stopWords.add("'s")

for i in range(5): 
    FILE = str(i+1)+".txt"
    txt = None
    token = None
    kataArtikel =[]
    with open(FILE, 'r') as file:
        txt = file.read()
        
    txt = txt.lower()

    txt = re.sub(r'\d+', '', txt)
    token = word_tokenize(txt)
    
    token = list(OrderedDict.fromkeys(token))
    token = sorted(token,key=str.lower)
    filter =[]
    for w in token:
        if w not in stopWords:
            if w not in tandaBaca:
                filter.append(w)
            
    token = filter

    ps = PorterStemmer()
    
    for kt in token :
        listKata.append(ps.stem(kt))
        kataArtikel.append(ps.stem(kt))
        
    listKataPerArtikel.append(kataArtikel)
    jumPerArtikel.append(Counter(kataArtikel)) 
        
    
listKata = sorted(listKata)
count = Counter(listKata)
print("")

unik = list(OrderedDict.fromkeys(listKata))
h = len(unik)
w = 6
TF = [[0 for x in range(w)] for y in range(h)]
for i in range(h):
    TF[i][0] = unik[i]
    k = unik[i]
    for j in range(5):
        if k not in listKataPerArtikel[j]:
            TF[i][j+1] = 0
        if k in listKataPerArtikel[j]:
            TF[i][j+1] = jumPerArtikel[j].__getitem__(k)
            
workbook = xlsxwriter.Workbook('Hasil_TF.xlsx')
worksheet = workbook.add_worksheet()

row = 0

for col, data in enumerate(TF):
    worksheet.write_column(row, col, data)

workbook.close()
print("Hasil_TF.xlsx Created")