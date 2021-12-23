from pathlib import Path
import nltk
from unidecode import unidecode
import re, string, unicodedata
import gensim
from gensim import models
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
global stop_words
from gensim import models
from gensim import utils
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
import copy
import re


text_files=[]
fdata = []
unigrams=[]
bigrams=[]
dict_unigrams={}
dict_bigrams={}
dict_trigrams={}
count_unigram=[]
n_grams=[]

def rawdata_read(path):
    """
    Reads a raw text file
    """
    with open(path, "r", encoding='utf8') as f:
        text=f.read().split()
        text_files.append(text)

def remove_non_ascii(rawtext):
    """
    Remove non-ASCII characters from list of tokenized words
    """
    text_removedascii = []
    for words in rawtext:
        new_word = unicodedata.normalize('NFKD', words).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        text_removedascii.append(new_word)
    return text_removedascii

def remove_numbers(withnumbers):
    """
        Remove numbers from list of tokenized words
    """
    withoutnum=[]
    for words in withnumbers:
        words=re.sub("\d+", ",", words)
        withoutnum.append(words)
    return wonum

def keep_words(tokens):
    """
    Keeps words only by removing non essential character containing words
    """
    wordsonly=[]
    wp=re.compile('([a-z][a-z]+|[A-Z][a-z]+|[A-Z][A-Z]+)')
    for words in tokens:
        if wp.match(words):
            wordsonly.append(words)
    return wordsonly

def remove_characters(text):
    """
        Removes all non essential characters form tokens
    """
    text_withoutchacters=[]
    p=re.compile('[a-z]+_[a-z]+')
    for words in text:
        temp_word=str(words)
        temp_word=temp_word.replace("(", " ")
        temp_word=temp_word.replace("~", " ")
        temp_word=temp_word.replace("{", " ")
        temp_word=temp_word.replace("}", " ")
        temp_word=temp_word.replace(")", " ")
        temp_word=temp_word.replace(",", " ")
        temp_word=temp_word.replace(":", " ")
        temp_word=temp_word.replace("[", " ")
        temp_word=temp_word.replace("]", " ")
        temp_word=temp_word.replace(".", " ")
        temp_word=temp_word.replace("%", " ")
        temp_word=temp_word.replace("?", " ")
        temp_word=temp_word.replace(";", " ")
        temp_word=temp_word.replace("/", " ")
        temp_word=temp_word.replace("\\", " ")
        temp_word=temp_word.replace("'", " ")
        temp_word=temp_word.replace("\"", " ")
        temp_word=temp_word.replace("#", " ")
        temp_word=temp_word.replace("&", " ")
        temp_word=temp_word.replace("--", " ")
        temp_word=temp_word.replace("----", " ")
        temp_word=temp_word.replace("->", " ")
        temp_word=temp_word.replace(">", " ")
        temp_word=temp_word.replace("<", " ")
        temp_word=temp_word.replace("|", " ")
        temp_word=temp_word.replace("$", " ")
        temp_word=temp_word.replace("  ", " ")
        temp_word=temp_word.replace("   ", " ")
        temp_word=temp_word.replace("__", " ")
        temp_word=temp_word.replace("___", " ")
        temp_word=temp_word.replace("    ", " ")
        temp_word=temp_word.replace("@", " ")
        temp_word=temp_word.replace("+", " ")
        temp_word=temp_word.replace("*", " ")
        temp_word=temp_word.replace(" ", " ")
        temp_word=temp_word.replace("!", " ")
        temp_word=temp_word.replace("=", " ")
        temp_word=temp_word.replace("==", " ")
        temp_word=re.sub("\d+", " ", temp_word)
        temp_word=temp_word.strip()
        temp_word=temp_word.replace(" ","")
        text_withoutchacters.append(temp_word)

    return text_withoutchacters

def removedash(text):
    t=text[0]# since there is only one file on index 0 of huge list
    n=[]
    for words in t:
        temp_word=str(words)
        temp_word=temp_word.replace("-", " ")
        temp_word=temp_word.strip()
        n.append(temp_word)
    return n


def clean_rawdata():
    i=0
    for lists in text_files:
        text_files[i]=remove_non_ascii(lists)
        i+=1
    i=0
    for lists in text_files:
        text_files[i]=remove_characters(lists)
        i+=1
    i=0
    for lists in text_files:
        abr=[words for words in lists if words.isupper()]
        text_files[i]= [words.lower() for words in lists if not words.isupper()] + abr # it will not concvert the all upercase words to lower, ( abbrivieations)
        i+=1

def stop_words_additional():
    """
    Adds more stopword from a file to existing "english" stopwords
    """
    stop_list = []
    with open(r"stoplist_new" + ".txt", "r", encoding='utf8') as f:
        stop_terms = f.read().split()
        stop_list.extend(stop_terms)
    #global stop_words
    stop_words = stopwords.words('english')
    stop_words.extend(stop_list)
    return stop_words

def stopwords_remove():
    ffdata = []
    for lists in text_files:
        temp = []
        for words in lists:
            if words not in stop_words_additional():
                temp.append(words)
                newDoc = [word for word in temp if len(word) >= 3]
        ffdata.append(newDoc)
    for lists in ffdata:
        tmp = [x for x in lists if x.strip()]
        fdata.append(tmp)

def frequence_count_unigrams():
    j=len(fdata)-4
    i=0
    for lists in fdata:
        i=i+1
        if i>j:
            break
        count_unigram=Counter(lists)
        n=len(lists)
        ulist=list(count_unigram)
        unigrams.append(ulist)
        for k in list(count_unigram):
            count_unigram[k]=int(count_unigram[k]/n*10000)
            if count_unigram[k] < 5:
                del count_unigram[k]
        dict_unigrams=dict(count_unigram.most_common())

def make_unigrams(freq):
    stopwords_remove()
    j=len(fdata)-1
    i=0
    nlist=[]
    for lists in fdata:
        for words in lists: # removing words having any nonalphanumeric character at initial position
            w=str(words)
            if w[0].isalpha():
                nlist.append(words)
        count_unigram=Counter(nlist)
        ulist=list(count_unigram)
        unigrams.append(ulist)
        f = open(r"\unigram_dict" + ".txt", "w")
        for k in list(count_unigram):
            if count_unigram[k] > 25:
                f.write("{}\n".format(k))
        for k in list(count_unigram):
            if count_unigram[k] < freq:
                del count_unigram[k]
        global dict_unigrams
        dict_unigrams=dict(count_unigram)
        copy_dict_unigrams = dict_unigrams
        for key in list(copy_dict_unigrams):
            if key + 'ing' in copy_dict_unigrams:
                frequency = copy_dict_unigrams.get(key + 'ing')
                frequency2 = copy_dict_unigrams.get(key)
                dict_unigrams[key] = frequency + frequency2
                dict_unigrams.pop(key + 'ing')

        for key in list(copy_dict_unigrams):
            if key + 'es' in copy_dict_unigrams:
                frequency = copy_dict_unigrams.get(key + 'es')
                frequency2 = copy_dict_unigrams.get(key)
                dict_unigrams[key] = frequency + frequency2
                dict_unigrams.pop(key + 'es')

        for key in list(copy_dict_unigrams):
            if key + 's' in copy_dict_unigrams:
                frequency = copy_dict_unigrams.get(key + 's')
                frequency2 = copy_dict_unigrams.get(key)
                dict_unigrams[key] = frequency + frequency2
                dict_unigrams.pop(key + 's')

def relative_unigrams(doc1):
        count_unigram=Counter(doc1)
        return count_unigram.most_common()

def clean_ngrams(s):
    chars = [',', '.', ':', '<','>','/','\\','(',')','#','$','[',']','{','}',';','%','!','®','?','&','^','+','*','=','\'','\"','|','α','β','~']
    if all(c not in s for c in chars):
        return True
def bigrams_trigrams(stop_words, bi_freq, tri_freq):
    hlist=[]
    hlist=removedash(text_files)
    biwordnonstop = [b for b in nltk.bigrams(text_files[0])]
    level1 = [list(row) for row in biwordnonstop]
    bigrams_withunderscore1 = []
    bigrams_withunderscore2 = []
    bigrams_withunderscore3 = []
    i = 0
    for bgr in level1:
        if bgr[i] not in stop_words and bgr[i+1] not in stop_words:
            bi = bgr[i] + '_' + bgr[i + 1]
            if str(bi[-1]) == "." or str(bi[-1]) == ",":
                t=str(bi[0:-1])
                bigrams_withunderscore1.append(t)
            else:
                bigrams_withunderscore1.append(bi)
    pattern = re.compile(r'^[a-z+A-Z ]+$')

    for bi in bigrams_withunderscore1:
        stri = str(bi)
        if clean_ngrams(stri) == True and stri[0].isalpha():
            bigrams_withunderscore2.append(bi.lower())
    reg = re.compile('^[a-zA-Z0-9\-_]+$')

    for big in bigrams_withunderscore2:
        if reg.match(big):
            bigrams_withunderscore3.append(big)
    count_bigrams1 = Counter(bigrams_withunderscore3)

    lis=count_bigrams1.most_common(10)
    for k in list(count_bigrams1):
         if count_bigrams1[k] < bi_freq:
             del count_bigrams1[k]
    liss = list(count_bigrams1)
    li=[]
    for k in list(count_bigrams1):
         if count_bigrams1[k] > 10:
             li.extend([k]*count_bigrams1[k])

    global dict_bigrams
    dict_bigrams=dict(count_bigrams1)
    # This code will work as a custom stemmer for bigrams and will eliminate semantically similar bigrams and
    # combine the frequency together, i.e Context_swithing and Context_switch will be combined as a Context_switch
    # and Operating_systems and Operating_system will be combined as Operating_system
    copy_dict_bigrams=dict_bigrams
    for key in list(copy_dict_bigrams):
        if key +'ing' in copy_dict_bigrams:
            frequency= copy_dict_bigrams.get(key + 'ing')
            frequency2=copy_dict_bigrams.get(key)
            dict_bigrams[key]=frequency+frequency2
            dict_bigrams.pop(key + 'ing')

    for key in list(copy_dict_bigrams):
        if key + 'es' in copy_dict_bigrams:
            frequency = copy_dict_bigrams.get(key + 'es')
            frequency2 = copy_dict_bigrams.get(key)
            dict_bigrams[key] = frequency + frequency2
            dict_bigrams.pop(key + 'es')

    for key in list(copy_dict_bigrams):
        if key + 's' in copy_dict_bigrams:
            frequency = copy_dict_bigrams.get(key + 's')
            frequency2 = copy_dict_bigrams.get(key)
            dict_bigrams[key] = frequency + frequency2
            dict_bigrams.pop(key + 's')

    triwordnonstop = [b for b in nltk.trigrams(text_files[0])]
    count_trigrams = Counter(triwordnonstop)
    level2 = [list(row) for row in triwordnonstop]
    lis2=[]
    lis1=[]
    j=0
    for bgr in level2:
        if bgr[0] not in stop_words and bgr[2] not in stop_words:

            ti=bgr[j]+'_'+bgr[j+1]+'_'+bgr[j+2]
            if str(ti[-1]) == "." or str(ti[-1]) == ",":
                t=str(ti[0:-1])
                lis1.append(t)

            else:
                lis1.append(ti)
    lis3=[]
    for tri in lis1:
        stri=str(tri)
        if clean_ngrams(stri) == True and stri[0].isalpha():
            lis2.append(tri.lower())
    reg = re.compile('^[a-zA-Z0-9\-_]+$')
    for tri in lis2:
        if reg.match(tri):
            lis3.append(tri)
    count_trigrams1=Counter(lis3)
    for k in list(count_trigrams1):
        if count_trigrams1[k] < tri_freq:
            del count_trigrams1[k]
    trilist = list(count_trigrams1)
    global dict_trigrams
    dict_trigrams=dict(count_trigrams1)

def filtered_unigrams():
    """
    This function will delete those unigrams which are part of bigrams and due to equal/slightly,
    greater frequency cannot be considered as a valid concept in unigram.
    """
    # Following lines will convert bigrams into unigrams and add the frequency if a unigram is part of two bigrams
    # for example in system appears in operating_system and in system_call, it will add both occurences of system
    text=[]
    new_dict={}
    for key, value in dict_bigrams.items():
        temp=key
        vtemp=value
        a = temp.split('_')
        for words in a:
            if words in new_dict:
                f=new_dict[words]
                new_dict[words]=f+vtemp
            else:
                new_dict[words]=vtemp
    list_for_filtering=[]
    for key, value in dict_unigrams.items():
        if key in new_dict.keys():
            if dict_unigrams[key]*0.2<= new_dict[key]:# if a unigram exist at least 50% more than the part of bigram, its valid
                list_for_filtering.append(key)
    temp_dict=dict_unigrams
    for key, value in list(temp_dict.items()):
        if key in list_for_filtering:
            del dict_unigrams[key]

def write_files(path):
    f = open(path / "myfile_unigrams.txt", "w")
    for k, v in dict_unigrams.items():
        f.write("{}\n".format(k))
    f = open(path / "myfile_unigrams_frequency.txt", "w")
    for k, v in dict_unigrams.items():
        f.write("{} {}\n".format(k, v))
    f = open(path / "myfile_bigrams.txt", "w")
    for k, v in dict_bigrams.items():
        if "_" in k:
            f.write("{}\n".format(k))
    f = open(path / "myfile_bigrams_withfrequency.txt", "w")
    for k, v in dict_bigrams.items():
        if "_" in k:
            f.write("{} {}\n".format(k, v))
    f = open(path / "myfile_trigrams.txt", "w")
    for k, v in dict_trigrams.items():
        if "_" in k:
            f.write("{}\n".format(k))
    f = open(path / "myfile_trigrams_withfrequency.txt", "w")
    for k, v in dict_trigrams.items():
        if "_" in k:
            f.write("{} {}\n".format(k, v))

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def ngrams_preparation(input_path, temp_path, unigram_frequency, bigram_frequency, trigram_frequency):
    rawdata_read(input_path)
    stopwords=stop_words_additional()
    bigrams_trigrams(stopwords, bigram_frequency, trigram_frequency)
    clean_rawdata()
    make_unigrams(unigram_frequency)
    n_grams = merge_dicts(dict_unigrams, dict_bigrams, dict_trigrams)
    f = open(temp_path / "ngrams_withfrequency.txt", "w",encoding='utf8' )
    for k, v in n_grams.items():
        k = str(k).title()
        f.write("{} {}\n".format(k, v))
    write_files(temp_path)
    filtered_unigrams()



