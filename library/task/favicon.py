
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import sys

class FaviconCheckerTask( BaseTask ):

	def getName( self ): return 'pageFavicon'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):
			
		beauty.find( id = 'pageFavicon' ).string.replace_with( data['pageFavicon'] )

	def start( self, domain ):

		content = self.getDefaultData()
		actions = []
		
		try:
			url = 'http://' + domain + '/favicon.ico'
			htmlLink = '<a href="%(faviconUrl)s" class="external" rel="nofollow" target="_blank"><img src="%(faviconUrl)s" alt="Favicon" /></a>' % { 'faviconUrl': url }
			result = urlfetch.fetch( url, deadline = 4 )

			if result.status_code == 200:
				content[ self.getName() ] = htmlLink 
				actions.append({ 'status': 'good' })
			elif result.status_code == 404:
				content[ self.getName() ] = 'Missing'
				actions.append({ 'status': 'bad', 'description': 'The %s file is missing' % htmlLink })
		except:
			logging.warning( sys.exc_info()[1] )

		self.sendAndSaveReport( domain, content, actions )

