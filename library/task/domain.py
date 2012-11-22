
import sys, json, logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class DomainAnalyzerTask( BaseTask ):

	def getName( self ): return 'domain'

	def start( self, fullUrl ):

		content = {
			'owner': 'N/A',
			'registrationDate': 'N/A',
			'expirationDate': 'N/A',
		}

		baseUrl = fullUrl.replace( 'http://', '' ).replace( '/', '' )
		apiUsername = 'devsantiago.lizardo'
		apiKey = '2dc9a-aceb3-a310e-e73b3-54f1d'

		url = 'http://api.domaintools.com/v1/%s/?format=json&api_username=%s&api_key=%s' % ( baseUrl, apiUsername, apiKey )
		url = 'http://api.domaintools.com/v1/domaintools.com/whois/'
		result = urlfetch.fetch( url )
		if result.status_code == 200:
			data = json.loads( result.content )
			logging.info(data)
			content['owner'] = data['response']['registrant']
			content['registrationDate'] = data['response']['registration']['created']
			content['expirationDate'] = data['response']['registration']['expires']

		self.saveReport( fullUrl, content )
		self.sendMessage( content )

