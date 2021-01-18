#!/usr/bin/env python
# coding: utf-8

# In[67]:


#Packages to install
import sys
import json
import lxml.etree
import urllib.parse
import urllib.error
import urllib.request


# In[68]:


CODES = {}
CODES[401] = "Authentication credentials were missing or authentication failed."
CODES[404] = "The requested entity was not found."
CODES[429] = "The request could be served because the application has reached its usage limit."
CODES[500] = "Internal Server Error. Something has gone wrong, which we will correct."


# In[60]:


from ISC_Project_Functions import getAPIprefix


# In[61]:


from ISC_Project_Functions import query_DBpedia1


# In[62]:


from ISC_Project_Functions import parser4


# In[63]:


from ISC_Project_Functions import titleselector


# In[64]:


from ISC_Project_Functions import API_to_JSON


# In[65]:


from ISC_Project_Functions import jsonsearcher


# In[66]:


if __name__ == "__main__":
    search = " "
    while not search == "q":
        search = input("What are we looking for? (or 'q' to quit): ")
        if search == 'q':
            print("Querying DBPedia Ended")
            break
        else:
            # 1 Making sure the prefix we are using still works
            DBPEDIA_PREFIX = getAPIprefix()
            # 2 Harvesting XML
            SEARCH_RESPONSE = query_DBpedia1(DBPEDIA_PREFIX, search)
            # 3 Parsing XML to intermediary dictionary
            PARENTS = parser4(SEARCH_RESPONSE)
            # 4 Checking whether the database contains information about the book we are looking for.
            # If not, the user can ask for a new title.
            if PARENTS == {}:
                    print("The title does not appear in the database, please try another title.")
                    continue
            else: 
                POSSIBLE_URI = titleselector(PARENTS)
            # 5 Transforming resouce URL to JSON URL 
                JSON_URI = API_to_JSON(POSSIBLE_URI)
            # 6 Iterate over the JSON file and extract the wanted metadata
                FINAL_DATA = jsonsearcher(POSSIBLE_URI, JSON_URI)    
           

