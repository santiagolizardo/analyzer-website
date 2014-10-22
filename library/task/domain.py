
import logging

import pygeoip

from library.task.base import BaseTask
from library.services.robowhois import RoboWhois

from datetime import timedelta, datetime
import calendar

import urllib
import urllib2

def make_api_call( name, params ):
	try:
		url = 'http://api.egosize.com/%s.php?%s' % ( name, urllib.urlencode( params ) )
		return urllib2.urlopen( url ).read()
	except Exception, ex:
		logging.error( ex )
		return None

class DomainAnalyzerTask( BaseTask ):

	def getName( self ):
		return 'domain'

	def updateView( self, beauty, data ):
		beauty.find( id = 'domainOwner' ).replace_with( str( data['owner'] ) )
		beauty.find( id = 'domainRegistrationDate' ).replace_with( str( data['regDate'] ) )
		beauty.find( id = 'domainExpirationDate' ).replace_with( str( data['expDate'] ) )
		if 'serverIp' in data:
			beauty.find( id = 'serverIp' ).string.replace_with( data['serverIp'] )

	def start( self, baseUrl ):
		self.fix_sys_path()

		rw = RoboWhois()
		rwdata = rw.whois( baseUrl )

		content = None

		if rwdata is not None:
			content = {}
			try:
				content['owner'] = rwdata['contacts'][0]['name']
			except:
				logging.warning( '%s has no registrant contacts' % baseUrl )
			try:
				content['nameservers'] = rwdata['nameservers']
			except Exception, ex:
				logging.warning( ex )
			regDate = datetime.strptime( rwdata['date_created'], '%Y-%m-%d %H:%M:%S' )
			expDate = datetime.strptime( rwdata['date_expires'], '%Y-%m-%d %H:%M:%S' )
			content['regDate'] = calendar.timegm( regDate.timetuple() )
			content['expDate'] = calendar.timegm( expDate.timetuple() )

		try:
			serverIp = make_api_call( 'ip', { 'domain': baseUrl } )
			if serverIp is not None:
				gi = pygeoip.GeoIP( 'GeoIP.dat' )
				countryCode = gi.country_code_by_addr( serverIp ).lower()
				try:
					countryName = gi.country_name_by_name( serverIp )
				except:
					countryName = 'N/A'
				serverIp = '%(serverIp)s (<img src="/images/flags/%(countryCode)s.png" alt="%(countryName)s flag" /> %(countryName)s)' % { 'countryCode': countryCode, 'countryName': countryName, 'serverIp': serverIp }
				content['serverIp'] = serverIp
		except Exception, ex:
			logging.error( ex )

		self.sendAndSaveReport( baseUrl, content )

	def suggest_actions( self, actions, data2, domain ):
		if data2 is None:
			return

		data = self.format_data( data2 )
		todayDate = datetime.today()
		oneYear = timedelta( days = 365 )

		if data['regDate'] < ( todayDate - oneYear ):
			actions.append({ 'status': 'good' })
		else:
			actions.append({ 'status': 'regular', 'description': 'Your domain has been registered during the last year. The older the better. Wait some time to get a better positioning because of this' })
		if data['expDate'] > ( todayDate + oneYear ):
			actions.append({ 'status': 'good' })
		else:
			actions.append({ 'status': 'regular', 'description': 'Register your domain longer than a year to prove Google and others you are serious about your business.' })


	def generate_html_node( self, data2 ):
		content = {}
		if data2 is None:
			return None

		data = self.format_data( data2 )
		if data['regDate'] is not None:
			content['registrationDate'] = data['regDate'].strftime( '%Y-%m-%d' )

		if data['expDate'] is not None:
			content['expirationDate'] = data['expDate'].strftime( '%Y-%m-%d' )

		return content

	def format_data( self, data ):
		if data is None:
			return data
		import copy
		data2 = copy.copy( data )
		if 'regDate' in data and data['regDate'] is not None and type( data['regDate'] ) == int:
			data2['regDate'] = datetime.utcfromtimestamp( data['regDate'] ) 
		if 'expDate' in data and data['expDate'] is not None and type( data['expDate'] ) == int:
			data2['expDate'] = datetime.utcfromtimestamp( data['expDate'] ) 
		return data2

