
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class FaviconCheckerTask( BaseTask ):

	def getName( self ):
		return 'pageFavicon'

	def updateView( self, beauty, favicon ):
		beauty.find( id = 'pageFavicon' ).string.replace_with( self.generate_html_node( favicon ) )

	def start( self, domain ):
		try:
			url = self.create_url( domain ) 
			result = urlfetch.fetch( url, deadline = 3 )
			favicon = url if result.status_code == 200 else None
			self.sendAndSaveReport( domain, favicon, [] )
		except Exception, ex:
			logging.error( ex )

	def create_url( self, domain ):
		return 'http://' + domain + '/favicon.ico'

	def suggest_actions( self, actions, favicon, domain ):
		if favicon is None:
			url = self.create_url( domain )
			actions.append({ 'status': 'bad', 'description': 'The <a href="%(url)s" class="external" rel="nofollow" target="_blank">%(url)s</a> file is missing' % { 'url': url } })
		else:
			actions.append({ 'status': 'good' })

	def generate_html_node( self, favicon ):
		if favicon is None:
			return 'Missing'

		htmlLink = '<a href="%(faviconUrl)s" class="external" rel="nofollow" target="_blank"><img src="%(faviconUrl)s" alt="Favicon" /></a>' % { 'faviconUrl': favicon }
		return htmlLink

