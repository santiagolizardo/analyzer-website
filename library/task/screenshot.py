
import json, logging

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

def grabScreenshot( url, channelId ):
	serviceApi = '18e1518747b2702d9bd216465603dbb3d74b8fea'
	screenshotSize = 'sc'
	url = 'http://api.snapito.com/web/%s/%s?url=%s' % ( serviceApi, screenshotSize, url )
	result = urlfetch.fetch( url )

	body = None
	logging.info( result.status_code )
	if result.status_code == 200:
		logging.info( result.final_url )
		body = result.final_url 

	response = {
		'type': 'screenshot',
		'body': body,
	}

	send_message( channelId, json.dumps( response ) )


