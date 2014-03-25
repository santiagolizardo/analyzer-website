
import sys, json, os, logging

import socket
import pygeoip

from google.appengine.api import urlfetch

from library.task.base import BaseTask
from library.services.robowhois import RoboWhois

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

		owner = 'N/A'
		if self.is_dev_env:
			owner = 'Test Owner'
			regDate = expDate = datetime.now()
		else:
			rw = RoboWhois()
			rwdata = rw.whois( baseUrl )

			if rwdata is not None:
				try:
					owner = rwdata['registrant_contacts'][0]['name']
				except:
					logging.warning( '%s has no registrant contacts' % baseUrl )
					owner = 'N/A'
				regDate = datetime.strptime( rwdata['created_on'][0:18], '%Y-%m-%dT%H:%M:%S' )
				expDate = datetime.strptime( rwdata['expires_on'][0:18], '%Y-%m-%dT%H:%M:%S' )

		todayDate = datetime.today()
		oneYear = timedelta( days = 365 )

		content['owner'] = owner 

		content['registrationDate'] = regDate.strftime( '%Y-%m-%d' )
		if regDate < ( todayDate - oneYear ):
			actions.append({ 'status': 'good' })
		else:
			actions.append({ 'status': 'regular', 'description': 'Your domain has been registered during the last year. The older the better. Wait some time to get a better positioning because of this' })

		content['expirationDate'] = expDate.strftime( '%Y-%m-%d' )
		if expDate > ( todayDate + oneYear ):
			actions.append({ 'status': 'good' })
		else:
			actions.append({ 'status': 'regular', 'description': 'Register your domain longer than a year to prove Google and others you are serious about your business.' })

		try:
			serverIp = socket.gethostbyname( baseUrl )
			gi = pygeoip.GeoIP( 'GeoIP.dat' )
			countryCode = gi.country_code_by_addr( serverIp ).lower()
			countryName = gi.country_name_by_name( serverIp )
			serverIp = '%(serverIp)s (<img src="/images/flags/%(countryCode)s.png" alt="%(countryName)s flag" /> %(countryName)s)' % { 'countryCode': countryCode, 'countryName': countryName, 'serverIp': serverIp }
			content['serverIp'] = serverIp
		except:
			logging.error( sys.exc_info()[0] ) 

		self.sendAndSaveReport( baseUrl, content, actions )

