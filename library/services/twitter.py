
import sys

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
		auth = self.authenticate()
		api = tweepy.API( auth )
		api.update_status( text )
		
	def get_user( self, username ):
		auth = self.authenticate()
		api = tweepy.API( auth, parser=tweepy.parsers.JSONParser() )
		return api.get_user( username )
		
if __name__ == '__main__':
	import sys
	sys.path.append( '../../externals/tweepy' )
	domain = sys.argv[1] if len( sys.argv ) > 1 else 'google'
	import pprint
	pprint.pprint(TwitterService().get_user(domain))

