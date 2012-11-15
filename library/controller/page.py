
from library.controller.basic import BasicController

class PageController( BasicController ):

	styleSheets = None 
	javaScripts = None

	def __init__( self, req, resp ):
		super( PageController, self ).__init__( req, resp )
		
		self.styleSheets = []
		self.javaScripts = []

	def addJavaScript( self, javaScript ):
		self.javaScripts.append( javaScript )

	def addStyleSheet( self, styleSheet ):
		self.styleSheets.append( styleSheet )


