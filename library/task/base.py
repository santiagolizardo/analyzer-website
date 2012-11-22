
import json, logging

from google.appengine.api.channel import send_message

from library.model.report import TaskReport

class BaseTask( object ):

	def __init__( self, channelId ):

		self.channelId = channelId

	def getName( self ):

		raise Exception( 'Method not implemented' )

	def saveReport( self, url, content ):

		niceUrl = url.replace( 'http://', '' )
		jsonContent = json.dumps( content )
		logging.info( jsonContent )
		taskReport = TaskReport( name = self.getName(), url = niceUrl, content = jsonContent )
		taskReport.put()

	def sendMessage( self, content ):
	
		message = {
			'type': self.getName(),
			'body': content
		}
		send_message( self.channelId, json.dumps( message ) )


