
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from config import current_instance as site

class RobotsController( StandardPageController ):

    def get( self ):
        values = {
            'domain': site['domain']
        }
        
        html = self.renderTemplate('robots.txt', values)

        self.writeResponse(html, 'text/plain; charset=utf-8')

class SitemapController( StandardPageController ):

    def get( self ):
	sites = SiteReport.all()

        values = {
            'domain': site['domain'],
            'sites': sites
        }
        
        html = self.renderTemplate('sitemap.xml', values)

        self.writeResponse(html, 'text/xml; charset=utf-8')

