
import sys
sys.path.append( 'vendor' )
sys.path.append( 'externals/tweepy' )
sys.path.append( 'externals/awis' )

import json, os, logging

from google.appengine.api.channel import send_message

from library.model.report import TaskReport

class BaseTask( object ):

	def __init__( self, channelId  = None ):
		self.channelId = channelId

		self.is_dev_env = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

	def fix_sys_path( self ):
		sys.path.append( 'vendor' )
		sys.path.append( 'externals/tweepy' )
		sys.path.append( 'externals/awis' )

	def setChannelId( self, channelId ):
		self.channelId = channelId

	def getName( self ):
		raise Exception( 'Method not implemented' )

	def getDefaultData( self ):
		return None

	def updateView( self, beauty, data ):
		pass

	def sendAndSaveReport( self, url, content ):
		if self.channelId is None:
			logging.error( 'channelId is None for task: ' + self.getName() )
			return

		actions = []
		self.suggest_actions( actions, content, url )

		message = {
			'name': self.getName(),
			'content': self.generate_html_node( content ),
			'actions': actions,
		}
		messageEncoded = json.dumps( message )

		# Send
		send_message( self.channelId, messageEncoded )

		# Save
		niceUrl = url.replace( 'http://', '' )

		taskReport = TaskReport( name = self.getName(), url = niceUrl, messageEncoded = json.dumps( content ) )
		taskReport.put()

	def suggest_actions( self, actions, data, domain = None ):
		pass

	def generate_html_node( self, data ):
		return {}
		return None

	def getSavedReport( self, domainUrl ):
		data = self.getDefaultData()

		taskReport = TaskReport.gql( "WHERE name = :1 AND url = :2", self.getName(), domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )

		return data

