# coding=utf-8

import webapp2
import os, logging

from mako.lookup import TemplateLookup
from mako import exceptions

from library.utilities import uriFor

import gettext
import config, local_config

class BasicController( webapp2.RequestHandler ):

        def __init__(self, req, res):
            self.initialize(req, res)

            self.current_instance = None
	    current_domain = os.environ['SERVER_NAME']
	    for instance in local_config.instances:
	        if instance['domain'] in current_domain:
	            self.current_instance = instance
	            break

	def renderTemplate( self, name, values = {} ):
		gettext_instance = gettext.translation( 'messages', 'locales', [ self.current_instance['language'] ] )
		values['_'] = gettext_instance.ugettext 

		values['instances'] = [ instance for instance in config.instances if instance['gaTrackingId'] is not None ]
		values['current_instance'] = self.current_instance

		values['uriFor'] = uriFor
		
		templateDirs = [ os.path.abspath( 'templates' ) ]
		templateFinder = TemplateLookup( directories = templateDirs, input_encoding = 'utf-8', output_encoding = 'utf-8', encoding_errors = 'ignore', disable_unicode = False )
		templ = templateFinder.get_template( name );

		try:
			htmlOutput = templ.render( **values )
		except:
			htmlOutput = exceptions.html_error_template().render()
			self.writeResponse( htmlOutput )

		return htmlOutput

	def writeResponse( self, body, contentType = 'text/html' ):
		self.response.headers['Content-Type'] = contentType
		self.response.write( body )

