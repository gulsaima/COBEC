import nltk
#from textblob import TextBlob
from unidecode import unidecode
import re, string, unicodedata
import gensim
from gensim import models
from collections import Counter
from nltk.corpus import stopwords
global newDoc

def input(in_tex):
    clean=clean_data(in_tex)
    clean2=clean
    clean.extend(make_bigrams(clean))
    clean.extend(make_trigrams(clean2))
    return clean


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

    #############################################################################


def remove_numbers(wnumbers):
    wonum = []
    for words in wnumbers:
        words = re.sub("\d+", ",", words)
        wonum.append(words)
    return wonum

    ##############################################################################


def keep_words(wordsonly):
    wonly = []
    wp = re.compile('([a-z][a-z]+|[A-Z][a-z]+|[A-Z][A-Z]+)')
    for words in wordsonly:
        if wp.match(words):
            wonly.append(words)
    return wonly


def keep_words1(text):
    text1 = []
    p = re.compile('[a-z]+_[a-z]+')
    for words in text:
        temp_word = str(words)
        temp_word = temp_word.replace("(", " ")
        temp_word = temp_word.replace(")", " ")
        temp_word = temp_word.replace(",", " ")
        temp_word = temp_word.replace(":", " ")
        temp_word = temp_word.replace("[", " ")
        temp_word = temp_word.replace("]", " ")
        temp_word = re.sub('[%s]' % re.escape(string.punctuation), '', temp_word)
        temp_word = re.sub("\d+", " ", temp_word)
        temp_word = temp_word.strip()

        text1.append(temp_word)

    return text1

    ############################################################################


def clean_rawdata(lists):
    new_list = []
    new_list = remove_non_ascii(lists)
    new_list = keep_words1(new_list)
    new_list = stopwords_remove(new_list)
    new_list = [words.title() for words in new_list]
    return new_list

def stopwords_remove(list1):
    tmp = []
    stop_words = stopwords.words('english')
    temp = []
    global newDoc

    for words in list1:
        if words not in stop_words:
            temp.append(words)
    newDoc = [word for word in temp if len(word) >= 3]
    tmp = [x for x in newDoc if x.strip()]
    return tmp


def length_of_tokens(list1):
    print(len(list1))


def clean_data(text):
    tokens=text.split()
    nlist=clean_rawdata(tokens)
    return nlist

def make_bigrams(list):

    biwordnonstop = [b for b in nltk.bigrams(list)]  # its a list of tuples
    bigrams_withunderscore = []
    for bgr in biwordnonstop:
        bi = bgr[0] + '_' + bgr[1].lower()
        bigrams_withunderscore.append(bi)
    return bigrams_withunderscore

def make_trigrams(list):
    triwordnonstop = [t for t in nltk.trigrams(list)]
    trigrams_withunderscore = []
    for tgr in triwordnonstop:
        ti = tgr[0]+'_'+tgr[1].lower()+'_'+tgr[2].lower()
        trigrams_withunderscore.append(ti)
    return trigrams_withunderscore
#def main():

#if __name__ == "__main__":
    main()