
import tweepy, logging

class TwitterService:

	consumer_key = '2t38koHXdwRZC8YVydtEyA'
	consumer_secret = 'YJhUd1tAmVTI3gZs3mGxZ8mtoRqDJYt98LKQJ5SetU'
	access_token = '2384273864-bKlP0OJrzoBAycrM4DFOFEziBSnmaRdtynV09vR'
	access_token_secret = 'XT8htB5RYtTAu0eP60yLbohgRx7YeoHfCSQz9ij9oQdDG'

	def authenticate( self ):
		auth = tweepy.OAuthHandler( self.consumer_key, self.consumer_secret )
		auth.set_access_token( self.access_token, self.access_token_secret )
		return auth

	def update_status( self, text ):
		try:
			auth = self.authenticate()
			api = tweepy.API( auth )
			api.update_status( text )
		except tweepy.TweepError, e:
			logging.error( e.response.status )

	def get_user( self, username ):
		try:
			auth = self.authenticate()
			api = tweepy.API( auth, parser=tweepy.parsers.JSONParser() )
			return api.get_user( username )
		except tweepy.TweepError, e:
			logging.error( e.response.status )
			return None

