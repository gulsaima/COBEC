import rdflib
import csv
import json
import ssl
import certifi
from nltk import word_tokenize, pos_tag
import nltk
from unidecode import unidecode
import unicodedata
ssl._create_default_https_context = ssl._create_unverified_context
from SPARQLWrapper import SPARQLWrapper, N3, JSON
def rf(st):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core:>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>

    PREFIX : <http://dbpedia.org/resource/>
        SELECT  ?label ?s 
        WHERE 
            {   
                                                                                                                                                                                                                                                                                                                                                                                                                
                { :"""+st[1:-1]+""" rdfs:label ?label .
                  #:"""+st[1:-1]+""" rdf:type ?type .
                        
                 FILTER ( lang(?label) = "en" )
                 #FILTER ( ?type != dbo:Place )
                 }
               
                UNION
                     {
                     ?altName rdfs:label """+st+"""@en ;
                        dbo:wikiPageRedirects ?s .
                      }           
            }    

   """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    if (result['results']['bindings']!= []):
        return True

def input_unigrams(path):

        concepts, nonconcepts, concepts1=([] for i in range(3))
        with open(path / "myfile_unigrams.txt") as f:
            words = f.read().split()
            concepts1.extend(words)
        abr = [words for words in concepts1 if words.isupper()]
        concepts1 = [word.capitalize() for word in concepts1 if not word.isupper()]+abr
        for words in concepts1:
            if (rf('"'+words+'"')==True):
                concepts.append(words)
            else:
                nonconcepts.append(words)

        with open(path / "unigram_concepts.txt", "w", encoding='utf8') as f:

            for item in concepts:
                if len(item)>=3:
                    f.write("%s\n" % item)
        ndic = {}
        for item in concepts:
            ndic[item] = 1

        with open(path / "unigram_concepts.json", 'w') as json_file:
            json.dump(ndic, json_file)

        data_nouns_adj=[]
        for cpt in concepts:
            data_nouns_adj.append(nouns_adj(cpt))
        with open(path / "unigram_concepts_filtered.txt","w") as f:
            for item in data_nouns_adj:
                if len(item)>3:
                    f.write("%s\n" % item)
def write_initialcontext(path, outpath):
    initial_context={}
    with open(path / "unigram_concepts.json") as json_file:
        refdict=json.load(json_file)
        initial_context.update(refdict)
    with open(path / "bigram_concepts.json") as json_file:
        refdict = json.load(json_file)
        initial_context.update(refdict)
    with open(path / "trigram_concepts.json") as json_file:
        refdict = json.load(json_file)
        initial_context.update(refdict)
    initial_context = dict((k.lower(), v) for k, v in initial_context.items())
    with open(outpath / "initial_context.json", 'w') as json_file:
        json.dump(initial_context, json_file)


def nouns_adj(text):
    '''Given a string of text, tokenize the text and pull out only the nouns and adjectives.'''
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'VBG'
    tokenized = word_tokenize(text)
    nouns_adj = [word for (word, pos) in pos_tag(tokenized) if is_noun_adj(pos)]
    return ' '.join(nouns_adj)

def input_bigrams(path):
        concepts, nonconcepts, concepts1,concepts2=([] for i in range(4))
        with open(path / "myfile_bigrams.txt") as f:
            words = f.read().split("\n")
            concepts1.extend(words)
        concepts1 = [word.capitalize() for word in concepts1]
        for words in concepts1:
            temp_word = str(words)
            temp_word = temp_word.replace(" ", "-")
            concepts2.append(temp_word)
        for words in concepts2:
            if (rf('"'+words+'"')==True):
                concepts.append(words)
            else:
                nonconcepts.append(words)
        with open(path / "bigram_concepts.txt", "w", encoding='utf8') as f:
            for item in concepts:
                if len(item)>3 and "_" in item:
                    f.write("%s\n" % item)
        ndic = {}
        for item in concepts:
            ndic[item] = 2
        with open(path / "bigram_concepts.json", 'w') as json_file:
            json.dump(ndic, json_file)
        return concepts

def input_trigrams(path):
    concepts, nonconcepts, concepts1,concepts2=([] for i in range(4))
    with open(path / "myfile_trigrams.txt") as f:
        words = f.read().split("\n")
        concepts1.extend(words)
    concepts1 = [word.capitalize() for word in concepts1]
    for words in concepts1:
        temp_word = str(words)
        temp_word = temp_word.replace(" ", "-")
        concepts2.append(temp_word)
    for words in concepts2:
        if (rf('"'+words+'"')==True):
            concepts.append(words)
        else:
            nonconcepts.append(words)
    with open(path / "trigram_concepts.txt", "w", encoding='utf8') as f:
        for item in concepts:
            if len(item)>3 and "_" in item:
                f.write("%s\n" % item)
    ndic = {}
    for item in concepts:
        ndic[item] = 3

    with open(path / "trigram_concepts.json", 'w') as json_file:
        json.dump(ndic, json_file)

def dbpedia_existence_check(temp_path, outputpath):
    input_unigrams(temp_path)
    input_bigrams(temp_path)
    input_trigrams(temp_path)
    write_initialcontext(temp_path, outputpath)

