
from library.controller.page import StandardPageController

import logging, json

from datetime import date

from bs4 import BeautifulSoup, NavigableString

from library.model.report import SiteReport

from library.utilities import uriFor
from google.appengine.ext import db

class RankingController( StandardPageController ):

    def get( self, country = None ):
        self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
        self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
        self.addJavaScript( 'https://www.google.com/jsapi' )
        self.addJavaScript( '/scripts/staticReport.js' )
        
        self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
        self.addStyleSheet( '/styles/allmedia.css' )

        sitesQuery = SiteReport.all()
        sitesQuery.order( '-score' )
        
        sites = []
        i = 0
        for entity in sitesQuery.run():
            i += 1
            site = db.to_dict( entity, { 'position': i, 'lastReportUrl': uriFor( 'staticReport', domainUrl = entity.url ) } ) 
            sites.append( site )

        values = {
            'pageTitle': 'Best SEO Social Websites  | Ranking of the top Websites SEO Social by DomainGrasp.com',
            'pageDescription': 'Check this list out! A ranking with the best Websites in terms of SEO and Social factors',
            'sites': sites
        }
        
        html = self.renderTemplate( 'ranking.html', values)

        self.writeResponse( html )

