
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import sys, random

class Custom404Task( BaseTask ):

	def getName( self ): return 'custom404'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):
			
		beauty.find( id = 'custom404' ).string.replace_with( data['custom404'] )

	def start( self, domain ):

		content = self.getDefaultData()
		actions = []
		
		try:
			missingPage = '/egosize/notfound/page/404/%d.html' % random.randint( 0, 100 )
			url = 'http://' + domain + missingPage
			result = urlfetch.fetch( url, deadline = 4 )
			if result.status_code == 200:
				content[ self.getName() ] = 'Your not found page has an error response code (200).' 
				actions.append({ 'status': 'bad', 'description': 'Configure your Web server to server not found pages with the right HTTP response code (404)' })
			elif result.status_code == 404:
				content[ self.getName() ] = 'Your page not found (404) is working, hooray!'
				actions.append({ 'status': 'good' })
		except:
			logging.warning( sys.exc_info()[1] )

		self.sendAndSaveReport( domain, content, actions )

