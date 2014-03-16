
from library.controller.basic import BasicController
import statvfs

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

class StandardPageController( PageController ):
	
	def renderTemplate( self, name, values = {} ):

		defaultValues = {
			'appUrl': self.app.config.get( 'url' ),
			'appDomain': self.app.config.get( 'domain' ),
			'pageTitle': 'EGOsize reviews any site and returns insights and improvements',
			'pageDescription': 'Free tool to generate reports out of websites with SEO and SEM metrics and get improvement ideas. Meant to marketers and developers.',
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
		}
		defaultValues.update( values )
		
		return super( StandardPageController, self ).renderTemplate( name, defaultValues )
