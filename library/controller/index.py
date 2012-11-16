
from library.controller.page import PageController
from library.model.domain import Domain

from google.appengine.ext import db

class IndexController( PageController ):

	def get( self ):
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )

		recentDomains = db.GqlQuery( 'SELECT * FROM Domain ORDER BY analysisDate DESC' ).fetch( 20 )

		values = {
			'pageTitle': 'Analyze your domain free. Check social, SEO and technical factors to improve your business | DomainGrasp ',
			'pageDescription': 'A free alternative to Woorank',
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
			'recentDomains': recentDomains,
		}
		html = self.renderTemplate( 'index.html', values )
		self.writeResponse( html )
	
