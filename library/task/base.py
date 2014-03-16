
import json, logging

from google.appengine.api.channel import send_message

from library.model.report import TaskReport

class BaseTask( object ):

	def __init__( self, channelId  = None ):

		self.channelId = channelId

	def setChannelId( self, channelId ):

		self.channelId = channelId

	def getName( self ):

		raise Exception( 'Method not implemented' )

	def getDefaultData( self ):
		
		raise Exception( 'Method not implemented' )

	def updateView( self, beauty, data ):

		pass

	def sendAndSaveReport( self, url, content, actions = [] ):

		message = {
			'name': self.getName(),
			'content': content,
			'actions': actions
		}
		messageEncoded = json.dumps( message )

		# Send
		send_message( self.channelId, messageEncoded )

		# Save
		niceUrl = url.replace( 'http://', '' )

		taskReport = TaskReport( name = self.getName(), url = niceUrl, messageEncoded = messageEncoded )
		taskReport.put()

	def getSavedReport( self, domainUrl ):
		data = self.getDefaultData()

		taskReport = TaskReport.gql( "WHERE name = :1 AND url = :2", self.getName(), domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )

		return data

