
import sys, logging
import urllib2, json
 
class RoboWhois:

	def __init__( self ):
		self.apikey = 'bc6ee2c8c82f225d95aa7ccebd60ce44'

	def whois( self, domain ):
		try:
			url = "http://api.whoapi.com/?domain=%s&apikey=%s&r=whois" % ( domain, self.apikey )

			opener = urllib2.build_opener()
			request = urllib2.Request( url )
			response = opener.open( request )

			body = response.read()
			jsonresponse = json.loads( body )
			if jsonresponse['status'] != '0':
				logging.warning( jsonresponse['status_desc'] if 'status_desc' in jsonresponse else jsonresponse['status'] )
				return None
			return jsonresponse
		except Exception, ex:
			logging.error( ex )
			return None

if __name__ == '__main__':
	import pprint

	whois = RoboWhois()
	pprint.pprint( whois.whois( 'example.com' ) )

