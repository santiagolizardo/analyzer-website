
import webapp2, logging, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import create_channel

from google.appengine.ext import deferred

import library.task.manager

class InitProcessingController( webapp2.RequestHandler ):

	def get( self ):
		domainUrl = self.request.get( 'domainUrl' )
		channelId = self.request.cookies.get( 'channelId' )

		tasks = library.task.manager.findAll()
		
		for task in tasks:
			task.setChannelId( channelId )
			deferred.defer( task.start, domainUrl, _name = task.getName() )

