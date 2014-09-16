
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import sys

class RobotsTxtCheckerTask( BaseTask ):

	def getName( self ):
		return 'robotsTxt'

	def getDefaultData( self ):
		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):
		beauty.find( id = 'robotsTxt' ).string.replace_with( self.generate_html_node( data ) )

	def start( self, domain ):
		robots_txt = None
		try:
			url = 'http://' + domain + '/robots.txt'
			result = urlfetch.fetch( url, deadline = 4 )
			robots_txt = {
				'status_code': result.status_code,
				'content_type': result.headers['Content-type'],
				'url': url,
			}
		except Exception, ex:
			logging.error( ex )
		
		self.sendAndSaveReport( domain, robots_txt )

	def suggest_actions( self, actions, robots_txt, domain ):
		if 200 == robots_txt['status_code']:
			html_link = self.generate_html_link( robots_txt['url'] )
			actions.append({ 'status': 'regular', 'description': 'The %s file is missing'  % html_link })
		else:
			if 'text/plain' in robots_txt['content_type']:
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'regular', 'description': 'Fix the content type for the %s URL' % robots_txt['url'] })

	def generate_html_node( self, robots_txt ):
		if 404 == robots_txt['status_code']:
			return 'Missing'

		html_link = self.generate_html_link( robots_txt['url'] )
		if 'text/plain' in robots_txt['content_type']:
			return html_link

		return '%(html_link)s has been found but with a wrong content type (%(contentType)s)' % { 'html_link': html_link, 'contentType': robots_txt['content_type'] } 

	def generate_html_link( self, url ):
		return '<a href="%(url)s" class="external" rel="nofollow" target="_blank">%(url)s</a>' % { 'url': url }

