
from google.appengine.ext import db

class Domain( db.Model ):
	url = db.StringProperty( required = True )
	analysisDate = db.DateTimeProperty( auto_now_add = True )

