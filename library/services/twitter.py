
import sys

import tweepy, logging

from local_config import twitter as twitter_config

class TwitterService:

	def authenticate( self ):
		auth = tweepy.OAuthHandler( twitter_config['consumer_key'], twitter_config['consumer_secret'] )
		auth.set_access_token( twitter_config['access_token'], twitter_config['access_token_secret'] )
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

