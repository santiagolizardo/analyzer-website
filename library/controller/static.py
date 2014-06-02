
from library.controller.page import StandardPageController

from library.model.report import SiteReport

class SitemapController( StandardPageController ):

    def get( self ):

	sites = SiteReport.all()

        values = {
            'pageTitle': 'See what EGO size has to tell about your site and your competitors',
            'pageDescription': 'Check a detailed list of EGO size features. All of them are free to use and immediately available.',
	    'sites': sites,
        }
        
        html = self.renderTemplate( 'sitemap.xml', values)

        self.writeResponse( html, 'text/xml; charset=utf-8' )

class PricingController( StandardPageController ):

    def get( self, country = None ):
        self.addStyleSheet( '/styles/pricing.css' )

        values = {
            'pageTitle': 'Pricing - Egosize',
	    'pageDescription': 'The Egosize pricing schema is simple. Freemium services are available.',
        }
        
        html = self.renderTemplate( 'pricing.html', values)

        self.writeResponse( html )

