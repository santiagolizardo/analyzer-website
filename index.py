
import webapp2, os

from webapp2_extras import routes

from library.controller.index import IndexController
from library.controller.analizeDomain import AnalyzeDomainController

from library.controller.liveReport import LiveReportController 
from library.controller.staticReport import StaticReportController 

debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 

config = {
	'debugActive': debugActive,
	'url': 'www.domaingrasp.dev:9090' if debugActive else 'www.domaingrasp.com'
}

routes = [
	( '/', IndexController ),
	( '/analyze', AnalyzeDomainController ),
	( '/initProcessing', 'library.controller.initProcessing.InitProcessingController' ),
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

