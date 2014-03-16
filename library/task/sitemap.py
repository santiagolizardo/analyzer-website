
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import sys

class SitemapXmlCheckerTask( BaseTask ):

	def getName( self ): return 'sitemapXml'

	def getDefaultData( self ):
		
		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):

		beauty.find( id = 'sitemapXml' ).string.replace_with( data['sitemapXml'] )

	def start( self, baseUrl ):

		domain = 'http://' + baseUrl

		content = self.getDefaultData()
		actions = []

		try:
			url = domain + '/sitemap.xml'
			htmlLink = '<a href="%(url)s" class="external" rel="nofollow" target="_blank">%(url)s</a>' % { 'url': url }
			result = urlfetch.fetch( url, deadline = 4 )

			if result.status_code == 200:
				contentType = result.headers['Content-type']
				if 'text/xml' in contentType:
					content[ self.getName() ] = htmlLink 
					actions.append({ 'status': 'good' })
				else:
					content[ self.getName() ] = '%(htmlLink)s has been found but with a wrong content type (%(contentType)s)' % { 'htmlLink': htmlLink, 'contentType': contentType } 
					actions.append({ 'status': 'regular', 'description': 'Fix the content type for the %s URL' % url })
			elif result.status_code == 404:
				content[ self.getName() ] = 'Missing' 
				actions.append({ 'status': 'regular', 'description': 'The %s file is missing'  % htmlLink })
		except:
			logging.warning( sys.exc_info()[1] )

		self.sendAndSaveReport( baseUrl, content, actions )

