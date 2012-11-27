
import webapp2
import os, logging

from mako.lookup import TemplateLookup

from library.utilities import uriFor

class BasicController( webapp2.RequestHandler ):

	def renderTemplate( self, name, values = {} ):
		values['uriFor'] = uriFor
		
		templateDirs = [ os.path.abspath( 'templates' ) ]
		templateFinder = TemplateLookup( directories = templateDirs, input_encoding = 'utf-8', output_encoding = 'utf-8', encoding_errors = 'ignore', disable_unicode = False )
		templ = templateFinder.get_template( name );

		try:
			htmlOutput = templ.render( **values )
		except:
			from mako import exceptions
			htmlOutput = exceptions.html_error_template().render()

		return htmlOutput

	def writeResponse( self, body, contentType = 'text/html' ):
		self.response.headers['Content-Type'] = contentType
		self.response.write( body )

