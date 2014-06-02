
import os

import config

from library.controller.basic import BasicController

class PageController( BasicController ):

	styleSheets = None 
	javaScripts = None

	def __init__( self, req, resp ):
		super( PageController, self ).__init__( req, resp )
		
		self.styleSheets = []
		self.javaScripts = []
		self.pageMetas = []

		self.is_dev_env = config.debug_active 
		if self.is_dev_env:
			self.addJavaScript( '/scripts/jquery.min.js' )
			self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
			self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		else:
			self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
			self.addJavaScript( '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js' )
			self.addStyleSheet( '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css' )

		self.addStyleSheet( '/styles/allmedia.css' )

	def addJavaScript( self, javaScript ):
		self.javaScripts.append( javaScript )

	def addStyleSheet( self, styleSheet ):
		self.styleSheets.append( styleSheet )

class StandardPageController( PageController ):

	def renderTemplate( self, name, values = {} ):

		defaultValues = {
			'appDomain': config.current_instance['url'],
			'pageTitle': 'Egosize reviews any site and returns insights and improvements',
			'pageDescription': 'Free tool to generate reports out of websites with SEO and SEM metrics and get improvement ideas. Meant to marketers and developers.',
			'pageMetas': self.pageMetas,
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
		}
		defaultValues.update( values )
		
		return super( StandardPageController, self ).renderTemplate( name, defaultValues )

