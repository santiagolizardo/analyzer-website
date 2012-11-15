
import webapp2
import os

from library.controller.index import IndexController
from library.controller.analizeDomain import AnalyzeDomainController

from library.task.fetchDomain import FetchDomainTaskController

routes = [
	( '/', IndexController ),
	( '/analyze', AnalyzeDomainController ),
	( '/task/fetch-domain', FetchDomainTaskController ),
]
app = webapp2.WSGIApplication( routes, debug = True )

