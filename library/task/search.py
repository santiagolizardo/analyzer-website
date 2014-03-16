
import json, logging, sys

from library.task.base import BaseTask

from google.appengine.api import urlfetch

from bs4 import BeautifulSoup, NavigableString

class SearchTask( BaseTask ):

	def getName( self ):

		return 'indexedPages'

	def getDefaultData( self ):

		return {
			'indexedPages': '0',
		}

	def updateView( self, beauty, data ):

		beauty.find( id = 'indexedPages' ).replace_with( NavigableString( data['indexedPages'] ) )

	def start( self, domainUrl ):

		content = self.getDefaultData()
		actions = []

		try:
			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:%s&filter=0' % domainUrl
			result = urlfetch.fetch( url, deadline = 5 )
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
		except:
			logging.warning( sys.exc_info()[1] )
	    
		self.sendAndSaveReport( domainUrl, content, actions )

