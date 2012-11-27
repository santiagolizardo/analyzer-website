
from google.appengine.ext import db

class SiteReport( db.Model ):
	
	creationDate = db.DateTimeProperty( auto_now_add = True )
	name = db.StringProperty()
	description = db.StringProperty()
	url = db.StringProperty()
	score = db.RatingProperty()

	def __str__( self ):
		
		return '<SiteReport url=%s>' % self.url

class TaskReport( db.Model ):

	name = db.StringProperty( required = True )
	url = db.StringProperty( required = True )
	messageEncoded = db.TextProperty( required = True )

	def __str__( self ):
		return '<TaskReport name=%s, url=%s, messageEncoded=...>' % ( self.name, self.url )

