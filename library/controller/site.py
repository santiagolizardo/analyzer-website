
from google.appengine.api import memcache
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
			report = SiteRating( domain = domain, rating_overall = 0.0 )
		report.num_raters += 1
		report.rating_content = report.rating_content + int( content )
		report.rating_usability = report.rating_usability + int( usability )
		report.rating_presentation = report.rating_presentation + int( presentation )

		overall = ( ( report.rating_content + report.rating_usability + report.rating_presentation ) / 3.0 ) / report.num_raters
		report.rating_overall = overall
		report.save()

		cache_key = 'page_' + domain
		memcache.delete( cache_key )

		self.response.set_status( 200 )
		self.response.headers['Access-Control-Allow-Origin'] = self.request.headers['Origin']
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write( '"true"' )

