from SPARQLWrapper import SPARQLWrapper, N3, JSON
import networkx as nx
import matplotlib.pyplot as plt

def disambiuaty_check(st):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category:>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT  ?dlinks ?label  
        WHERE 
            {   

                 { 
                 :""" + st[1:-1] + """ dbo:wikiPageDisambiguates ?dlinks .
                 ?dlinks rdfs:label ?label .
                 FILTER ( lang(?label) = "en" )
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
    inner_dict2=[]
    for x in range(len(inner_dict)):
        temp=inner_dict[x]
        inner_dict2.append(temp['dlinks']['value'])
    if (result['results']['bindings'] != []):
        return inner_dict2


def disambiguity_check_forlink(link):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category:>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT  ?dlinks   

        WHERE 
              
                 { 
                    ?dlinks  dbo:wikiPageRedirects* <"""+link+""">  .     
                }
                limit 1
                 
                  
                  
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
        inner_dict2.append(temp['dlinks']['value'])
    if (result['results']['bindings'] != []):

        return True


def disambiuaty_pageRedirect(r):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?rlinks ?label

        WHERE 
        {
            {   
                    :""" + r[1:-1] + """ dbo:wikiPageRedirects* ?rlinks .
                        ?rlinks rdfs:label ?label .
                        FILTER ( lang(?label) = "en" )
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
        link = inner_dict2['rlinks']['value']
        return link

def rdftype_check(link):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category:>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT  ?label

        WHERE 
            {   

                 { 
                 <"""+link+""">  rdfs:label ?label ;
                                 rdf:type dbo:Company.

                    FILTER ( lang(?label) = "en" )

                  }
                  
                UNION
                {
                 <"""+link+""">  rdfs:label ?label ;
                                 rdf:type dbo:Organisation.

                    FILTER ( lang(?label) = "en" )
                
                }
                UNION
                {
                 <"""+link+""">  rdfs:label ?label ;
                                 rdf:type dbo:Film.

                    FILTER ( lang(?label) = "en" )
                
                }
                UNION
                {
                 <"""+link+""">  rdfs:label ?label ;
                                 rdf:type dbo:Person.

                    FILTER ( lang(?label) = "en" )
                
                }
                UNION
                {
                 <"""+link+""">  rdfs:label ?label ;
                                 rdf:type dbo:Work.

                    FILTER ( lang(?label) = "en" )
                
                }
                UNION
                {
                 <"""+link+""">  rdfs:label ?label ;
                                 rdf:type dbo:Activity.

                    FILTER ( lang(?label) = "en" )
                
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
        type = inner_dict2['label']['value']

        return type

def pageredirect_links2(r):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>

    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?s ?label

        WHERE 
            {
                {
                :""" + r[1:-1] + """ dbo:wikiPageRedirects ?s .
                ?s rdfs:label ?label .
                FILTER ( lang(?label) = "en" ) 
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
        link = inner_dict2['s']['value']
        label= inner_dict2['label']['value']

        return link, label
    else:
        return None
