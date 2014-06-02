
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from google.appengine.ext import db
from library.utilities import uriFor

from google.appengine.api import memcache

class ContactController( StandardPageController ):

	def get( self ):
		html = memcache.get( 'page-contact' )
		if html is None or self.is_dev_env:
			html = self.generate_html()
			memcache.set( 'page-contact', html, time = 3600 )

		self.writeResponse( html )

	def generate_html( self ):
		
		values = {
			'_': lambda x: _(x)
		}

		return self.renderTemplate( 'contact.html', values )
	
