import re

def count_words(sentence):
    words = re.findall(r"\b(\w+'?\w*)\b", sentence.replace('_',' ').lower())

    wcount={}

    for word in words:
        if word in wcount: wcount[word]+=1
        else:              wcount[word]=1

    return wcount

 
if __name__=='__main__':
    print(count_words(",\n,one,\n ,two \n 'three'"))
    print(count_words("testing, 1, 2 testing"))