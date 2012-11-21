
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import create_channel

from google.appengine.ext import deferred

from library.task.html import analyzeHtml
from library.task.twitter import checkTwitterAccount
from library.task.robots import checkForRobotsTxt, checkForSitemapXml
from library.task.screenshot import grabScreenshot
from library.task.w3c import runW3cValidation

class InitProcessingController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )

		fullUrl = 'http://' + domainUrl

		url = 'http://tldextract.appspot.com/api/extract?url=' + fullUrl
		result = urlfetch.fetch( url )
		apiData = json.loads( result.content )
		baseDomain = apiData['domain']
		
		# Sorted by required time per task 
		deferred.defer( analyzeHtml, domainUrl, fullUrl, channelId )
		deferred.defer( grabScreenshot, fullUrl, channelId )
		deferred.defer( runW3cValidation, fullUrl, channelId )
		deferred.defer( checkForRobotsTxt, fullUrl, channelId )
		deferred.defer( checkForSitemapXml, fullUrl, channelId )
		deferred.defer( checkTwitterAccount, baseDomain, channelId )
		
