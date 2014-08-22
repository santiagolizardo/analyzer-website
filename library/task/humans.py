
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class HumansTxtCheckerTask( BaseTask ):

	def getName( self ):
		return 'humansTxt'

	def updateView( self, beauty, humans_txt ):
		beauty.find( id = 'humansTxt' ).string.replace_with( self.generate_html_node( humans_txt ) )

	def start( self, domain ):
		humans_txt = None
		try:
			url = 'http://' + domain + '/humans.txt'
			result = urlfetch.fetch( url, deadline = 4 )
			humans_txt = {
				'status_code': result.status_code,
				'content_type': result.headers['Content-type'],
				'url': url,
			}
		except Exception, ex:
			logging.error( ex )
		
		self.sendAndSaveReport( domain, humans_txt )

	def suggest_actions( self, actions, humans_txt, domain ):
		if 200 == humans_txt['status_code']:
			html_link = self.generate_html_link( humans_txt['url'] )
			actions.append({ 'status': 'regular', 'description': 'The %s file is missing'  % html_link })
		else:
			if 'text/plain' in humans_txt['content_type']:
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'regular', 'description': 'Fix the content type for the %s URL' % humans_txt['url'] })

	def generate_html_node( self, humans_txt ):
		if 404 == humans_txt['status_code']:
			return 'Missing'

		html_link = self.generate_html_link( humans_txt['url'] )
		if 'text/plain' in humans_txt['content_type']:
			return html_link

		return '%(html_link)s has been found but with a wrong content type (%(contentType)s)' % { 'html_link': html_link, 'contentType': humans_txt['content_type'] } 

	def generate_html_link( self, url ):
		return '<a href="%(url)s" class="external" rel="nofollow" target="_blank">%(url)s</a>' % { 'url': url }

