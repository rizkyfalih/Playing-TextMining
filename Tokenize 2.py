from nltk.tokenize import word_tokenize

with open('Data_PR_5FebIF2.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')

tokens_data = word_tokenize(data.lower())
sorted_tokens_data = sorted(tokens_data)
complete_tokens = []


for k in range(len(sorted_tokens_data)):
    if k+1 < len(sorted_tokens_data):      
        if sorted_tokens_data[k+1] != sorted_tokens_data[k]:
            complete_tokens.append(sorted_tokens_data[k+1])
    else:
        if sorted_tokens_data[k] != sorted_tokens_data[k]:
            complete_tokens.append(sorted_tokens_data[k])

print(complete_tokens)

#Stupid logic:
#print(set(sorted_tokens_data))