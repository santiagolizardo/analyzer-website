
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from google.appengine.ext import db
from library.utilities import uriFor

class IndexController( StandardPageController ):

	def get( self ):
		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )		
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		self.addStyleSheet( '/styles/allmedia.css' )

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
		html = self.renderTemplate( 'index.html', values )
		self.writeResponse( html )
	
