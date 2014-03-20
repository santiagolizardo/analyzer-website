
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
            'pageTitle': 'See what EGO size has to tell about your site and your competitors',
            'pageDescription': 'Check a detailed list of EGO size features. All of them are free to use and immediately available.',
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
            'pageTitle': 'A list of things to take care when optimizing Websites - EGOsize',
            'pageDescription': 'A comprehensive list of things to do to have better SERP and increase conversions. All of them are part of EGOsize reports.',
	    'features': features,
        }
        
        html = self.renderTemplate( 'features.html', values)

        self.writeResponse( html )

class PricingController( StandardPageController ):

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
            'pageTitle': 'Pricing (FREE!) - EGOsize',
	    'pageDescription': 'The EGOsize pricing schema is simple: Free service',
	    'features': features,
        }
        
        html = self.renderTemplate( 'pricing.html', values)

        self.writeResponse( html )

