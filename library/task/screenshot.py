
import json, logging, os

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

from library.task.base import BaseTask

class ScreenshotGrabberTask( BaseTask ):

	def getName( self ): return 'screenshot'

	def start( self, url ):

		content = 'http://img5.wsimg.com/pc/img/1/86649_pc_header.png'
		
		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 
		if not debugActive:
			serviceApi = '18e1518747b2702d9bd216465603dbb3d74b8fea'
			screenshotSize = 'mc'
			url = 'http://api.snapito.com/web/%s/%s?url=%s' % ( serviceApi, screenshotSize, url )
			result = urlfetch.fetch( url )
			
			content = None
			logging.info( result.status_code )
			if result.status_code == 200:
				logging.info( result.final_url )
				content = result.final_url 

		self.saveReport( url, content )
		self.sendMessage( content )

