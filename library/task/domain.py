
import sys, json, os

import pygeoip

from google.appengine.api import urlfetch

from library.task.base import BaseTask

from datetime import timedelta, datetime

from bs4 import BeautifulSoup, NavigableString

class DomainAnalyzerTask( BaseTask ):

	def getName( self ): return 'domain'

	def getDefaultData( self ):

		return {
			'owner': 'N/A',
			'registrationDate': 'N/A',
			'expirationDate': 'N/A',
			'serverIp': 'N/A',
		}

	def updateView( self, beauty, data ):

		beauty.find( id = 'domainOwner' ).replace_with( str( data['owner'] ) )
		beauty.find( id = 'domainRegistrationDate' ).replace_with( str( data['registrationDate'] ) )
		beauty.find( id = 'domainExpirationDate' ).replace_with( str( data['expirationDate'] ) )
		beauty.find( id = 'serverIp' ).string.replace_with( data['serverIp'] )

	def start( self, baseUrl ):

		fullUrl = 'http://' + baseUrl

		content = self.getDefaultData()
		actions = []

		apiUsername = 'devsantiago.lizardo'
		apiKey = '2dc9a-aceb3-a310e-e73b3-54f1d'

		url = 'http://freeapi.domaintools.com/v1/%s/?format=json&api_username=%s&api_key=%s' % ( baseUrl, apiUsername, apiKey )

		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 
		debugActive = False
		if debugActive:
			url = 'http://api.domaintools.com/v1/domaintools.com/whois/'

		result = urlfetch.fetch( url )
		if result.status_code == 200:
			todayDate = datetime.today()
			oneYear = timedelta( days = 365 )

			data = json.loads( result.content )
			content['owner'] = data['response']['registrant']['name']

			regDate = data['response']['registration']['created']
			content['registrationDate'] = regDate 
			regDate = datetime.strptime( regDate, '%Y-%m-%d' )
			if regDate < ( todayDate - oneYear ):
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'regular', 'description': 'Your domain has been registered during the last year. The older the better. Wait some time to get a better positioning because of this' })

			expDate = data['response']['registration']['expires']
			content['expirationDate'] = expDate 
			expDate = datetime.strptime( expDate, '%Y-%m-%d' )
			if expDate > ( todayDate + oneYear ):
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'regular', 'description': 'Register your domain longer than a year to prove Google and others you are serious about your business.' })

			serverIp = data['response']['server']['ip_address']

			gi = pygeoip.GeoIP( 'GeoIP.dat' )
			countryCode = gi.country_code_by_addr( serverIp ).lower()
			countryName = gi.country_name_by_name( serverIp )
			serverIp = '%(serverIp)s (<img src="/images/flags/%(countryCode)s.png" alt="%(countryName)s flag" /> %(countryName)s)' % { 'countryCode': countryCode, 'countryName': countryName, 'serverIp': serverIp }
			content['serverIp'] = serverIp

		self.sendAndSaveReport( baseUrl, content, actions )

