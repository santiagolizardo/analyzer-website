
import sys, json, logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class W3cValidatorTask( BaseTask ):

	def getName( self ):
		return 'w3cValidation'

	def updateView( self, beauty, data ):
		beauty.find( id = 'w3cValidity' ).string.replace_with( self.generate_html_node( data ) )

	def start( self, url ):
		data = None
		fullUrl = 'http://' + url
		
		try:
			ws_url = 'http://validator.w3.org/check?uri=%s&charset=%%28detect+automatically%%29&doctype=Inline&group=1&output=json' % fullUrl
			result = urlfetch.fetch( ws_url, deadline = 10 )
			if result.status_code == 200:
				data = json.loads( result.content )
		except:
			logging.warning( sys.exc_info()[1] )
				
		self.sendAndSaveReport( url, data )

	def suggest_actions( self, actions, data, domain ):
	        if not data:
	                logging.warning('data is None')
	                return
		if len( data['messages'] ) == 0:
			actions.append({ 'status': 'good' })
		else:
			counting = { 'info': 0, 'error': 0, 'warning': 0 }
			for message in data['messages']:
				counting[ message['type'] ] += 1
			del counting['info']

			actions.append({ 'status': 'regular', 'description': 'Clean your HTML and fix the errors and warnings detected by the W3C validator' })

	def generate_html_node( self, data ):
		if not data or len( data['messages'] ) == 0:
			return 'No errors detected. Great!'
		else:
			counting = { 'info': 0, 'error': 0, 'warning': 0 }
			for message in data['messages']:
				counting[ message['type'] ] += 1
			del counting['info']

			return  'Your HTML has %d error(s) and %d warning(s).' % tuple( counting.itervalues() )

