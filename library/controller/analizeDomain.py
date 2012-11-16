
import webapp2

class AnalyzeDomainController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' )

		self.redirect_to( 'viewDomain', domainUrl = domain )

