
import os

import config
from config import current_instance as site

from library.controller.basic import BasicController

class PageController( BasicController ):

	styleSheets = None 
	javaScripts = None

	def __init__( self, req, resp ):
		super( PageController, self ).__init__( req, resp )
		
		self.styleSheets = []
		self.javaScripts = []
		self.pageMetas = []

		if config.debug_active:
			self.addJavaScript( '/scripts/jquery.min.js' )
			self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
			self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		else:
			self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
			self.addJavaScript( '//netdna.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js' )
			self.addStyleSheet( '//netdna.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css' )

		self.addStyleSheet( '/styles/allmedia.css' )

	def addJavaScript( self, javaScript ):
		self.javaScripts.append( javaScript )

	def addStyleSheet( self, styleSheet ):
		self.styleSheets.append( styleSheet )

class StandardPageController( PageController ):

	def renderTemplate( self, name, values = {} ):

		defaultValues = {
			'appDomain': site['url'],
			'domain': site['domain'],
			'siteName': site['name'],
			'pageTitle': '%s reviews any site and returns insights and improvements' % site['name'],
			'pageDescription': 'Free tool to generate reports out of websites with SEO and SEM metrics and get improvement ideas. Meant to marketers and developers.',
			'pageMetas': self.pageMetas,
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
		}
		defaultValues.update( values )
		
		return super( StandardPageController, self ).renderTemplate( name, defaultValues )

