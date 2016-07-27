
from library.controller.page import StandardPageController

from library.model.report import SiteReport, SiteRating

from library.utilities import uriFor
from google.appengine.ext import db

class RankingController( StandardPageController ):

	def get( self, country = None ):

		sites_by_audit_score = self.get_sites_by_audit_score()
		sites_by_user_reviews = self.get_sites_by_user_reviews()

		values = {
			'pageTitle': 'Ranking of the most optimized websites for SEO/SEM/WPO - %s' % self.current_instance['name'],
			'pageDescription': 'Discover what are the most successful websites in terms of their UX, SEO/SEM and WPO practices. Learn from their reports for free.',
			'sites_by_audit_score': sites_by_audit_score,
			'sites_by_user_reviews': sites_by_user_reviews,
		}

		html = self.renderTemplate( 'ranking.html', values)

		self.writeResponse( html )

	def get_sites_by_audit_score( self ):
		sites = []

		site_scores = SiteReport.all()
		site_scores.order( '-score' )
		
		for result in site_scores.run( limit = 20 ):
			site = db.to_dict( result, { 'lastReportUrl': uriFor( 'staticReport', domainUrl = result.url ) } ) 
			sites.append( site )

		return sites

	def get_sites_by_user_reviews( self ):
		sites = []

		site_ratings = SiteRating.all()
		site_ratings.order( '-rating_overall' )

		for result in site_ratings.run( limit = 20 ):
			site = db.to_dict( result, { 'lastReportUrl': uriFor( 'staticReport', domainUrl = result.domain ) } )
			sites.append( site )

		return sites

