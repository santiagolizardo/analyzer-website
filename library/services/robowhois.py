
import sys, logging
import urllib2, json

from local_config import whoapi as whoapi_config

class RoboWhois:

	def whois( self, domain ):
		try:
			url = "http://api.whoapi.com/?domain=%s&apikey=%s&r=whois" % ( domain, whoapi_config['apiKey'] )

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

