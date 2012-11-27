
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
			'pageTitle': 'Analyze your domain for free. Check social, SEO and technical metrics to improve your business | DomainGrasp',
			'pageDescription': 'Check in less than a minute how your site is performing in terms of social and seo aspects. A free alternative to Woorank',
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
		}
		defaultValues.update( values )
		
		return super( StandardPageController, self ).renderTemplate( name, defaultValues )
