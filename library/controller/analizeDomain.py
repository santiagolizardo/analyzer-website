
import webapp2

from google.appengine.api import taskqueue

class AnalyzeDomainController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' )
		taskqueue.add( url = '/task/fetch-domain', params = { 'domain': domain } )


