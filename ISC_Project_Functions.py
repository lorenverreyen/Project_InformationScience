#!/usr/bin/env python
# coding: utf-8

# In[21]:


#Packages to install
import json
import urllib.parse
import urllib.request
import urllib.error
import lxml.etree


# In[22]:


CODES = {}
CODES[401] = "Authentication credentials were missing or authentication failed."
CODES[404] = "The requested entity was not found."
CODES[429] = "The request could be served because the application has reached its usage limit."
CODES[500] = "Internal Server Error. Something has gone wrong, which we will correct."


# In[23]:


#Prefix of the DBPedia lookup API
def getAPIprefix() -> str:
    
    prefixes = ["https://lookup.dbpedia.org/api/search/PrefixSearch?QueryString=",
                "http://lookup.dbpedia.org/api/search/PrefixSearch?QueryString=",
                "https://lookup.dbpedia.org/api/prefix?query=",
                "http://lookup.dbpedia.org/api/prefix?query=",
                "http://akswnc7.informatik.uni-leipzig.de/lookup/api/search?query="]
    for prefix in prefixes:
        with urllib.request.urlopen(prefix + "Antwerp") as test:
            if test.status == 200:
                return prefix
    sys.exit("No functioning DBpedia lookup API found!")


# In[24]:


#Cleaning up the input string
def clean(string: str) -> str:
    string = str(string)
    string = string.strip()
    string = string.casefold()
    string = urllib.parse.quote(string)
    return string


# In[25]:


#Querying API and return the response (or errorcode)
def query_DBpedia1(prefix, search: str) -> bytes: 
    search = clean(search)
    url = prefix + search
    try:
        with urllib.request.urlopen(url) as query:
            return query.read()
    except urllib.error.HTTPError as HTTPerr:
        exit(CODES.get(HTTPerr.code))
    except urllib.error.URLError as URLerr:
        exit(URLerr)


# In[26]:


# Transforming the API to a jupyter dictionary to be able to iterate over it.

def parser4(search_response: bytes) -> dict:
    root = lxml.etree.fromstring(search_response) 

    index=0
    diction={}

# Iterating over the dictionary, looking for all the titles that match a book, marked by "http://dbpedia.org/ontology/Book"
    for result in root.iter("Result"):
        for field in result.iter("URI"):
                
            if field.text ==  "http://dbpedia.org/ontology/Book":
                #print(result.tag)
                #print(result.text)
                
                for URI in result[1].iter("URI"):
                    #print(URI.text)
                    index+=1
                    diction[index]=URI.text
            
    return diction


# In[27]:


# Returning the possible book titles to the user, they select one title to continue with.
# By placing the code in a while-loop, the code will only continue if the user gives a valid input. 

def titleselector(possiblefields):
    
    while True: 
        print(possiblefields)
        userselection = input("With which URI would you like to continue? Press the matching key. ")
        
        for key, value in possiblefields.items():
            if str(key) == userselection:
       
                linkto=value
                return linkto
            
        else:
            print("This key is invalid, please try again.")
            continue
                


# In[28]:


# Transforming the resource URL to JSON URL.

def API_to_JSON(link):
    
    x = link.replace("resource", "data")
    json_uri = x + ".json"

    return json_uri


# In[29]:


# jsonsearcher iterates over the JSON file, looking for metadata we want to extract.

# The metadata we are looking for:
# the title, the author, short introdcution of the author, abstract of the book, original language, 
# country, number of pages, publisher and year of publication

# By placing every for loop that looks for a different piece of information inside a try/except block,
# the inforamtion will be marked as absent if said information is missing in the JSON file


import json
import urllib.parse
import urllib.request
import urllib.error

def jsonsearcher(API_link, JSON_link):
    
    try:
        with urllib.request.urlopen(JSON_link) as page:
          
            json_string = page.read()
            test = json.loads(json_string)
            resultdata=""
       
    
            ## TITLE ##
            try:
                for title in test[API_link]["http://www.w3.org/2000/01/rdf-schema#label"]:
                    for key, value in title.items():
                        #If an information item is given in different languages, the English information is sselected by filtering on "lang": "en"
                        if value =="en":
                            for key, value in title.items():
                                if key =="value":
                                    print("\n")
                                    print("Title: " + value)
            
            except KeyError:
                print("\n")
                print("Title: Information absent in data")
                
            ##AUTHOR##
            
            
            try:
                
                # The JSON data contains linked information to the author of the book, rather than the information about the author itself.
                # The URL that matches the author is transformed to its JSON url to be able to extract the information about the author.
                
                for author in test[API_link]["http://dbpedia.org/property/author"]:
                    
                    for key, value in author.items():
                        if key == "value":
                            authorlink = value
                            authorlink1 =  authorlink.replace("resource", "data")
                            authorlink2 = authorlink1 + ".json"
                            
                            
                            with urllib.request.urlopen(authorlink2) as page:
                                json_string = page.read()
                                test2 = json.loads(json_string)
                                
                                
                                for authordata in test2[authorlink]["http://www.w3.org/2000/01/rdf-schema#label"]:
                                    for key, value in authordata.items():
                                        if value == "en":
                                            for key, value in authordata.items():
                                                if key == "value":
                                                    print("\n")
                                                    print("Author: " + value)
                                    
                                for authordata2 in test2[authorlink]["http://dbpedia.org/ontology/abstract"]:
                                    for key, value in authordata2.items():
                                        if value == "en":
                                            for key, value in authordata2.items():
                                                if key == "value":
                                                    print("\n")
                                                    print("About the author: " + value)
            except ValueError:
                print("\n")
                print("About the author: Information absent in data")
            
            ## ABSTRACT ##
            try:
                for abstract in test[API_link]["http://dbpedia.org/ontology/abstract"]:
                    for key, value in abstract.items():
                        if value == "en":
                            for key, value in abstract.items():
                                if key=="value":
                                    print("\n")
                                    print("Abstract: " + str(value))
                                    
            except KeyError:
                print("\n")
                print("Abstract: Information absent in data")
            
            
            ## ORIGINAL LANGUAGE##
            try:
                for language in test[API_link]["http://dbpedia.org/property/language"]:
                    for key, value in language.items():
                        if value == "en":
                            for key, value in language.items():
                                if key == "value":
                                    print("\n")
                                    print("Original Language: " + str(value))
            except KeyError:
                print("\n")
                print("Original Langauge: Information absent in data")
            
            ## COUNTRY ##
            try: 
                for country in test[API_link]["http://dbpedia.org/property/country"]:
                    for key, value in country.items():
                        if key == "value":
                            print("\n")
                            print("Country: " + str(value))
                            
            except KeyError:
                print("\n")
                print("Country: Information absent in data")
                    
            
            ## NUMBER OF PAGES ##
            try:
                for pages in test[API_link]["http://dbpedia.org/property/pages"]:
                    for key, value in pages.items():
                        if key =="value":
                            print("\n")
                            print("Number of pages: " + str(value))
            except KeyError:
                print("\n")
                print("Number of pages: Information absent in data")
                    
            
            ## PUBLISHER ##
            try:
                for publisher in test[API_link]["http://purl.org/dc/elements/1.1/publisher"]:
                    for key, value in publisher.items():
                        if key == "value":
                            print("\n")
                            print("Publisher: " + value)
            except KeyError:
                print("\n")
                print("Publisher: Information absent in data")
                
            
            ## YEAR OF PUBLICATION ##
            try:
                for publication in test[API_link]["http://dbpedia.org/property/published"]:
                    for key, value in publication.items():
                        if key =="value":
                            print("\n")
                            print("Date of publication: " + str(value))
                                                           
            except KeyError:
                print("\n")
                print("Date of publication: Information absent in data")
        
            
            
                                    
        
    except urllib.error.HTTPError as HTTPerr:
        print("No data available, please try another title.")
    except urllib.error.URLError as URLerr:
        print("No data available, please try another title.")
    


# In[ ]:


#18/01

