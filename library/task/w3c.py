
import sys, json, logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class W3cValidatorTask( BaseTask ):

	def getName( self ): return 'w3cValidation'

	def getDefaultData( self ):

		return { self.getName(): 'Unable to contact W3C servers' }

	def updateView( self, beauty, data ):

		beauty.find( id = 'w3cValidity' ).string.replace_with( data['w3cValidation'] )

	def start( self, baseUrl ):

		fullUrl = 'http://' + baseUrl
		
		content = self.getDefaultData()
		actions = []
	    
		try:
			url = 'http://validator.w3.org/check?uri=%s&charset=%%28detect+automatically%%29&doctype=Inline&group=1&output=json' % fullUrl
			result = urlfetch.fetch( url, deadline = 10 )
			if result.status_code == 200:
				data = json.loads( result.content )
				if len( data['messages'] ) == 0:
					content[ self.getName() ] = 'No errors detected. Great!'
					actions.append({ 'status': 'good' })
				else:
					counting = { 'info': 0, 'error': 0, 'warning': 0 }
					for message in data['messages']:
						counting[ message['type'] ] += 1
					del counting['info']

					content[ self.getName() ] = 'Your HTML has %d error(s) and %d warning(s).' % tuple( counting.itervalues() )
					actions.append({ 'status': 'regular', 'description': 'Clean your HTML and fix the erros and warnings detected by the W3C validator' })
		except:
			logging.warning( sys.exc_info()[1] )
		
		self.sendAndSaveReport( fullUrl, content, actions )

