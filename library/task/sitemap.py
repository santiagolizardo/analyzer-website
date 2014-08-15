
import logging

from google.appengine.api import urlfetch

from library.task.base import BaseTask

class SitemapXmlCheckerTask( BaseTask ):

	def getName( self ):
		return 'sitemapXml'

	def updateView( self, beauty, sitemap_xml ):
		beauty.find( id = 'sitemapXml' ).string.replace_with( self.generate_html_node( sitemap_xml ) )

	def start( self, domain ):
		try:
			url = 'http://' + domain + '/sitemap.xml'
			result = urlfetch.fetch( url, deadline = 4 )
			sitemap_xml = {
				'status_code': result.status_code,
				'content_type': result.headers['Content-type'],
				'url': url,
			}
			self.sendAndSaveReport( domain, sitemap_xml, [] )
		except Exception, ex:
			logging.error( ex )


	def suggest_actions( self, actions, sitemap_xml, domain ):
		if 200 == sitemap_xml['status_code']:
			html_link = self.generate_html_link( sitemap_xml['url'] )
			actions.append({ 'status': 'regular', 'description': 'The %s file is missing'  % html_link })
		else:
			if 'text/xml' in sitemap_xml['content_type']:
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'regular', 'description': 'Fix the content type for the %s URL' % url })


	def generate_html_node( self, sitemap_xml ):
		if 404 == sitemap_xml['status_code']:
			return 'Missing'

		html_link = self.generate_html_link( sitemap_xml['url'] )
		if 'text/xml' in sitemap_xml['content_type']:
			return html_link

		return '%(html_link)s has been found but with a wrong content type (%(contentType)s)' % { 'html_link': html_link, 'contentType': sitemap_xml['content_type'] } 

	def generate_html_link( self, url ):
		return '<a href="%(url)s" class="external" rel="nofollow" target="_blank">%(url)s</a>' % { 'url': url }

