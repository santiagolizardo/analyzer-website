
from google.appengine.api import app_identity
from google.appengine.api import urlfetch

import logging, json

def createShortUrl( long_url ):
	scope = "https://www.googleapis.com/auth/urlshortener"
	authorization_token, _ = app_identity.get_access_token( scope )
	payload = json.dumps({ "longUrl": long_url })

	try:
		response = urlfetch.fetch( "https://www.googleapis.com/urlshortener/v1/url?pp=1", method = urlfetch.POST, payload = payload, deadline = 4, headers = { "Content-Type": "application/json", "Authorization": "OAuth " + authorization_token })
		if response.status_code == 200:
			result = json.loads( response.content )
			return result["id"]
		logging.error( 'Urlshortener call failed. Status code %s. Body %s', response.status_code, response.content )
	except:
		logging.error( 'Urlshortener call failed' )

	return long_url

