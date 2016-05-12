import os
import mwclient
import logging
import requests
from csv import DictWriter

from utf8_csv import UnicodeReader, UnicodeWriter
from collections import OrderedDict

logging.basicConfig(filename='downloads.log',level=logging.DEBUG)


def main():

	#login using mwclient and env variables
	WIKI_MEDIA_SITE = 'commons.wikimedia.org'
	try:
		user = os.environ['MEDIA_WIKI_USER']
		password = os.environ['MEDIA_WIKI_PASS']
		user_agent = os.environ['MEDIA_WIKI_USER_AGENT']
	except KeyError, e:
		logging.debug('Credentials not found in environment')
		raise e
	site = mwclient.Site(WIKI_MEDIA_SITE, clients_useragent=user_agent)
	site.login(user, password)


	#no race conditions, just check if images dir exists
	if not os.path.exists('images'):
		os.makedirs('images')

	bad_urls = []
	bad_downloads = []

	#read in the mediawiki URIs from csv
	with open('signatures.csv', 'rb') as f:
		reader = UnicodeReader(f)
		headers = reader.next()
		for row in reader:
			image_name = row[1]
			image_obj = site.Images[image_name]
			url = image_obj.imageinfo.get('url')
			if url is None:
				bad_urls.append(row)
			else:
				try:
					r = requests.get(url)
					with open(os.path.join('images',image_name), 'wb') as f:
						for chunk in r.iter_content():
							f.write(chunk)
				except requests.exceptions.RequestException, e:
					print e
					logging.warning('Error downloading {0}, {1}'.format(
						url, e))
					bad_downloads.append(row)
				print "Downloaded {0}".format(url)

	with open('bad_urls.csv', 'wb') as csvfile:
		csv_headers = OrderedDict([('Person_URI',None),('Signature',None)])
		dw = DictWriter(csvfile, delimiter=',', fieldnames=csv_headers)
		dw.writeheader()

		for row in bad_urls:
			writer = UnicodeWriter(csvfile)
			writer.writerow(row)

	with open('bad_downloads.csv', 'wb') as csvfile:
		csv_headers = OrderedDict([('Person_URI',None),('Signature',None)])
		dw = DictWriter(csvfile, delimiter=',', fieldnames=csv_headers)
		dw.writeheader()

		for row in bad_downloads:
			writer = UnicodeWriter(csvfile)
			writer.writerow(row)




if __name__ == '__main__':
	main()