
from library.controller.page import PageController

class IndexController( PageController ):

	def get( self ):
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )

		values = {
			'name': 'Santiago',
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
		}
		html = self.renderTemplate( 'index.html', values )
		self.writeResponse( html )
	
