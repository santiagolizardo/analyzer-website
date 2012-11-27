
import webapp2, os

from webapp2_extras import routes

from library.controller.index import IndexController
from library.controller.analizeDomain import AnalyzeDomainController

from library.controller.liveReport import LiveReportController 
from library.controller.staticReport import StaticReportController 
from library.controller.ranking import RankingController 

debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 

config = {
	'debugActive': debugActive,
	'domain': 'domaingrasp.dev:9090' if debugActive else 'domaingrasp.com',
	'url': 'www.domaingrasp.dev:9090' if debugActive else 'www.domaingrasp.com',
}

routes = [
	webapp2.Route( '/analyze', handler = AnalyzeDomainController ),
	webapp2.Route( '/launchSubreports', handler = 'library.controller.processing.InitProcessingController' ),
	webapp2.Route( '/calculateScore', handler = 'library.controller.scores.CalculateScoreController' ),
	routes.DomainRoute( 'www.domaingrasp.<:dev|com>',
		[
			webapp2.Route( '/', handler = IndexController ),
		]
	),
	routes.DomainRoute( 'ranking.domaingrasp.<:dev|com>',
		[
			webapp2.Route( '/<:.*>', handler = RankingController, name = 'ranking' ),
		]
	),
	routes.DomainRoute( 'live-report.domaingrasp.<:dev|com>',
		[
			webapp2.Route( '/<domainUrl:.+>', handler = LiveReportController, name = 'liveReport' ),
		]
	),
	routes.DomainRoute( 'report.domaingrasp.<:dev|com>',
		[
			webapp2.Route( '/<domainUrl:.+>', handler = StaticReportController, name = 'staticReport' ),
		]
	),
]
app = webapp2.WSGIApplication( routes, debug = debugActive, config = config )

