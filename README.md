# DBPedia Public Acces Catalogue

## Required packages

In order to run the code, following packages are required: 

* sys
* json
* lxml.etree
* urllib.parse
* urllib.error
* urllib.request

## Buidling the Catalogue

This code builds a public access catalogue for the Great Books, based on information provided by the DBPedia lookup API. The DBPedia API response is XML. By building an intermediary dictionary and filtering on the ontology URL ("http://dbpedia.org/ontology/Book"), the code selects every book title that matches the user's query. After extracting all book titles from the intermediary dictionary, the user has to select the title they would like to get more information on. After selecting their title of choice, the resource URL is transformed to its JSON URL. The JSON file is parsed and iterated over to extract all the available metadata we are interested in.

The metadata that will be extracted is the following:
* Title book
* Author
* About the author
* Abstract
* Original language
* Country
* Number of pages
* publisher
* Year of publication

If any of this information is absent in the database, the code will return "Information absent in data".


```python

```
