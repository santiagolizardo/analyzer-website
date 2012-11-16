
import webapp2
import os

from library.controller.index import IndexController
from library.controller.analizeDomain import AnalyzeDomainController
from library.controller.viewDomain import ViewDomainController

from library.task.fetchDomain import FetchDomainTaskController

routes = [
	( '/', IndexController ),
	( '/analyze', AnalyzeDomainController ),
	( '/initProcessing', 'library.controller.initProcessing.InitProcessingController' ),
	( '/task/fetch-domain', FetchDomainTaskController ),
	webapp2.Route( '/view/<domainUrl>', handler = ViewDomainController, name = 'viewDomain' ),
]
app = webapp2.WSGIApplication( routes, debug = True )

