
import webapp2, os, re

from library.utilities import uriFor

class AnalyzeDomainController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' ) 		# 'http://FOOBAR.com/          '
		domain = domain.lower()				# 'http://foobar.com/      '
		domain = domain.strip() 			# 'http://foobar.com/'
		domain = domain.rstrip( '/' ) 			# 'http://foobar.com'
		domain = re.sub( '^http://', '', domain ) 	# 'foobar.com'

		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

		if len( domain ) == 0:
			url = self.request.referer
		else:
			url = uriFor( 'liveReport', domainUrl = domain )

		self.redirect( url )

