
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import create_channel

from google.appengine.ext import deferred

from library.model.domain import Domain

from library.task.html import HtmlAnalyzerTask 
from library.task.domain import DomainAnalyzerTask 
from library.task.twitter import TwitterAccountCheckerTask 
from library.task.robots import RobotsTxtCheckerTask, SitemapXmlCheckerTask 
from library.task.screenshot import ScreenshotGrabberTask 
from library.task.w3c import W3cValidatorTask
from library.task.alexa import AlexaAnalyzerTask
from library.task.social import FacebookCounterTask

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
	
		domain = Domain.gql( 'WHERE url = :url', url = domainUrl ).get()
		if domain is None:
			domain = Domain( url = domainUrl )
			domain.put()

