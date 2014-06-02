
import webapp2, os, re

from library.utilities import uriFor

from library.model.report import SiteReport

class AnalyzeDomainController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' ) 		# 'http://FOOBAR.com/          '
		domain = domain.lower()				# 'http://foobar.com/      '
		domain = domain.strip() 			# 'http://foobar.com/'
		domain = domain.rstrip( '/' ) 			# 'http://foobar.com'
		domain = re.sub( '^http://', '', domain ) 	# 'foobar.com'

		if len( domain ) == 0:
			url = self.request.referer
		else:
			report = SiteReport.all().filter( 'url =', domain ).get()

			reportType = 'liveReport' if report is None else 'staticReport'

			url = uriFor( reportType, domainUrl = domain )

		self.redirect( url )

