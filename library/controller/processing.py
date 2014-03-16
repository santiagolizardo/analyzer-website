
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import create_channel

from google.appengine.ext import deferred

import library.task.manager

import tweepy

def tweet( domain ):
	consumer_key = '2t38koHXdwRZC8YVydtEyA'
	consumer_secret = 'YJhUd1tAmVTI3gZs3mGxZ8mtoRqDJYt98LKQJ5SetU'
	access_token = '2384273864-bKlP0OJrzoBAycrM4DFOFEziBSnmaRdtynV09vR'
	access_token_secret = 'XT8htB5RYtTAu0eP60yLbohgRx7YeoHfCSQz9ij9oQdDG'

	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)

		message = '%s website SEO/SEM/WPO metrics report available at http://report.egosize.com/%s, get yours for free!' % ( domain, domain )
		api.update_status( message )
	except TweepError:
		pass	

class InitProcessingController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )

		#deferred.defer( tweet, domainUrl )

		tasks = library.task.manager.findAll()
		
		# Sorted by required time per task 
		for task in tasks:
			task.setChannelId( channelId )
			deferred.defer( task.start, domainUrl )

