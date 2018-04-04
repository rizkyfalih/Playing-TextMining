from nltk.tokenize import word_tokenize
import tinysegmenter
segmenter = tinysegmenter.TinySegmenter()
print(' | '.join(segmenter.tokenize(u"私の名前は中野です")))

text_arabian = "ذهبت إلى السوق"
text_japan = "私は市場に行った"
text_english = "I go to the market"
text_indonesian = "Saya pergi ke pasar"

tokens_arabian = word_tokenize(text_arabian)
tokens_japan = word_tokenize(text_japan)
tokens_english = word_tokenize(text_english)
tokens_indonesian = word_tokenize(text_indonesian)

print(tokens_arabian)
print(tokens_japan)
print(tokens_english[:2])
print(tokens_indonesian)