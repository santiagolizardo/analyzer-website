
import logging, os

from google.appengine.api import urlfetch

from library.task.base import BaseTask

import urllib2

import cloudstorage as gcs
from google.appengine.api import app_identity

from config import current_instance as site

from config import debug_active

from urllib import quote_plus
import time

def storeFileInCloud( data, url ):
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    sanitized_url = url.replace( 'http://', '' ).replace( '.', '-' )
    filename = '/' + bucket_name + '/screenshots/' + sanitized_url + '.png'
    gcs_file = gcs.open(
        filename,
        'w',
        content_type = 'image/png',
        options = { 'x-goog-acl': 'public-read' }
    )
    gcs_file.write(data)
    gcs_file.close()

    base_url = 'http://' + site['url'] + '/_ah/gcs' if debug_active else 'https://storage.googleapis.com'
    return base_url + filename

class ScreenshotGrabberTask( BaseTask ):

	def getName( self ):
		return 'screenshot'

	def updateView( self, beauty, data ):
		beauty.find( id = 'screenshot' )['src'] = data

	def start( self, url ):
		content = None
		
		imageData = captureScreenshotWordpress( 'http://' + url )
		if imageData is not None:
			imageUrl = storeFileInCloud(imageData, url)

			content = imageUrl
		
		self.sendAndSaveReport( url, content )

	def suggest_actions( self, actions, data, domain ):
		pass

	def generate_html_node( self, data ):
		return data

def captureScreenshotWordpress( url ):
	apiUrl = 'http://s.wordpress.com/mshots/v1/%s?w=250' % quote_plus( url )
	result = urlfetch.fetch( apiUrl, deadline = 12, follow_redirects = False )
	if result.status_code == 200:
		imageData = urllib2.urlopen( apiUrl ).read()
		return imageData
	elif result.status_code == 307:
		time.sleep( 4 )
		return captureScreenshotWordpress( url )
	else:
		return None

	return None

