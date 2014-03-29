
import webapp2, os, logging

from webapp2_extras import routes

from library.controller.index import IndexController
from library.controller.analizeDomain import AnalyzeDomainController

from library.controller.liveReport import LiveReportController 
from library.controller.staticReport import StaticReportController 
from library.controller.ranking import RankingController 
from library.controller.errorPage import ErrorPageController
from library.controller.channel import ChannelController

debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 

config = {
	'debugActive': debugActive,
	'domain': 'egosize.dev:9090' if debugActive else 'egosize.com',
	'url': 'www.egosize.dev:9090' if debugActive else 'www.egosize.com',
}

routes = [
	webapp2.Route( '/_ah/channel/connected/', handler = ChannelController ),
	webapp2.Route( '/_ah/channel/disconnected/', handler = ChannelController ),
	webapp2.Route( '/analyze', handler = AnalyzeDomainController ),
	webapp2.Route( '/launchSubreports', handler = 'library.controller.processing.InitProcessingController' ),
	webapp2.Route( '/calculateScore', handler = 'library.controller.scores.CalculateScoreController' ),
	webapp2.Route( '/sitemap.xml', handler = 'library.controller.static.SitemapController' ),
	routes.DomainRoute( 'www.egosize.<:dev|com>',
		[
			webapp2.Route( '/', handler = IndexController ),
			webapp2.Route( '/features', handler = 'library.controller.static.FeaturesController', name = 'features' ),
			webapp2.Route( '/rate', handler = 'library.controller.site.RateController' ),
		]
	),
	routes.DomainRoute( 'ranking.egosize.<:dev|com>',
		[
			webapp2.Route( '/<:.*>', handler = RankingController, name = 'ranking' ),
		]
	),
	routes.DomainRoute( 'pricing.egosize.<:dev|com>',
		[
			webapp2.Route( '/<:.*>', handler = 'library.controller.static.PricingController' ),
		]
	),
	routes.DomainRoute( 'stats.egosize.<:dev|com>',
		[
			webapp2.Route( '/<:.*>', handler = 'library.controller.stats.Index' ),
		]
	),
	routes.DomainRoute( 'live-report.egosize.<:dev|com>',
		[
			webapp2.Route( '/<domainUrl:.+>', handler = LiveReportController, name = 'liveReport' ),
		]
	),
	routes.DomainRoute( 'report.egosize.<:dev|com>',
		[
			webapp2.Route( '/<domainUrl:.+>', handler = StaticReportController, name = 'staticReport' ),
		]
	),
]

def handle_404(request, response, exception):
	logging.exception(exception)

	controller = ErrorPageController( request, response )
	controller.get()

app = webapp2.WSGIApplication( routes, debug = debugActive, config = config )
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_404

