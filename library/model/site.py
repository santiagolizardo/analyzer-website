
from google.appengine.ext import db

class SiteReview( db.Model ):
	domain = db.StringProperty( required = True )
	title = db.StringProperty()
	strengths = db.StringListProperty()
	weaknesses = db.StringListProperty()
	mod_date = db.DateTimeProperty( auto_now = True )

