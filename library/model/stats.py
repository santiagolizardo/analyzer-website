
from google.appengine.ext import db

class StatCounter( db.Model ):
	category = db.StringProperty( required = True )
	code = db.StringProperty( required = True )
	report_date = db.DateProperty()
	count = db.IntegerProperty( required = True, default = 1 )

