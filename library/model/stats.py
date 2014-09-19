
from google.appengine.ext import db

class DomainTld( db.Model ):
	code = db.StringProperty( required = True )
	report_date = db.DateProperty()
	count = db.IntegerProperty( required = True, default = 1 )

class HtmlDocumentType( db.Model ):
	code = db.StringProperty( required = True )
	report_date = db.DateProperty()
	count = db.IntegerProperty( required = True, default = 1 )

