
from google.appengine.ext import db

class ResponseBody( db.Model ):
	domain = db.StringProperty( required = True )
	length = db.IntegerProperty( required = True )
	body = db.TextProperty( required = True )
	retrievalDate = db.DateTimeProperty( auto_now_add = True )

