
import json

from google.appengine.api.channel import send_message

class BaseTask( object ):

	def __init__( self, channelId ):

		self.channelId = channelId

	def getName( self ):

		raise Exception( 'Method not implemented' )

	def saveReport( self, url, content ):

		taskReport = TaskReport( self.getName(), url, json.dumps( content ) )
		taskReport.put()

	def sendMessage( self, content ):

		send_message( self.channelId, json.dumps( content ) )


