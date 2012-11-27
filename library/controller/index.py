
from library.controller.page import StandardPageController

from google.appengine.ext import db

class IndexController( StandardPageController ):

	def get( self ):
		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )		
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		self.addStyleSheet( '/styles/allmedia.css' )

		recentDomains = db.GqlQuery( 'SELECT * FROM SiteReport ORDER BY creationDate DESC' ).fetch( 50 )

		values = {
			'recentDomains': recentDomains,
		}
		html = self.renderTemplate( 'index.html', values )
		self.writeResponse( html )
	
