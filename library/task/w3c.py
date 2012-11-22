
import sys, json, logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class W3cValidatorTask( BaseTask ):

	def getName( self ): return 'w3cValidation'

	def start( self, fullUrl ):
		
		content = 'Unable to contact W3C servers',
	    
		url = 'http://validator.w3.org/check?uri=%s&charset=%%28detect+automatically%%29&doctype=Inline&group=1&output=json' % fullUrl
		result = urlfetch.fetch( url )
		if result.status_code == 200:
			try:
				data = json.loads( result.content )
				if len( data['messages'] ) == 0:
					content = 'No errors detected. Great!'
				else:
					counting = { 'info': 0, 'error': 0, 'warning': 0 }
					for message in data['messages']:
						counting[ message['type'] ] += 1
					del counting['info']

					content = 'Your HTML has %d error(s) and %d warning(s).' % tuple( counting.itervalues() )
			except:
				e = sys.exc_info()[0]
				logging.error( str( e ) )

		self.saveReport( fullUrl, content )
		self.sendMessage( content )

