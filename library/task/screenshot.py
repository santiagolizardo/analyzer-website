
import json, logging, os

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message
from google.appengine.api import files
from google.appengine.api.images import get_serving_url

from library.task.base import BaseTask

import urllib2

def storeFileInCloud( data, url ):

	filename = '/gs/domaingrasp-screenshots/' + url.replace( 'http://', '' ).replace( '.', '-' ) + '.png'
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

	def start( self, url ):

		content = self.getDefaultData() 
		actions = []
		
		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )
		if not debugActive:
			serviceApi = '18e1518747b2702d9bd216465603dbb3d74b8fea'
			screenshotSize = 'mc'
			apiUrl = 'http://api.snapito.com/web/%s/%s?url=%s' % ( serviceApi, screenshotSize, url )
			result = urlfetch.fetch( apiUrl )
						
			logging.info( result.status_code )
			if result.status_code == 200:
				imageData = urllib2.urlopen( result.final_url ).read()

				#storeFileInCloud( imageData, url )
				imageUrl = storeFileInBlobstore( imageData, url )

				logging.info( result.final_url )
				content[ self.getName() ] = imageUrl

		self.sendAndSaveReport( url, content, actions )

