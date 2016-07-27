
from library.controller.page import StandardPageController

from library.model.report import SiteReport

class RobotsController(StandardPageController):

    def get( self ):
        values = {
            'domain': self.current_instance['domain']
        }
        
        html = self.renderTemplate('robots.txt', values)

        self.writeResponse(html, 'text/plain; charset=utf-8')

class SitemapController(StandardPageController):

    def get( self ):
	sites = SiteReport.all()

        values = {
            'domain': self.current_instance['domain'],
            'sites': sites
        }
        
        html = self.renderTemplate('sitemap.xml', values)

        self.writeResponse(html, 'text/xml; charset=utf-8')

