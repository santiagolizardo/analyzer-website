
from collections import OrderedDict
from google.appengine.ext import db

from library.utilities.lists import remove_duplicates

class SiteReport( db.Model ):
	creationDate = db.DateTimeProperty(auto_now_add = True)
	name = db.StringProperty()
	description = db.StringProperty()
	url = db.StringProperty()
	score = db.RatingProperty()

	def __str__( self ):
		return '<SiteReport url=%s>' % self.url

	@classmethod
        def get_recent_report_urls(cls):
	    reports = db.Query(cls, projection = ('url',)).order('-creationDate').run(limit = 20)
	    urls = (report.url for report in reports)
	    unique_urls = remove_duplicates(urls)
	    return unique_urls 

	@classmethod
	def get_best_scored_report_urls(cls):
            all_reports = db.Query(cls, projection = ('url', 'score')).order('-score').run(limit = 20)
            reports = OrderedDict()
            for report in all_reports:
                if report.url not in reports:
                    reports[ report.url ] = report.score

	    return reports 

class SiteRating( db.Model ):
	domain = db.StringProperty( required = True )
	num_raters = db.IntegerProperty( default = 0 )
	rating_content = db.IntegerProperty( default = 0 )
	rating_usability = db.IntegerProperty( default = 0 )
	rating_presentation = db.IntegerProperty( default = 0 )
	rating_overall = db.FloatProperty( default = 0.0 )

class TaskReport( db.Model ):
	name = db.StringProperty( required = True )
	url = db.StringProperty( required = True )
	messageEncoded = db.TextProperty( required = True )

	def __str__( self ):
		return '<TaskReport name=%s, url=%s, messageEncoded=...>' % ( self.name, self.url )

