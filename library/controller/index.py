
from library.controller.page import PageController
from library.model.domain import Domain

from google.appengine.ext import db

class IndexController( PageController ):

	def get( self ):
		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )		
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		self.addStyleSheet( '/styles/allmedia.css' )

		recentDomains = db.GqlQuery( 'SELECT * FROM Domain ORDER BY analysisDate DESC' ).fetch( 50 )

		values = {
			'appUrl': self.app.config.get( 'url' ),
			'pageTitle': 'Analyze your domain for free. Check social, SEO and technical metrics to improve your business | DomainGrasp',
			'pageDescription': 'A free alternative to Woorank',
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
			'recentDomains': recentDomains,
		}
		html = self.renderTemplate( 'index.html', values )
		self.writeResponse( html )
	
