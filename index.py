
import sys
sys.path.append( 'vendor' )
sys.path.append( 'externals/tweepy' )
sys.path.append( 'externals/awis' )

import config
config.load_current_instance()

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

domain_ext = '<:com.dev|es.dev|com|es>'

routes = [
	webapp2.Route( '/_ah/channel/connected/', handler = ChannelController ),
	webapp2.Route( '/_ah/channel/disconnected/', handler = ChannelController ),
	webapp2.Route( '/addReview', handler = 'library.controller.site.AddReviewController' ),
	webapp2.Route( '/analyze', handler = AnalyzeDomainController ),
	webapp2.Route( '/launchSubreports', handler = 'library.controller.processing.InitProcessingController' ),
	webapp2.Route( '/calculateScore', handler = 'library.controller.scores.CalculateScoreController' ),
	webapp2.Route( '/sitemap.xml', handler = 'library.controller.static.SitemapController' ),
	routes.DomainRoute( 'www.egosize.' + domain_ext,
		[
			webapp2.Route( '/', handler = IndexController ),
			webapp2.Route( '/rate', handler = 'library.controller.site.RateController' ),
		]
	),
	routes.DomainRoute( 'search.egosize.' + domain_ext,
		[
			webapp2.Route( '/<query:.+>', handler = SearchController, name = 'search' ),
		]
	),
	routes.DomainRoute( 'ranking.egosize.' + domain_ext,
		[
			webapp2.Route( '/<:.*>', handler = RankingController, name = 'ranking' ),
		]
	),
	routes.DomainRoute( 'stats.egosize.' + domain_ext,
		[
			webapp2.Route( '/<:.*>', handler = 'library.controller.stats.Index' ),
		]
	),
	routes.DomainRoute( 'live-report.egosize.' + domain_ext,
		[
			webapp2.Route( '/<domainUrl:.+>', handler = LiveReportController, name = 'liveReport' ),
		]
	),
	routes.DomainRoute( 'report.egosize.' + domain_ext,
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

