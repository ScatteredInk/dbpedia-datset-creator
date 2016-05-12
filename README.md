# DBPedia-WikiMedia Dataset Creator

A set of scripts for:

- Finding media files associated with DBPedia resources using a SPARQL endpoint
- Querying the WikiMedia API to discover metadata and URL information associated with media files
- Downloading media files and logging bad URLs and failed downloads
- Cleaning and converting media files into a specified form

# Installation and requirements

Python 2

In a virtual environment:

```
pip install -r requirements.txt
```

Or, create a new Anaconda environment called `dbpedia2` with:

```
conda env create -f environment.yml
```

To use the MediaWiki API, set the environment variables MEDIA_WIKI_USER_AGENT, MEDIA_WIKI_PASS, MEDIA_WIKI_APP_NAME according to the [Anaconda documentation](http://conda.pydata.org/docs/using/envs.html#saved-environment-variables) or during virtualenv activation. 

- MEDIA_WIKI_USER and MEDIA_WIKI_PASS are the username and password for your Wikimedia account
- MEDIA_WIKI_USER_AGENT is the [User-Agent](https://meta.wikimedia.org/wiki/User-Agent_policy) string of the form:

```
User-Agent: MyDatasetCreator/1.0 (http://example.com/MyDatasetCreator/; MyDatasetCreator@example.com) BasedOnDBPedia-WikiMediaDatasetCreator/0.1
``` 

# Use

**Current funcionality**: hard-coded to query for **Person** resource in DBPedia ontology with **signature** property.

## Queries

To execute query on DBPedia SPARQL endpoint:

```
python signature_query.py
```

This script saves the result of the query in a UTF-8 encoded CSV, 'signatures.csv', with the format:

| Resource | Property |
|---|---|
| Value | Value | 

## WikiMedia API query and media download

To query WikiMedia API:

```
python download_signatures.py
```

Fetches the urls associated with image URIs read in from 'signatures.csv'. If any url is None, the Person and Signature URIs are saved in 'bad_urls.csv'. Good urls are processed with the requests library and binary files downloaded to the images subdirectory. Any failures are logged and saved to 'bad_downloads.csv'.  






