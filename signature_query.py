import os
import rdflib
import json
import csv, codecs, cStringIO
from collections import OrderedDict

from rdflib import URIRef, Graph
from SPARQLWrapper import SPARQLWrapper, JSON

from utf8_csv import UnicodeWriter


def main():

	sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
	sparql.setQuery("""

	SELECT DISTINCT ?scientist ?signature
	WHERE
	{
	  ?scientist rdf:type dbo:Person .
	  ?scientist dbp:signature ?signature
	  FILTER(lang(?signature) = "en")
	}
	LIMIT 100
	""")

	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	with open('signatures.csv', 'wb') as csvfile:
		csv_headers = OrderedDict([('Person_URI',None),('Signature',None)])
		dw = csv.DictWriter(csvfile, delimiter=',', fieldnames=csv_headers)
		dw.writeheader()

		for result in results["results"]["bindings"]:
			person = result["scientist"]["value"]
			signature = result["signature"]["value"]
			writer = UnicodeWriter(csvfile)
			writer.writerow([person, signature])




if __name__ == '__main__':
	main()