
import webapp2, os, re

from library.utilities import uriFor

from library.model.report import SiteReport, SiteRating

class RateController( webapp2.RequestHandler ):

	def post( self ):
		domain = self.request.get( 'domain' )

		content = self.request.get( 'content' )
		usability = self.request.get( 'usability' )
		presentation = self.request.get( 'presentation' )

		report = SiteRating.all().filter( 'domain =', domain ).get()
		if report is None:
			report = SiteRating( domain = domain )
			report.content = report.usability = report.presentation = report.num_raters = 0
		report.content = report.content + int( content )
		report.usability = report.usability + int( usability )
		report.presentation = report.presentation + int( presentation )
		report.num_raters = report.num_raters + 1
		report.save()

		self.response.set_status( 200 )
		self.response.headers['Access-Control-Allow-Origin'] = self.request.headers['Origin']
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write( '"true"' )

