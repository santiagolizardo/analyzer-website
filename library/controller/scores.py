
import webapp2, logging, json, os

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

from google.appengine.ext import deferred

from library.model.report import SiteReport

from library.services.twitter import TwitterService

import library.task.manager

def send_twitter_update( domainUrl ):
	message = '%(domainUrl)s website SEO/SEM/WPO metrics report available at http://report.egosize.com/%(domainUrl)s, get yours for free!' % { 'domainUrl': domainUrl }

	twitterService = TwitterService()
	twitterService.update_status( message )

class CalculateScoreController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )
		
		tasks = library.task.manager.findAll()
	
		data = {
			'pageTitle': None,
			'pageDescription': None,
		}
		actions = []

		for task in tasks:
			report = task.getSavedReport( domainUrl )
			task.suggest_actions( actions, report, domainUrl )

			html_node = task.generate_html_node( report )
			if html_node is not None:
				data[ task.getName() ] = html_node 

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
				
		memcache.delete( 'page-index' )

		send_message( channelId, messageEncoded )

