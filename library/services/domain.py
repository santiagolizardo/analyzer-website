
from google.appengine.api import urlfetch
import json, logging

def tokenize_url( url ):
	"""
	Returns a dictionary with the keys: domain, subdomain, suffix, tld
	"""
	webservice_url = 'http://tldextract.appspot.com/api/extract?url=' + url
	result = urlfetch.fetch( webservice_url, deadline = 3 )
	return json.loads( result.content )

if __name__ == '__main__':
	print tokenize_url( 'www.bbc.co.uk' )

