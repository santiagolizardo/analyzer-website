
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import random

class Custom404Task( BaseTask ):

	def getName( self ):
		return 'custom404'

	def updateView( self, beauty, data ):
		beauty.find( id = 'custom404' ).string.replace_with( self.generate_html_node( data ) )

	def start( self, domain ):
		custom404 = None

		try:
			missingPage = '/egosize/notfound/page/404/%d.html' % random.randint( 0, 100 )
			url = 'http://' + domain + missingPage
			result = urlfetch.fetch( url, deadline = 4 )
			custom404 = { 'status_code': result.status_code }
		except Exception, ex:
			logging.error( ex )
		
		self.sendAndSaveReport( domain, custom404 )

	def suggest_actions( self, actions, custom404, domain ):
		if custom404['status_code'] == 404:
			actions.append({ 'status': 'good' })
		else:
			actions.append({ 'status': 'bad', 'description': 'Configure your Web server to server not found pages with the right HTTP response code (404)' })

	def generate_html_node( self, custom404 ):
		if custom404['status_code'] == 404:
			return 'The web server has sent a not found page correctly.'
		
		return  'The web server has sent a not found page with the wrong status code: ' + str( custom404['status_code'] )

