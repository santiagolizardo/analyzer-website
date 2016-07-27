
from google.appengine.ext import vendor
vendor.add('vendor')

import sys
sys.path.append( 'externals/tweepy' )
sys.path.append( 'externals/awis' )
sys.path.append( 'externals/oauthlib' )
sys.path.append( 'externals/requests' )
sys.path.append( 'externals/requests-oauthlib' )
sys.path.append( 'externals/requests-toolbelt' )
sys.path.append( 'externals/gcs-client/python/src' )

import config
config.load_current_instance()
from config import current_instance as site

import webapp2, os, logging

from webapp2_extras import routes

from library.controller.index import IndexController
from library.controller.analizeDomain import AnalyzeDomainController

from library.controller.liveReport import LiveReportController 
from library.controller.search import SearchController 
from library.controller.staticReport import StaticReportController 
from library.controller.ranking import RankingController 
from library.controller.errorPage import ErrorPageController
from library.controller.channel import ChannelController

def handle_warmup( request ):
        response = request.response
        response.set_status(200)
        response.write('ok')

routes = [
	webapp2.Route( '/_ah/warmup', handler = handle_warmup ),
	webapp2.Route( '/_ah/channel/connected/', handler = ChannelController ),
	webapp2.Route( '/_ah/channel/disconnected/', handler = ChannelController ),
	webapp2.Route( '/addReview', handler = 'library.controller.site.AddReviewController' ),
	webapp2.Route( '/analyze', handler = AnalyzeDomainController ),
	webapp2.Route( '/launchSubreports', handler = 'library.controller.processing.InitProcessingController' ),
	webapp2.Route( '/calculateScore', handler = 'library.controller.scores.CalculateScoreController' ),
	webapp2.Route( '/sitemap.xml', handler = 'library.controller.static.SitemapController' ),
	webapp2.Route( '/robots.txt', handler = 'library.controller.static.RobotsController' ),
	routes.DomainRoute( site['domain'],
		[
			webapp2.Route( '/', handler = IndexController ),
			webapp2.Route( '/rate', handler = 'library.controller.site.RateController' ),
		]
	),
	routes.DomainRoute( 'search.' + site['domain'],
		[
			webapp2.Route( '/<query:.+>', handler = SearchController, name = 'search' ),
		]
	),
	routes.DomainRoute( 'ranking.' + site['domain'],
		[
			webapp2.Route( '/<:.*>', handler = RankingController, name = 'ranking' ),
		]
	),
	routes.DomainRoute( 'stats.' + site['domain'],
		[
			webapp2.Route( '/<:.*>', handler = 'library.controller.stats.Index' ),
		]
	),
	routes.DomainRoute( 'live-report.' + site['domain'],
		[
			webapp2.Route( '/<domainUrl:.+>', handler = LiveReportController, name = 'liveReport' ),
		]
	),
	routes.DomainRoute( 'report.' + site['domain'],
		[
			webapp2.Route( '/<domainUrl:.+>', handler = StaticReportController, name = 'staticReport' ),
		]
	),
]

def handle_404( request, response, exception ):
	logging.exception( exception )

	controller = ErrorPageController( request, response )
	controller.get()

app = webapp2.WSGIApplication( routes, debug = config.debug_active )
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_404

