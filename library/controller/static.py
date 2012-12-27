
from library.controller.page import StandardPageController

import logging, json

from datetime import date

from bs4 import BeautifulSoup, NavigableString

from library.model.report import SiteReport

from library.utilities import uriFor
from google.appengine.ext import db

class SitemapController( StandardPageController ):

    def get( self ):
        self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
        self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
        
        self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
        self.addStyleSheet( '/styles/allmedia.css' )

	sites = SiteReport.all()

        values = {
            'pageTitle': 'See what DomainGrasp has to tell about your site and your competitors',
            'pageDescription': 'Check a detailed list of DomainGrasp features. All of them are free to use and immediately available.',
	    'sites': sites,
        }
        
        html = self.renderTemplate( 'sitemap.xml', values)

        self.writeResponse( html, 'text/xml; charset=utf-8' )

class FeaturesController( StandardPageController ):

    def get( self, country = None ):
        self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
        self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
        
        self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
        self.addStyleSheet( '/styles/allmedia.css' )

	features = (
		'Number of indexed pages on Google',
		'Page title and description',
		'Meta keywords',
		'Sitemap XML',
		'Robots TXT',
		'Load time',
		'HTML errors and warnings',
	)

        values = {
            'pageTitle': 'See what DomainGrasp has to tell about your site and your competitors',
            'pageDescription': 'Check a detailed list of DomainGrasp features. All of them are free to use and immediately available.',
	    'features': features,
        }
        
        html = self.renderTemplate( 'features.html', values)

        self.writeResponse( html )

class AboutController( StandardPageController ):

    def get( self, country = None ):
        self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
        self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
        
        self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
        self.addStyleSheet( '/styles/allmedia.css' )

        values = {
            'pageTitle': 'About the DomainGrasp project',
            'pageDescription': 'A few words on DomainGrasp mission and history',
        }
        
        html = self.renderTemplate( 'about.html', values)

        self.writeResponse( html )

