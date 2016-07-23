
import json, logging, sys

from library.task.base import BaseTask

from google.appengine.api import urlfetch

from bs4 import BeautifulSoup, NavigableString

class SearchTask( BaseTask ):

	def getName( self ):
		return 'indexedPages'

	def updateView( self, beauty, indexed_pages ):
	    if indexed_pages:
		beauty.find( id = 'indexedPages' ).string.replace_with( self.generate_html_node( indexed_pages ) )

	def start( self, domain ):
		indexed_pages = None
		try:
			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:%s&filter=0' % domain
			result = urlfetch.fetch( url, deadline = 5 )
			if result.status_code == 200:
				data = json.loads( result.content )
				indexed_pages = int( data['responseData']['cursor']['estimatedResultCount'] )
		except Exception, ex:
			logging.error( ex )
				
		self.sendAndSaveReport( domain, indexed_pages )

	def suggest_actions( self, actions, indexed_pages, domain ):
		if indexed_pages < 500:
			actions.append({ 'status': 'bad', 'description': 'Your site has few pages indexed. Add more unique content progressively.' })
		elif indexed_pages < 2500:
			actions.append({ 'status': 'regular', 'description': 'The number of indexed pages is fine, but you could have lot more and attract additional visitors.' })
		else:
			actions.append({ 'status': 'good' })

	def generate_html_node( self, indexed_pages ):
	        if indexed_pages is None:
	            logging.warning('indexed_pages is None')
	            return None

		return '%d indexed pages' % indexed_pages

