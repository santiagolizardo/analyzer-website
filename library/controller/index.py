
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from google.appengine.ext import db
from library.utilities import uriFor

from google.appengine.api import memcache

class IndexController( StandardPageController ):

	def get( self ):

		html = memcache.get( 'page-index' )
		if html is None or self.is_dev_env:
			html = self.generate_html()
			memcache.set( 'page-index', html, time = 3600 )

		self.writeResponse( html )

	def generate_html( self ):

		recentDomains = db.GqlQuery( 'SELECT * FROM SiteReport ORDER BY creationDate DESC' ).fetch( 10 )

		sitesQuery = SiteReport.all()
		sitesQuery.order( '-score' )
		
		sites = []
		i = 0
		for entity in sitesQuery.run( limit = 10 ):
		    i += 1
		    site = db.to_dict( entity, { 'position': i, 'lastReportUrl': uriFor( 'staticReport', domainUrl = entity.url ) } ) 
		    sites.append( site )

		values = {
			'recentDomains': recentDomains,
			'sitesRanking': sites,
		}

		return self.renderTemplate( 'index.html', values )

	
