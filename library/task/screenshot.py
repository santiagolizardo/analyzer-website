
import json, logging, os, sys

import config

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message
from google.appengine.api import files
from google.appengine.api.images import get_serving_url

from library.task.base import BaseTask

import urllib2

from bs4 import BeautifulSoup, NavigableString

def storeFileInCloud( data, url ):

	filename = '/gs/egosize-screenshots/' + url.replace( 'http://', '' ).replace( '.', '-' ) + '.png'
	writable_file_name = files.gs.create( filename, mime_type = 'image/png', acl = 'public-read', user_metadata= { 'x-goog-project-id': '1004040993338' } )
	with files.open(writable_file_name, 'a' ) as f:
		f.write( imageData )
	files.finalize(writable_file_name)

	return filename

def storeFileInBlobstore( data, url ):

	file_name = files.blobstore.create(mime_type = 'image/png' )
	with files.open(file_name, 'a') as f:
		f.write( data )
	files.finalize(file_name)

	blob_key = files.blobstore.get_blob_key( file_name )

	return get_serving_url( blob_key )

class ScreenshotGrabberTask( BaseTask ):

	def getName( self ): return 'screenshot'

	def getDefaultData( self ):

		return { self.getName(): '/images/1x1.png' }

	def updateView( self, beauty, data ):

		beauty.find( id = 'screenshot' )['src'] = data['screenshot']

	def start( self, baseUrl ):

		url = 'http://' + baseUrl

		content = self.getDefaultData() 
		actions = []
		
		if not config.debug_active:
			# imageData = captureScreenshotSnapito( url )
			imageData = captureScreenshotWordpress( url )
			if imageData is not None:
				# storeFileInCloud( imageData, url )
				imageUrl = storeFileInBlobstore( imageData, url )

				content[ self.getName() ] = imageUrl
		
		self.sendAndSaveReport( url, content, actions )

def captureScreenshotSnapito( url ):
	serviceApi = '18e1518747b2702d9bd216465603dbb3d74b8fea'
	screenshotSize = 'mc'

	try:
		apiUrl = 'http://api.snapito.com/web/%s/%s/%s' % ( serviceApi, screenshotSize, url )
		result = urlfetch.fetch( apiUrl, deadline = 30 )
		if result.status_code == 200:
			imageData = urllib2.urlopen( result.final_url ).read()
			return imageData
	except:
		logging.warning( sys.exc_info()[1] )

	return None

from urllib import quote_plus
import time

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

