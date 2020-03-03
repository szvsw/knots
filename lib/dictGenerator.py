import re

# Receives a file path and generates raw text word list
# Punctuation are treated as words
# TODO: GUI should optionally define delmiters
# TODO: Delimiters should be passed in and iterated over recursively
def splitToWords(plaintext):
    plaintext = plaintext.lower()
    splittext = []
    words = re.split('(\W)',plaintext) # Uses standard regexp '\W' word def
    for word in words: # filter out unwanted chars
        if word!=' ' and word!='\r' and word!='' and word!= "." and word != "," and word != ";" and word != ":" and word != "!" and word !="?" and word!="-" and word!= "\'" and word!= "/" and word != "(" and word!=")" and word!="\"":
            if  word=='\n':
                splittext.append("\\NEWLINE")
            else:
                splittext.append(word)
        elif word == "." or word == "!" or word == "?":
            splittext.append("\\STOP")
    return splittext

# convert text list to dictionary
def createDict(wordList):
    dict = {}
    dict['\\NEWLINE'] = {'id':-1, 'count' : 0}
    dict['\\STOP'] = {'id':0, 'count' : 0}
    id = 1
    for word in wordList:
        if word in dict: # increment count
            dict[word]['count'] = dict[word]['count']+1
        else: # create entry and increment ids
            dict[word]={'id':id,'count':1}
            id = id+1
    return dict,id;
