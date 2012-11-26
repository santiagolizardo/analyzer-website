
import webapp2, os, re

from library.utilities import uriFor

class AnalyzeDomainController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' ) 		# 'http://FOOBAR.com/    '
		domain = domain.strip() 			# 'http://FOOBAR.com/'
		domain = domain.rstrip( '/' ) 			# 'http://FOOBAR.com'
		domain = re.sub( '^http://', '', domain ) 	# 'FOOBAR.com'
		domain = domain.lower() 			# 'foobar.com'

		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

		url = uriFor( 'liveReport', domainUrl = domain )

		self.redirect( url )

