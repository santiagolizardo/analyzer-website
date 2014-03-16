
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import sys

class HumansTxtCheckerTask( BaseTask ):

	def getName( self ): return 'humansTxt'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):
			
		beauty.find( id = 'humansTxt' ).string.replace_with( data['humansTxt'] )

	def start( self, domain ):

		content = self.getDefaultData()
		actions = []
		
		try:
			url = 'http://' + domain + '/humans.txt'
			htmlLink = '<a href="%(humansUrl)s" class="external" rel="nofollow" target="_blank">%(humansUrl)s</a>' % { 'humansUrl': url }
			result = urlfetch.fetch( url, deadline = 4 )

			if result.status_code == 200:
				contentType = result.headers['Content-type']
				if 'text/plain' in contentType:
					content[ self.getName() ] = htmlLink 
					actions.append({ 'status': 'good' })
				else:
					content[ self.getName() ] = '%(htmlLink)s has been found but with a wrong content type (%(contentType)s)' % { 'htmlLink': htmlLink, 'contentType': contentType } 
					actions.append({ 'status': 'regular', 'description': 'Fix the content type for the %s URL' % url })
			elif result.status_code == 404:
				content[ self.getName() ] = 'Missing'
				actions.append({ 'status': 'regular', 'description': 'The %s file is missing' % htmlLink })
		except:
			logging.warning( sys.exc_info()[1] )

		self.sendAndSaveReport( domain, content, actions )

