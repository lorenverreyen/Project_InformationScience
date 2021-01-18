#!/usr/bin/env python
# coding: utf-8

# In[8]:


#Packages to install
import json
import urllib.parse
import urllib.request
import urllib.error
import lxml.etree


# In[9]:


CODES = {}
CODES[401] = "Authentication credentials were missing or authentication failed."
CODES[404] = "The requested entity was not found."
CODES[429] = "The request could be served because the application has reached its usage limit."
CODES[500] = "Internal Server Error. Something has gone wrong, which we will correct."


# In[10]:


from ISC_Project_Functions import getAPIprefix


# In[11]:


from ISC_Project_Functions import query_DBpedia1


# In[12]:


from ISC_Project_Functions import parser4


# In[13]:


from ISC_Project_Functions import titleselector


# In[14]:


from ISC_Project_Functions import API_to_JSON


# In[15]:


from ISC_Project_Functions import jsonsearcher


# In[ ]:


if __name__ == "__main__":
    search = " "
    while not search == "q":
        search = input("What are we looking for? (or q: to quit): ")
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
           


# In[ ]:


#18/01

