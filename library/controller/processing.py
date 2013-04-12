
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import create_channel

from google.appengine.ext import deferred

from library.task.html import HtmlAnalyzerTask 
from library.task.domain import DomainAnalyzerTask 
from library.task.twitter import TwitterAccountCheckerTask 
from library.task.robots import RobotsTxtCheckerTask, SitemapXmlCheckerTask 
from library.task.screenshot import ScreenshotGrabberTask 
from library.task.w3c import W3cValidatorTask
from library.task.alexa import AlexaAnalyzerTask
from library.task.social import FacebookCounterTask
from library.task.search import SearchTask

import twitter

def tweet( domain ):
	api = twitter.Api(
		consumer_key = 'wdRZHTPeaz8rpCsIW4Kw',
		consumer_secret = 'pPb3hsR6ugXLJrTL6SDSeP12D0AGTcT2H2hylaNqGg',
		access_token_key = '957283916-yTeTCwS2IpTwiLjTshf2gaOGMC2kuH3R7xBXmJy9',
		access_token_secret = '5Ch8cgaB7OmOE5l9XDNILLCK67xiNlM5JSYiLG1kDk',
		cache = None
	)

	api.VerifyCredentials()

	message = 'The domain %s has been reviewed on SEO. Check the report here: http://report.domaingrasp.com/%s' % ( domain, domain )
	status = api.PostUpdate( message )

class InitProcessingController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )

		fullUrl = 'http://' + domainUrl

		url = 'http://tldextract.appspot.com/api/extract?url=' + fullUrl
		result = urlfetch.fetch( url )
		apiData = json.loads( result.content )
		baseDomain = apiData['domain']

		deferred.defer( tweet, domainUrl )
		
		# Sorted by required time per task 
		htmlAnalyzer = HtmlAnalyzerTask( channelId )
		deferred.defer( htmlAnalyzer.start, domainUrl, fullUrl )

		domainAnalyzer = DomainAnalyzerTask( channelId )
		deferred.defer( domainAnalyzer.start, fullUrl )

		screenshotGrabber = ScreenshotGrabberTask( channelId )
		deferred.defer( screenshotGrabber.start, fullUrl )

		w3cValidator = W3cValidatorTask( channelId )
		deferred.defer( w3cValidator.start, fullUrl )

		robotsChecker = RobotsTxtCheckerTask( channelId )
		deferred.defer( robotsChecker.start, fullUrl )

		sitemapChecker = SitemapXmlCheckerTask( channelId )
		deferred.defer( sitemapChecker.start, fullUrl )

		twitterChecker = TwitterAccountCheckerTask( channelId )
		deferred.defer( twitterChecker.start, baseDomain )
	
		alexaAnalyzer = AlexaAnalyzerTask( channelId )
		deferred.defer( alexaAnalyzer.start, fullUrl )

		fbCounter = FacebookCounterTask( channelId )
		deferred.defer( fbCounter.start, domainUrl )
	
		searchTask = SearchTask( channelId )
		deferred.defer( searchTask.start, domainUrl )

