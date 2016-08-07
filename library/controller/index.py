
from library.controller.page import StandardPageController

from library.model.report import SiteReport

from google.appengine.ext import db
from library.utilities import uriFor

from google.appengine.api import memcache

class IndexController( StandardPageController ):

	def get( self ):
		html = memcache.get( 'page-index' )
		if html is None:
			html = self.generate_html()
			memcache.set( 'page-index', html, time = 3600 )

		self.writeResponse( html )

	def generate_html( self ):
	        mostRecentSites = SiteReport.get_recent_report_urls()
	        bestScoredSites = SiteReport.get_best_scored_report_urls()

		values = {
			'recentDomains': mostRecentSites,
			'sitesRanking': bestScoredSites,
		}

		self.addJavaScript( '/scripts/index.js' )

		return self.renderTemplate( 'index.html', values )

