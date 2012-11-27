
import json

from library.task.base import BaseTask

from google.appengine.api import urlfetch

class SearchTask( BaseTask ):

	def getName( self ):

		return 'indexedPages'

	def getDefaultData( self ):

		return {
			'indexedPages': 0,
		}

	def start( self, domainUrl ):

		content = self.getDefaultData()
		actions = []

		url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:%s&filter=0' % domainUrl
		result = urlfetch.fetch( url )
		if result.status_code == 200:
			data = json.loads( result.content )
			indexedPages = int( data['responseData']['cursor']['estimatedResultCount'] )
			content['indexedPages'] = str( indexedPages )
			if indexedPages < 500:
				actions.append({ 'status': 'bad', 'description': 'Your site has few pages indexed. Add more unique content progressively.' })
			elif indexedPages < 2500:
				actions.append({ 'status': 'regular', 'description': 'The number of indexed pages is fine, but you could have lot more and attract additional visitors.' })
			else:
				actions.append({ 'status': 'good' })
	    
		self.sendAndSaveReport( domainUrl, content, actions )

