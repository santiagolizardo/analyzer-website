
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from library.utilities import uriFor
from google.appengine.ext import db

class RankingController( StandardPageController ):

    def get( self, country = None ):

        sitesQuery = SiteReport.all()
        sitesQuery.order( '-score' )
        
        sites = []
        i = 0
        for entity in sitesQuery.run():
            i += 1
            site = db.to_dict( entity, { 'position': i, 'lastReportUrl': uriFor( 'staticReport', domainUrl = entity.url ) } ) 
            sites.append( site )

        values = {
            'pageTitle': 'Ranking of the most optimized websites for SEO/SEM/WPO - EGOsize',
            'pageDescription': 'Discover what are the most successful websites in terms of their UX, SEO/SEM and WPO practices. Learn from their reports for free.',
            'sites': sites
        }
        
        html = self.renderTemplate( 'ranking.html', values)

        self.writeResponse( html )

