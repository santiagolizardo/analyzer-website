
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from library.utilities import uriFor
from google.appengine.ext import db

from library.model.stats import *

class Index( StandardPageController ):

    def get( self, country = None ):

        sitesQuery = SiteReport.all()
        sitesQuery.order( '-score' )

	# self.addJavaScript( '/scripts/flotr2/flotr2.min.js' )
	self.addJavaScript( '/scripts/Chart.min.js' )
	self.addJavaScript( '/scripts/stats.js' )
        
        sites = []
        i = 0
        for entity in sitesQuery.run():
            i += 1
            site = db.to_dict( entity, { 'position': i, 'lastReportUrl': uriFor( 'staticReport', domainUrl = entity.url ) } ) 
            sites.append( site )

	domainTlds = StatCounter.all().filter( 'category = ', 'domain_tld' ).filter('report_date =', None ).order( '-count' )
	htmlDocumentTypes = StatCounter.all().filter( 'category = ', 'html_document_type').filter('report_date =', None ).order( '-count' )
	pageRanks = StatCounter.all().filter( 'category =', 'page_rank' ).order( 'code' )

        values = {
		'pageTitle': 'Domain, social and other popular site statistics ',
		'pageDescription': 'Discover what are the most successful websites in terms of their UX, SEO/SEM and WPO practices. Learn from their reports for free.',
		'sites': sites,
		'domainTlds': domainTlds,
		'htmlDocumentTypes': htmlDocumentTypes,
		'pageRanks': pageRanks,
        }
        
        html = self.renderTemplate( 'stats.html', values)

        self.writeResponse( html )

