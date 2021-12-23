from SPARQLWrapper import SPARQLWrapper, N3, JSON
global inner_dict2

def disambiguity_concept_abstract(link):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>

    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?label ?abstract ?rt

        WHERE 
            {
                {
                <"""+link+"""> rdfs:label ?label ;
                                rdf:type ?rt ;
                               dbo:abstract  ?abstract .
                            

                            FILTER ( lang(?abstract) = "en" )
                            FILTER ( lang(?label) = "en" )  
                            FILTER ( ?rt != dbo:Place )
                            FILTER ( ?rt != dbo:Company)
                            FILTER ( ?rt != dbo:Activity) 
                            FILTER ( ?rt != dbo:Person )
                            FILTER ( ?rt != dbo:Album )
                            FILTER ( ?rt != dbo:Artist )
                            FILTER ( ?rt != dbo:Band )
                            FILTER ( ?rt != dbo:MusicalWork )
                            FILTER ( ?rt != dbo:Work )
                            FILTER ( ?rt != dbo:FictionalCharacter )

                            



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
    if inner_dict==[]:
        return None
    global inner_dict2

    for x in inner_dict:
        inner_dict2 = inner_dict[0]
    label = inner_dict2['label']['value']
    abstract=inner_dict2['abstract']['value']
    if (label and abstract)!=None:
            return label, abstract
    else:
        return None



def disambiguity_concept_labstract(label):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX cat: <http://dbpedia.org/resource/Category/>
    PREFIX : <http://dbpedia.org/resource/>
        SELECT ?label ?abstract

        WHERE 
            {
                {
                :""" + label[1:-1] + """  rdfs:label ?label ;
                               dbo:abstract  ?abstract .
                            FILTER ( lang(?abstract) = "en" )
                            FILTER ( lang(?label) = "en" )                                         
            }
        }

   """)
    global new_dict1
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    new_dict_list = []
    for val in result.values():
        new_dict1 = dict(val)
        new_dict_list.append(val)
    global inner_dict1
    global inner_dict3
    inner_dict1 = new_dict1['bindings']
    if inner_dict1==[]:
        return None

    for x in inner_dict1:
        global inner_dict3
        inner_dict3 = inner_dict1[0]

    label = inner_dict3['label']['value']
    abstract=inner_dict3['abstract']['value']
    if label!=None and abstract!=None:

        return label, abstract

    else:
        return None

def disambiuaty_check_forlinks(link):
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
                 <"""+link+"""> dbo:wikiPageDisambiguates ?dlinks .
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
    inner_dict2 = []
    for x in range(len(inner_dict)):
        temp = inner_dict[x]
        inner_dict2.append(temp['dlinks']['value'])

    if (result['results']['bindings'] != []):
        return inner_dict2


def pageredirect_linkfind(l):

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
        SELECT ?rlinks ?label

        WHERE 
        {   
            {
            :"""+l[1:-1]+""" dbo:wikiPageRedirects ?rlinks  .
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
    # global inner_dict2
    inner_dict = new_dict['bindings']
    for x in inner_dict:
        inner_dict2 = inner_dict[0]

    if (result['results']['bindings'] != []):
        link = inner_dict2['rlinks']['value']
        label=inner_dict2['label']['value']

        return link, label