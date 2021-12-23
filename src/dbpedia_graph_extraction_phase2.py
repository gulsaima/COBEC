import rdflib
import csv
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle
from pathlib import Path
import json
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, N3, JSON
from collections import defaultdict
import itertools
from abstract_tokenizer import*
from dbpResourceFinder import*
from dbpediaqueries import*
from dbpedia_ambiguous_check import*

bothconcepts = []
others=[]
k=[]
p3=[]
refdict={}

def writeupdatedref(p):
    concepts_list={}
    with open(r"..\temp\unigram_concepts" + ".json") as f:  ## for testing put testing1 instead of results
        a=json.load(f)
        concepts_list.update(a)
    with open(r"..\temp\bigram_concepts" + ".json") as f:
        a = json.load(f)
        concepts_list.update(a)
    with open(r"..\temp\trigram_concepts" + ".json") as f:
        a = json.load(f)
        concepts_list.update(a)
    with open(r"..\output\phase2\json_bfs" + ".json") as f:
        a = json.load(f)
        concepts_list.update(a)
    new_dict = dict((k.lower(), v) for k, v in concepts_list .items())
    with open(p / "json_bfs.json", 'w') as json_file:
        json.dump(new_dict, json_file)

def read_refdic(p):
    global refdict
    with open(p / "json_bfs.json") as json_file:
        refdict=json.load(json_file)
    return refdict

def pageredirect_links(r):
    global inner_dict2
    global new_dict
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?rlinks ?label ?abstract

        WHERE 
        {   
            {
            :""" + r[1:-1] + """ dbo:wikiPageRedirects ?rlinks .
            ?rlinks rdfs:label ?label .
            ?rlinks dbo:abstract ?abstract .           
            FILTER ( lang(?label) = "en" )
            FILTER ( lang(?abstract) = "en" )
               
            }
         }   
   """)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    new_dict_list = []
    for val in result.values():
        new_dict = dict(val)
        new_dict_list.append(val)
    inner_dict = new_dict['bindings']
    for x in inner_dict:
        inner_dict2 = inner_dict[0]
    if (result['results']['bindings'] != []):
        link=inner_dict2['rlinks']['value']
        rlabel=inner_dict2['label']['value']
        abstract=inner_dict2['abstract']['value']
        return link, rlabel, abstract


def remove_underscore(word):
    temp_word = word.replace("_", " ")
    return temp_word
def update_merge(d1, d2):
    if isinstance(d1, dict) and isinstance(d2, dict):

        return {
            **d1, **d2,
            **{k: d1[k] if d1[k] == d2[k] else update_merge(d1[k], d2[k])
            for k in {*d1} & {*d2}}
        }
    else:

        return [
            *(d1 if isinstance(d1, list) else [d1]),*(d2 if isinstance(d2, list) else [d2])
        ]

wordstoremove=[]
ref_dict=[]
def refernce_dictionary(dict_items):
    global ref_dict
    for items in dict_items:
        ref_dict.append(items)
def cscoreupdated(abst):
    count = 0
    abst=[x.lower() for x in abst]
    for k, v in refdict.items():
        if k in abst:
            count = count + v

    return count, len(abst)

def csscore(abst):
    count = 0
    for words in ref_dict[0]:
        if words in abst:
            count=count+1
    for words in ref_dict[1]:
        if words in abst:
            count=count+5
    for words in ref_dict[2]:
        if words in abst:
            count=count+10
    return count, len(abst)

def cal_contextscore(abst):
   return cscoreupdated(abst)

def abstract_tokenize(*args):
    global abs_list
    if len(args)>1:
        word=args[0]
        abs_list = input(args[1])
        if word in abs_list:
            abs_list.remove(word)
    else:
        abs_list = input(str(args))

    return abs_list

def read_frequencyfile():
    concept_frequency=[]
    with open(r"..\temp\ngrams_withfrequency" + ".txt", "r") as f:
        w=f.readline().rstrip('\n')
        while w !="":
            n=w.split(' ')
            n[0]=n[0].lower().capitalize()
            n[1]=int(n[-1])
            w=list(n)
            concept_frequency.append(w)
            w = f.readline().rstrip('\n')
    return concept_frequency

combinedPool=[]
def read_unigrams():
    concepts_list = []
    with open(r"..\\temp\unigram_concepts" + ".txt") as f:
        words = f.read().split()
        concepts_list.extend(words)
    return concepts_list

def read_bigrams():
    concepts_list=[]
    with open(r"..\\temp\bigram_concepts" + ".txt") as f:
         words = f.read().split()
         concepts_list.extend(words)
    return concepts_list

def read_trigrams():
    concepts_list=[]
    with open(r"..\\temp\trigram_concepts" + ".txt") as f:
          words = f.read().split()
          concepts_list.extend(words)
    return concepts_list

def find_rank():
    unigrams=read_unigrams()
    bigrams=read_bigrams()
    trigrams=read_trigrams()
    concepts_list=unigrams+bigrams+trigrams
    import random
    from dbpedia_ambiguous_check import pageredirect_links2
    nonambiguousPool = []
    ambiguousPool = []
    count=1
    for concepts in concepts_list:
        if disambiuaty_check('"' + concepts + '"') == None and pageredirect_links2('"' + concepts + '"')==None:
            nonambiguousPool.append(concepts)
        else:
            ambiguousPool.append(concepts)
        count=count+1

    with open(r"..\\temp\Nonambiguous_concepts" + ".txt", "w",
              encoding='utf8') as f:
        for item in nonambiguousPool:
            f.write("%s\n" % item)
    with open(r"..\\temp\ambiguous_concepts" + ".txt", "w",encoding='utf8') as f:
        for item in ambiguousPool:
            f.write("%s\n" % item)

    link_list=[]
    import copy
    amp=copy.deepcopy(ambiguousPool)
    nrPool=[]
    global bothconcepts
    global others
    global k
    for w in amp:
        l = []
        link=pageredirect_linkfind('"' + w + '"')
        if link!=None:
            l.append(w)
            temp=link[1]
            temp=temp.replace(" ","_")
            temp2 = temp.replace("(", "\(")
            temp3 = temp2.replace(")", "\)")
            temp3 = temp3.replace("/","\/")
            temp3 = temp3.replace("'","\\'")
            temp3 = temp3.replace(",","\\,")
            temp3 = temp3.replace(".","\\.")
            temp3 = temp3.replace("&","\\&")
            if disambiuaty_check('"' + temp3 + '"')!=None:
                k.append(temp3)
                tup=(w,temp3)
                bothconcepts.append(tup)
            else:
                tup = (w, temp3)
                nrPool.append(tup)
                bothconcepts.append(tup)
            l.append(link)
            link_list.append(tuple(l))
        else:
            others.append(w)
    new_amb_pool=others+k
    with open(r"..\\temp\ambiguous_concepts1" + ".txt", "w",encoding='utf8') as f:
        for item in new_amb_pool:
            f.write("%s\n" % item)
    with open(r'..\\temp\nonambiguousRedirected.pickle', 'wb') as f:
        pickle.dump(nrPool, f)
    with open(r"..\\temp\nonambiguous" + ".txt", "w",encoding='utf8') as f:
        for item in nonambiguousPool:
            f.write("%s\n" % item)

def find_nonambiguousrank(p):
    with open(r'..\temp\nonambiguousRedirected.pickle', "rb") as f:
        namb_redirected = pickle.load(f)
        nscore = nonambiguous_scoreRD(namb_redirected)
    with open(r"..\temp\nonambiguous" + ".txt", "r", encoding='utf8') as f:
        namb = f.read().split()
        nonambiguous_score(namb)
    with open(r'..\temp\p3.pickle', 'wb') as f:
        pickle.dump(p3, f)
    with open(p / 'p3.pickle', 'wb') as f:
        pickle.dump(p3, f)
    return nscore

def pool1(words):
    redirected_tuple = pageredirect_links('"' + words + '"')
    if redirected_tuple != None:
        return redirected_tuple

def nonambiguous_score(na):
    napool=[]
    length=len(na)
    if length != 0:
        for words in na:
            redirected_tuple = disambiguity_concept_labstract('"' + words + '"')
            if redirected_tuple==None:
                continue
            else:
                abstract = redirected_tuple[1]
                tokens_abstract=abstract_tokenize(words,abstract)
                score=list((cal_contextscore(tokens_abstract)))
                concepts_tuple = list((words, redirected_tuple[0], score, length))
                napool.append(concepts_tuple)
    global p3
    for item in napool :
        p3.append(item)

def nonambiguous_scoreRD(na):
    narpool=[]
    length=len(na)
    if length != 0:
        for wordstuple in na:
            words=wordstuple[1]
            textlabel=wordstuple[0]
            redirected_tuple = disambiguity_concept_labstract('"' + words + '"')
            if redirected_tuple!=None:
                abstract = redirected_tuple[1]
                tokens_abstract=abstract_tokenize(words,abstract)
                score=list((cal_contextscore(tokens_abstract)))
                concepts_tuple = list((textlabel, redirected_tuple[0], score, length))
                narpool.append(concepts_tuple)
    global p3
    for item in narpool :
        p3.append(item)
    return narpool

def find_redirectedlinks(rpool):
    rdpool=[]
    length=len(rpool)
    for r_tuple in rpool:
        w=r_tuple[1]
        redirected_tuple = disambiguity_concept_labstract('"' + w + '"')
        textconcept=r_tuple[0]
        label=redirected_tuple[0]
        abstract = redirected_tuple[1]
        tokens_abstract = abstract_tokenize(w, abstract)
        score = list(cal_contextscore(tokens_abstract))
        concepts_tuple = (textconcept, label, score, length)
        rdpool.append(concepts_tuple)
    for item in rdpool:
        p3.append(item)

def links_disambiguating(link):
    concept_disambiguated = []
    concept=link[0]
    links=disambiuaty_check_forlinks(link[1])
    if links is None:
        return 1

    length_disambguited_links = len(links)
    for link in links:
        lk=pageredirect_linkfind(link)
        if lk!=None:
            redirected_tuple = disambiguity_concept_abstract(lk)
            abstract = redirected_tuple[1]
            tokens_abstract=abstract_tokenize(concept,abstract)
            score=list(cal_contextscore(tokens_abstract))
            concepts_tuple = (concept, redirected_tuple[0], score, length_disambguited_links)
            concept_disambiguated.append(concepts_tuple)
        else:
            redirected_tuple = disambiguity_concept_abstract(link)
            abstract = redirected_tuple[1]
            tokens_abstract = abstract_tokenize(concept, abstract)
            score = list(cal_contextscore(tokens_abstract))
            concepts_tuple = (concept, redirected_tuple[0], score, length_disambguited_links)
            concept_disambiguated.append(concepts_tuple)

    return concept_disambiguated

def read_ambiguousconept_file():
    with open(r"..\temp\ambiguous_concepts1" + ".txt", "r",encoding='utf8') as f:
        a=f.read().split()
        list_of_aconepts=a
    return list_of_aconepts

def abstract_score(list_of_ambiguous,p,d):
    checklist=[]
    for i in d:
        checklist.append(i[0])
    for word in list_of_ambiguous:
        if word not in checklist:
            score=final_scoring2(single_conceptcheck(word),p)

def single_conceptcheck(concept):
    concept_disambiguated = []
    newlinklist=[]
    links=disambiuaty_check('"' + concept + '"')
    for link in links:
        r= disambiguity_concept_abstract(link)
        if r!=None:
            newlinklist.append(link)
    length_disambguited_links = len(newlinklist)

    if length_disambguited_links>=1:
        for link in newlinklist:
            redirected_tuple = disambiguity_concept_abstract(link)
            label1=redirected_tuple[0]
            abstract = redirected_tuple[1]
            tokens_abstract=abstract_tokenize(concept,abstract)
            score=list(cal_contextscore(tokens_abstract))
            concepts_tuple = list((concept, redirected_tuple[0], score, length_disambguited_links))
            concept_disambiguated.append(concepts_tuple)
    finallist=[]
    otherlist=[]
    for tp in concept_disambiguated:
        if tp[0] not in others:
            for t in bothconcepts:
                if tp[0]==t[1]:
                    tp[0]=t[0]
                    finallist.append(tp)
                else:
                    otherlist.append(tp)
    for tp in otherlist:
        finallist.append(tp)
    return concept_disambiguated

def final_scoring(cd_list):
    extracted_tuples_list=[]
    length=len(cd_list)
    for x in cd_list:
        if x not in extracted_tuples_list:
            extracted_tuples_list.append(list(x))
    sum=0
    sd_list=[]
    for x in extracted_tuples_list:
        x[3]=length
        sum=sum+x[2][1]
    for x in extracted_tuples_list:
         individaul_length=x[2][1]
         similar_count=x[2][0]
         normalized_contextual_score2 = similar_count/individaul_length
         x[2][0] = normalized_contextual_score2+x[2][0]
         sd_list.append(x[2][0])
    extracted_tuples_list2=sorted(extracted_tuples_list, key=lambda x: x[2][0], reverse=True)
    return extracted_tuples_list2
p3=[]

def pool3(ms):
    global p3
    p3.append(ms)

def update_dictionary(wordtr):
    global ref_dict
    ref_dict[0]=list(filter(lambda x: x not in wordtr, ref_dict[0]))
    ref_dict[1]=list(filter(lambda x: x not in wordtr, ref_dict[1]))

def normalizer(l, al):
    b=1
    n=1-b+b * (l/al)
    return n

def normalizer2(x,y):
    r=x/y
    return r

def final_scoring2(cd_list,p):
    extracted_tuples_list=[]
    length=len(cd_list)
    for x in cd_list:
        extracted_tuples_list.append(list(x))
    sum=0
    sd_list=[]
    if len(extracted_tuples_list)>1:
        for x in extracted_tuples_list:
            x[3]=length
            sum=sum+x[2][1]
        for x in extracted_tuples_list:
             individaul_length=x[2][1]
             average=sum/x[3]
             similar_count=x[2][0]
             normalized_contextual_score2 = similar_count/individaul_length
             x[2][0] = normalized_contextual_score2+x[2][0]
             sd_list.append(x[2][0])
        extracted_tuples_list2=sorted(extracted_tuples_list, key=lambda x: x[2][0], reverse=True)
        import statistics
        if len(extracted_tuples_list2)==1:
            max_scorer=extracted_tuples_list2[0]
        else:
            sd = statistics.stdev(sd_list)
            for x in extracted_tuples_list2:
                if x[2][0]<sd:
                    wordstoremove.append(x[1])
            max_scorer=extracted_tuples_list2[0]
        nl=[]
        if max_scorer[0] not in others:
            for t in bothconcepts:
                if max_scorer[0] == t[1]:
                    max_scorer[0] = t[0]
                    nl.append(max_scorer)
        p3.append(tuple(max_scorer))
        if len(p3)!=1:
            with open(p / 'ambiguous_concepts.pickle', 'rb') as f:
                d = pickle.load(f)
            d.append(max_scorer)
            with open(p / 'ambiguous_concepts.pickle', 'wb') as f:
                pickle.dump(d,f)
        else:
            return p3
    else:
        if not extracted_tuples_list:
            return p3
        else:
            p3.append(extracted_tuples_list[0])
            return p3

def merging(final_rank):
    for t in final_rank:
        if t[0] in k:
            for tpl in bothconcepts:
                if t[0] == tpl[1]:
                    t[0] = tpl
    fr = list(final_rank for final_rank, _ in itertools.groupby(final_rank))
    elements = []
    for t in fr:
        elements.append(t[1])
    elements = dict(Counter(elements))
    elements = {key: val for key, val in elements.items() if val > 1}

    A = []
    for e in elements:
        for c in fr:
            if c[1] == e:
                A.append(c)
    B = list(filter(lambda x: x not in A, fr))
    temp3 = []

    def merge(a, b):
        temp = a
        temp2=[]
        temp2.append(temp[0])
        for r in b:
            if a[1] == r[1]:
                temp2.append(r[0])
        temp[0]=temp2
        temp3.append(temp[1])
        if temp3.count(temp[1])<=1:

            return temp
    lofa=len(A)
    for i in range(lofa):
        j = i + 1
        remaining=A[j:lofa]
        n = merge(A[i], remaining)
        if n != None:
            B.append(n)
    rank_dict = {}
    count = 1
    B = sorted(B, key=lambda x: x[2][0], reverse=True)
    for line in B:
        rank_dict.update({count: (line[0], line[1])})
        count = count + 1
    return rank_dict

def forjson(dd):
    rank_dict = {}
    count = 1
    for line in dd:
        rank_dict.update({count: line[0]})
        count = count + 1
    return rank_dict

def merge_rank(fr):
    elements=[]
    for t in fr:
        elements.append(t[1])
    elements = dict(Counter(elements))
    elements = {key: val for key, val in elements.items() if val > 1}
    for k,v in elements.items():
        r = 0
        for x in fr:
            if k==x[1]:
                r+=x[2][0]
        for x in fr:
            if k==x[1]:
                x[2][0]=r
    return fr

def updatedcontext(path):
    writeupdatedref(path)
    read_refdic(path)

def abstract_score_firstambiguous(w,p):
    score=final_scoring2(single_conceptcheck(w),p)
    return score

def ranking_phase2(p):
    updatedcontext(p)
    find_rank()
    ambiguous_concepts = read_ambiguousconept_file()
    first_ambiguous_concept = ambiguous_concepts[0]
    if ambiguous_concepts:
        my_file = Path(p / 'ambiguous_concepts.pickle')
        if not my_file.is_file():
            first = abstract_score_firstambiguous(first_ambiguous_concept, p)
            with open(p / 'ambiguous_concepts.pickle', 'wb') as f:
                pickle.dump(first, f)
        with open(p / 'ambiguous_concepts.pickle', 'rb') as f:
            disambiguated = pickle.load(f)
        abstract_score(ambiguous_concepts, p, disambiguated)
    ns = find_nonambiguousrank(p)
    with open(p / 'nonambi.pickle', 'wb') as f:
        pickle.dump(ns, f)
    with open(p / 'p3.pickle', 'rb') as f:
        nam = pickle.load(f)
    with open(p / 'ambiguous_concepts.pickle', 'rb') as f:
        disambiguated_final = pickle.load(f)
    final_pool = nam + disambiguated_final + ns
    final_rank = final_scoring(final_pool)
    for row in final_rank:
        if "_" in row[0]:
            row[2][0] = row[2][0] + 1
    sorted_final_rank = sorted(final_rank, key=lambda x: x[2][0], reverse=True)
    final_rank = []
    for rank_of_word in sorted_final_rank:
        if rank_of_word[2][0] > 0.0:
            rank_of_word[2][0] = int(rank_of_word[2][0])
            final_rank.append(rank_of_word)
    final_rank = merge_rank(final_rank)
    final_rank = sorted(final_rank, key=lambda x: x[2][0], reverse=True)
    new_fr = []
    for t in final_rank:
        if t not in new_fr:
            new_fr.append(t)
    new_fr = sorted(new_fr, key=lambda x: x[2][0], reverse=True)
    merged_ranked_concepts = merging(new_fr)
    with open(p / "ranked_concepts.json", 'w') as json_file:
        json.dump(merged_ranked_concepts, json_file)
    return merged_ranked_concepts

