
from google.appengine.ext import db

class TaskReport( db.Model ):

	name = db.StringProperty( required = True )
	url = db.StringProperty( required = True )
	messageEncoded = db.TextProperty( required = True )

	def __str__( self ):
		return '<TaskReport name=%s, url=%s, messageEncoded=...>' % ( self.name, self.url )

