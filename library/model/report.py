
from google.appengine.ext import db

class TaskReport( db.Model ):

	name = db.StringProperty( required = True )
	url = db.StringProperty( required = True )
	content = db.TextProperty( required = True )

	def __str__( self ):
		return '<Report name=%s, url=%s, content=...>' % ( self.name, self.url )

