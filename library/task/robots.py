
import webapp2, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

from library.task.base import BaseTask

class RobotsTxtCheckerTask( BaseTask ):

	def getName( self ): return 'robotsTxt'

	def getDefaultData( self ):

		return 'N/A'

	def start( self, domain ):

		url = domain + '/robots.txt'
		result = urlfetch.fetch( url )

		content = self.getDefaultData()
		actions = []

		if result.status_code == 200:
			content = url
			actions.append({ 'status': 'good' })
		elif result.status_code == 404:
			content = 'Missing' 
			actions.append({ 'status': 'regular', 'description': 'Add a robots.txt file to your site' })

		self.sendAndSaveReport( url, content, actions )

class SitemapXmlCheckerTask( BaseTask ):

	def getName( self ): return 'sitemapXml'

	def getDefaultData( self ):

		return 'N/A'

	def start( self, domain ):

		url = domain + '/sitemap.xml'
		result = urlfetch.fetch( url )

		content = self.getDefaultData()
		actions = []

		if result.status_code == 200:
			content = url
			actions.append({ 'status': 'good' })
		elif result.status_code == 404:
			content = 'Missing' 
			actions.append({ 'status': 'regular', 'description': 'Add a sitemap.xml to your site' })

		self.sendAndSaveReport( url, content, actions )

