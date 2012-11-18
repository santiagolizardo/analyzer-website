
import webapp2, os 

from library.utilities import uriFor

class AnalyzeDomainController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' )
		domain = domain.strip()
		domain = domain.lower()

		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

		url = uriFor( 'liveReport', domainUrl = domain )

		self.redirect( url )

