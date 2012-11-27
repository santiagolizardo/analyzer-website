
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

from google.appengine.ext import deferred

from library.model.report import SiteReport

from library.task.html import HtmlAnalyzerTask 
from library.task.domain import DomainAnalyzerTask 
from library.task.twitter import TwitterAccountCheckerTask 
from library.task.robots import RobotsTxtCheckerTask, SitemapXmlCheckerTask 
from library.task.screenshot import ScreenshotGrabberTask 
from library.task.w3c import W3cValidatorTask
from library.task.alexa import AlexaAnalyzerTask
from library.task.social import FacebookCounterTask

class CalculateScoreController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )
		
		htmlAnalyzer = HtmlAnalyzerTask()
		domainAnalyzer = DomainAnalyzerTask()
		screenshotGrabber = ScreenshotGrabberTask()
		w3cValidator = W3cValidatorTask()
		robotsChecker = RobotsTxtCheckerTask()
		sitemapChecker = SitemapXmlCheckerTask()
		twitterChecker = TwitterAccountCheckerTask()
		alexaAnalyzer = AlexaAnalyzerTask()

		tasks = ( htmlAnalyzer, domainAnalyzer, screenshotGrabber, w3cValidator, robotsChecker, sitemapChecker, twitterChecker, alexaAnalyzer, FacebookCounterTask() )
	
		data = {}
		actions = []

		for task in tasks:
			report = task.getSavedReport( domainUrl )
			if 'actions' in report:
				actions.extend( report['actions'] )

			defaultData = task.getDefaultData()
			if 'content' in report:
				if type( report['content'] ) == dict:
					defaultData.update( report['content'] )
				else:
					defaultData[ task.getName() ] = report['content']
			data.update( defaultData )

		score = 100
		totalVariables = len( actions ) # eg 12
		scorePerVariable = 100 / totalVariables # eg: 8.33
		
		for action in actions:
			if action['status'] == 'good':
				pass
			elif action['status'] == 'regular':
				score -= scorePerVariable/2
			elif action['status'] == 'bad':
				score -= scorePerVariable
		
		siteReport = SiteReport()
		siteReport.score = score
		siteReport.name = data['pageTitle']
		siteReport.description = data['pageDescription']
		siteReport.url = domainUrl
		siteReport.put()
		
		message = {
			'name': 'score',
			'content': str( score ) + '/100',
			'actions': [],
		}
		messageEncoded = json.dumps( message )
				
		send_message( channelId, messageEncoded )

