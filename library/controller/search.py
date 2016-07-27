
from google.appengine.api import search

from library.controller.page import StandardPageController

from library.model.report import SiteReport, SiteRating

from library.utilities import uriFor
from google.appengine.ext import db

class SearchController(StandardPageController):

	def get( self, query = None ):

		query = query.replace( '-', ' ' )
		result_response = self.search( query )

		if result_response.number_found == 0:
			self.response.set_status( 404 )

		results = result_response.results
	
		values = {
			'pageTitle': '%s website metrics and reports - %s' % (query.capitalize(), self.current_instance['name']),
			'pageDescription': '%s related websites. Find useful information about %s pages and use it for your own websites.' % ( query.capitalize(), query ),
			'results': results,
			'query': query,
		}

		html = self.renderTemplate( 'search.html', values)

		self.writeResponse( html )

	def search( self, query ):
		index = search.Index( name = 'domains' )
		query_string = 'description: %(pattern)s OR title: %(pattern)s OR keywords: %(pattern)s' % { 'pattern': query } 
		try:
			results = index.search( query_string ) 
		except search.Error:
			logging.exception('Search failed')
		return results

