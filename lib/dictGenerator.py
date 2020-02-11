import re

# Receives a file path and generates raw text word list
# Punctuation are treated as words
def splitToWords(plaintext):
    splittext = []
    words = re.split('(\W)',plaintext)
    for word in words:
        # GUI should optionally define delmiters
        # Delimiters should be passed in and iterated over recursively
        if word!=' ' and word!='\n' and word!='\r' and word!='\r\n' and word!='':
            splittext.append(word)
    return splittext

# convert text list to dictionary
def createDict(wordList):
    dict = {}
    id=0
    for word in wordList:
        if word in dict:
            dict[word]['count'] = dict[word]['count']+1
        else:
            dict[word]={'id':id,'count':1}
            id = id+1
    return dict,id;
