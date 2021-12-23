import networkx as nx
import matplotlib.pyplot as plt
from SPARQLWrapper import SPARQLWrapper, N3, JSON
import json
import ssl
import certifi
import operator
import statistics
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
ssl._create_default_https_context = ssl._create_unverified_context

eigen_score=[]
indegree_score=[]
closeness_score=[]
list_tofind_ranking=[]
graph_list=[]

def graph_forlabel(label):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?parentl ?gplabel ?label 
        #?gparentl
        #?nt ?ntl

        WHERE 
            {   

                 { 
                 :""" + label[1:-1] + """ dct:subject ?pconcept .

                 ?pconcept rdfs:label ?parentl . 
                 ?pconcept skos:broader ?gpconcept .
                 ?gpconcept skos:prefLabel ?gplabel . 
                 #FILTER ( lang(?parentl) = "en" )
                 #FILTER (lang(?gparentl) ="en" )
                }

            } ORDER BY ?pconcept

   """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    new_dict_list = []
    for val in result.values():
        new_dict = dict(val)
        new_dict_list.append(val)
    inner_dict = new_dict['bindings']
    if (result['results']['bindings'] != []):
        return inner_dict


def graph_forlink(link):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>

    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?parentl ?gplabel ?label 

        WHERE 
            {   

                 { 
                 <""" + link + """>  dct:subject ?pconcept .
                 <""" + link + """>  rdfs:label ?label .

                 ?pconcept rdfs:label ?parentl . 
                 ?pconcept skos:broader ?gpconcept .
                 ?gpconcept skos:prefLabel ?gplabel . 
                 FILTER ( lang(?label) = "en" )

                 FILTER (lang(?gplabel) ="en" )
                 FILTER (lang(?parentl) ="en" )
                }

            } ORDER BY ?pconcept

   """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    new_dict_list = []
    for val in result.values():
        new_dict = dict(val)
        new_dict_list.append(val)
    inner_dict = new_dict['bindings']
    if (result['results']['bindings'] != []):
        return inner_dict
    else:
        return None
def graph_construct_labels(words):
    dict_to_label={}
    dict1 = graph_forlabel('"' + words + '"')
    try:
        for i in dict1:
            dict_to_label.update(i.items())
    except TypeError:
        return 1
    dict2 = {}
    parent = {}
    gparent = []
    combined = {}
    for i in dict1:
        r = 'default'
        dict2.update(i.items())
        p = dict2['parentl']['value']
        gp = dict2['gplabel']['value']
        if p in parent:
            r = p
            gparent.append(gp)
            parent[p] = list(x for x in gparent)
        else:
            parent.update({p: gp})
            gparent.append(gp)
    final_dict={words:dict(parent)}
    import numpy as np
    g = nx.DiGraph(final_dict)#created an empty graph
    from collections import Mapping
    q = list(final_dict.items())
    while q:
        v, d = q.pop()
        for k, vs in d.items():
            for x in vs:
                g.add_edge(k, x)
    nx.draw(g, with_labels=True)
    #plt.draw()
    #plt.show()
    return final_dict
def graph_construct_links(links):
    dict_to_label={}
    dict1 = graph_forlink(links)
    if dict1 != None:
        for i in dict1:
            dict_to_label.update(i.items())
    else:
        return
    try:
        for i in dict1:
            if dict1 == None:
                break
            dict_to_label.update(i.items())
    except TypeError:
         print("That is a redirected page and has no properties")
    dict2 = {}
    parent = {}
    gparent = []
    for i in dict1:

        dict2.update(i.items())
        r = 'default'
        p = dict2['parentl']['value']
        gp = dict2['gplabel']['value']
        label=dict2['label']['value']
        if p in parent:
            r = p
            gparent.append(gp)
            parent[p] = list(x for x in gparent)
        else:
            gparent.append(gp)
            parent[p]=list(x for x in gparent)
    final_dict={label:dict(parent)}
    g=nx.DiGraph(final_dict)
    q = list(final_dict.items())
    while q:
        v, d = q.pop()
        for k, vs in d.items():
            for x in vs:
                g.add_edge(k, x)
    return final_dict
def extract_nested_dictionaries(final_d):
    g=nx.DiGraph(final_d)
    q = list(final_d.items())
    while q:
        v, d = q.pop()
        for k, vs in d.items():
            for x in vs:
                g.add_edge(k, x)
    nx.draw(g, with_labels=True)
    plt.draw()
    plt.show()
    closeness_centrality = nx.closeness_centrality(g)
    eigen_centrality=nx.eigenvector_centrality_numpy(g)
    sorted_eigen = sorted(eigen_centrality.items(), key=lambda kv: kv[1], reverse=True)
    sorted_closeness=sorted(closeness_centrality.items(), key=lambda kv: kv[1], reverse=True)
    order = nx.topological_sort(g)
    size = g.number_of_nodes()
    degrees = [val for (node, val) in g.degree()]
    my_degree=g.degree()
    degree_values = [v for k, v in my_degree]
    sorted_degree=sorted(g.degree, key=lambda x: x[1], reverse=True)
    count=0
    for key, value in eigen_centrality.items():
        count+=1
    global indegree_score
    indegree_score=sorted_degree
    global eigen_score
    eigen_score=sorted_eigen
    global closeness_score
    closeness_score=sorted_closeness

def combined_graph(h,g):
    h=nx.DiGraph(h)
    g=nx.DiGraph(g)
    combined= nx.compose(h,g)
    nx.draw(combined, with_labels=True)
    plt.draw()
    plt.show()

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

def contextupdate(path):

    def url_extract(st):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX cat: <http://dbpedia.org/resource/Category:>
    
        PREFIX : <http://dbpedia.org/resource/>
            SELECT  ?link1
    
            WHERE 
                {   
                    {                                                                                                                                                                                                                                                                                                                                                                                               
                     ?link1 rdfs:label """+st+"""@en.
                     
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
        inner_dict2 = []
        for x in range(len(inner_dict)):
            temp = inner_dict[x]
            inner_dict2.append(temp['link1']['value'])
        if (result['results']['bindings'] != []):
            return inner_dict2
    def extract_nested_dictionaries(final_d):
        g=nx.DiGraph(final_d)
        q = list(final_d.items())

        while q:
            v, d = q.pop()
            for k, vs in d.items():
                for x in vs:
                    g.add_edge(k, x)
        nx.draw(g, with_labels=True)
        #plt.draw()
        #plt.show()

        g2=g.to_undirected()
        nx.draw(g, with_labels=True)
        #plt.draw()
        #plt.show()
        Gc = max(nx.connected_component_subgraphs(g2), key=len)
        nx.draw(Gc, with_labels=True)
        #plt.draw()
        #plt.show()

        T = nx.minimum_spanning_tree(Gc)
        nx.draw(T, with_labels=True)
        #plt.draw()
        #plt.show()


        information_centailty=nx.information_centrality(Gc)
        ic=sorted(information_centailty.items(), key=lambda kv: kv[1], reverse=True)
        closeness_centrality = nx.closeness_centrality(Gc)
        cc=sorted(closeness_centrality.items(), key=lambda kv: kv[1], reverse=True)
        eigen_centrality=nx.eigenvector_centrality_numpy(Gc)
        ec=sorted(eigen_centrality.items(), key=lambda kv: kv[1], reverse=True)
        kcen2=nx.katz_centrality_numpy(Gc)
        kc=sorted(kcen2.items(), key=lambda kv: kv[1], reverse=True)
        bcc=nx.betweenness_centrality(Gc)
        bc=sorted(bcc.items(), key=lambda kv: kv[1], reverse=True)
        rw=nx.pagerank_numpy(Gc)
        pc=sorted(rw.items(), key=lambda kv: kv[1], reverse=True)
        size = g2.number_of_nodes()
        size2 = Gc.number_of_nodes()
        degrees = [val for (node, val) in g2.degree()]
        my_degree = g2.degree()
        degree_values = [v for k, v in my_degree]
        inc = sorted(g2.degree, key=lambda x: x[1], reverse=True)
        mat=[]
        res =  [list(elem) for elem in ic[:5]]
        mat.append(res)
        res =  [list(elem) for elem in bc]
        mat.append(res[:5])
        res =  [list(elem) for elem in cc]
        mat.append(res[:5])
        res =  [list(elem) for elem in kc]
        mat.append(res[:5])
        res =  [list(elem) for elem in ec]
        mat.append(res[:5])
        res =  [list(elem) for elem in pc]
        mat.append(res[:5])
        for x in mat:
            index=1
            for i in x:
                i[1]=i[1]/index
                index=index+1
        mat = [item for items in mat for item in items]
        totals = {}
        for key, value in mat:
            totals[key] = totals.get(key, 0) + value
        root=max(totals, key=totals.get)
        sour=max(eigen_centrality.items(), key=operator.itemgetter(1))[0]
        bg=nx.bfs_tree(Gc,root)
        bg2 = bg.to_undirected()
        nx.draw(bg, with_labels=True)

        #plt.draw()
        #plt.show()
        log=len(bg2)
        import queue
        def bfs_connected_component(graph, start):
            # keep track of all visited nodes
            explored = []
            node_dic= {}
            queue = [start]
            pp= Gc.number_of_nodes()
            node_dic[start] = pp
            # keep looping until there are nodes still to be checked
            while queue:
                node = queue.pop(0)
                if node not in explored:
                    # add node to list of checked nodes
                    explored.append(node)
                    neighbours = graph[node]

                    # add neighbours of node to queue
                    for neighbour in neighbours:

                        if neighbour not in explored:
                            queue.append(neighbour)
                            node_dic[neighbour]=node_dic[node]-1
            catlist=[]
            for k, v in node_dic.items():
                str1=k
                if "(" in str1:
                    str2=str1.split("(")[1].split(")")[0]
                    catlist.append(str2)
            catlist2=[]
            for word in catlist:
                w=str(word)
                w=w.capitalize()
                if " " in w:
                    w2=w.replace(" ", "_")
                    catlist2.append(w2)
                else:
                    catlist2.append(w)
            with open(r"..\temp\catlist" + ".txt", "w") as ff:
                for w in catlist2:
                    ff.write("%s\n" % w)
            with open(r"..\temp\levelsdic" + ".txt", "w", encoding='utf8') as f:
                for k, v in node_dic.items():
                    f.write("{} {}\n".format(k,v))
            node_dic_with_underscore={}
            # These lines will remove the category information from the keys and add underscore replacing whitespaces and write the json file to the disk#
            for k,v in node_dic.items():
                s = str(k)
                split_s=s.split("(",1)
                sstring=split_s[0]
                sstring = sstring.rstrip()
                fs = sstring.replace(" ","_")
                if fs not in node_dic_with_underscore:
                    node_dic_with_underscore[fs] = v
            with open(r"..\output\phase2\json_bfs" + ".json", 'w') as json_file:
                json.dump(node_dic_with_underscore, json_file)
            catdic={}
            for item in catlist2:
                catdic[item]=15
            with open(r"..\temp\catagories" + ".json", 'w') as json_file:
                json.dump(catdic, json_file)
            l=["a","b"]
            ndic={}
            for item in l:
                ndic[item]=1
            return node_dic
        bfs_connected_component(Gc, root)
        sorted_eigen = sorted(eigen_centrality.items(), key=lambda kv: kv[1], reverse=True)
        sorted_closeness=sorted(closeness_centrality.items(), key=lambda kv: kv[1], reverse=True)
        order = nx.topological_sort(g)
        f = open(r"..\temp\updated-ref" + ".txt", "w", encoding='utf-8')
        for x in inc:
            y=str(x[0])
            y=y.replace(" ", "_")
            f.write("{}\n".format(y))
        count=0
        ##To maintain a dictionay of terms which will be used to validate the ambigous terms
        for key, value in eigen_centrality.items():
            count+=1
        global indegree_score
        indegree_score=inc
        global eigen_score
        eigen_score=sorted_eigen
        global closeness_score
        closeness_score=sorted_closeness
    list1=[]
    with open(path / "ranked_concepts.json") as json_file:
        inputfile=json.load(json_file)
    for key,value in inputfile.items():
        if key in ['1','2','3','4','5']:
            list1.append(value)
    newlist1=[]
    newlist2=[]
    for item in list1:
        for x in item:
            if type(x) is list:
                for y in x:
                    newlist1.append(y)
            else:
                newlist2.append(item[-1])
    newlist2=set(newlist2)
    gl=[]
    for words in newlist2:
        gl.append(words)
        temp=str(words)
        temp=temp.replace(" ", "_")
        r=url_extract('"'+words+'"') ## This will extract all the links associated with the concepts ( wikidata links and others as well
        import re
        n=r
        m=[]
        for x in n:
            t=str(x)
            c = re.findall('http://dbpedia.org/resource/',t)
            if c!=[]:
                m.append(x)

        for x in m:
            t=str(x)
            c = re.findall('Category', t)
            if c != []:
                m.remove(x)
        for link in m:
            value=graph_construct_links(link)
            if value!=None:
                graph_list.append(graph_construct_links(link))
    result = graph_list[0]
    j = 1
    for j in range(len(graph_list)):
        result = update_merge(result, graph_list[j])
    g = nx.DiGraph(result)
    nx.draw(g, with_labels=True)
    #plt.draw()
    #plt.show()
    extract_nested_dictionaries(result)
    indegree = []
    eigen = []
    closness = []
    med_score_list = []
    score_list = []
    for words in gl:
        indegree1 = [item for item in indegree_score if words in item]
        indegree = []
        for i in indegree1:
            value = list(i)
            value[1] = value[1] + 1
            indegree.append(tuple(value))

        eigen = [item for item in eigen_score if words in item]
        closness = [item for item in closeness_score if words in item]
        list_of_tuples = list(indegree + eigen + closness)
        dict_of_scores = {}
        for a, b in list_of_tuples:
            dict_of_scores.setdefault(a, []).append(b)
        for key, value in dict_of_scores.items():
            dict_of_scores[key] = sum(value)
        score_list.append(dict_of_scores)
    dict_of_scores = {k: v for element in score_list for k, v in element.items()}
    sorted_score = sorted(dict_of_scores.items(), key=lambda kv: kv[1], reverse=True)
    final_rank=[]
    from dbpedia_graph_extraction import read_frequencyfile
    f=read_frequencyfile()
    for concepts in sorted_score:
        temp=list(concepts)
        for tup in f:
            if concepts[0]==tup[0]:
                temp[0]=concepts[0]
                temp[1]=(concepts[1]*tup[1])/100
                final_rank.append(tuple(temp))
