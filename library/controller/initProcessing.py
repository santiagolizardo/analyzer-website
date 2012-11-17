
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from google.appengine.api.channel import create_channel

from google.appengine.ext import deferred

from library.task.twitter import checkTwitterAccount
from library.task.robots import checkForRobotsTxt, checkForSitemapXml
from library.task.screenshot import grabScreenshot

class InitProcessingController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )

		fullUrl = 'http://' + domainUrl

		logging.info( '>>>> Enqueueing task' )
		taskParams = {
			'url': domainUrl,
			'channelId': channelId,
		}
		
		url = 'http://tldextract.appspot.com/api/extract?url=' + fullUrl
		result = urlfetch.fetch( url )
		apiData = json.loads( result.content )
		baseDomain = apiData['domain']
		
		taskqueue.add( url = '/task/fetch-domain', params = taskParams )
		
		deferred.defer( checkTwitterAccount, baseDomain, channelId )
		deferred.defer( checkForRobotsTxt, fullUrl, channelId )
		deferred.defer( checkForSitemapXml, fullUrl, channelId )
		deferred.defer( grabScreenshot, fullUrl, channelId )

