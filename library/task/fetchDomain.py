
import webapp2

class FetchDomainTaskController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' )

		import logging
		logging.info( 'Analyzing domain: ' + domain )


