
import logging

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

from library.task.base import BaseTask

import sys

class RobotsTxtCheckerTask( BaseTask ):

	def getName( self ): return 'robotsTxt'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def start( self, domain ):

		content = self.getDefaultData()
		actions = []
		
		try:
			url = domain + '/robots.txt'
			result = urlfetch.fetch( url, deadline = 4 )

			if result.status_code == 200:
				content[ self.getName() ] = url
				actions.append({ 'status': 'good' })
			elif result.status_code == 404:
				content[ self.getName() ] = 'Missing' 
				actions.append({ 'status': 'regular', 'description': 'Add a robots.txt file to your site' })
		except:
			logging.warning( sys.exc_info()[1] )

		self.sendAndSaveReport( domain, content, actions )

class SitemapXmlCheckerTask( BaseTask ):

	def getName( self ): return 'sitemapXml'

	def getDefaultData( self ):
		
		return { self.getName(): 'N/A' }

	def start( self, domain ):

		content = self.getDefaultData()
		actions = []

		try:
			url = domain + '/sitemap.xml'
			result = urlfetch.fetch( url, deadline = 4 )

			if result.status_code == 200:
				content[ self.getName() ] = url
				actions.append({ 'status': 'good' })
			elif result.status_code == 404:
				content[ self.getName() ] = 'Missing' 
				actions.append({ 'status': 'regular', 'description': 'Add a sitemap.xml to your site' })
		except:
			logging.warning( sys.exc_info()[1] )

		self.sendAndSaveReport( domain, content, actions )

