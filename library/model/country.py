
from google.appengine.ext import db

class CountryIp( db.Model ):
	ip_from = db.StringProperty( required = True )
	ip_to = db.StringProperty( required = True )

	def __str__( self ):
		return '<CountryIp>'

