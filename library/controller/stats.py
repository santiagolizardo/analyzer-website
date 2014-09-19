
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

	domainTlds = DomainTld.all().filter( 'report_date =', None )
	htmlDocumentTypes = HtmlDocumentType.all().filter( 'report_date =', None )

        values = {
		'pageTitle': 'Domain, social and other popular site statistics ',
		'pageDescription': 'Discover what are the most successful websites in terms of their UX, SEO/SEM and WPO practices. Learn from their reports for free.',
		'sites': sites,
		'domainTlds': domainTlds,
		'htmlDocumentTypes': htmlDocumentTypes,
        }
        
        html = self.renderTemplate( 'stats.html', values)

        self.writeResponse( html )

