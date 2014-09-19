
import logging

from library.task.base import BaseTask
		
from library.services.twitter import TwitterService
from library.services.domain import tokenize_url
from library.services.stats import increase_domain_tld_count

class TwitterAccountCheckerTask( BaseTask ):

	def getName( self ):
		return 'twitterAccount'

	def updateView( self, beauty, data ):
		beauty.find( id = 'twitterAccount' ).string.replace_with( self.generate_html_node( data ) )

	def start( self, baseUrl ):
		content = {}
		content['baseUrl'] = baseUrl
		content['twitterUser'] = None
		try:
			apiData = tokenize_url( baseUrl )
			baseDomain = apiData['domain']
			try:
				increase_domain_tld_count( apiData['tld'] )
			except Exception, ex:
				logging.error( 'Error saving tld stats' )
				logging.error( ex )

			content['baseDomain'] = baseDomain

			try:
				twitterService = TwitterService()
				twitterUser = twitterService.get_user( baseDomain )
				content['twitterUser'] = twitterUser

				if twitterUser is not None:
					try:
						twitterUrl = twitterUser['entities']['url']['urls'][0]['expanded_url']
						content['twitterUrl'] = twitterUrl
					except Exception, ex:
						logging.warning( 'twitter user @%s doesnt have a profile url' % baseDomain )
						content['twitterUrl'] = None
			except Exception, ex:
				logging.error( ex )
				content['twitterUser'] = None
		except Exception, ex:
			logging.error( ex )

		self.sendAndSaveReport( baseUrl, content )

	def suggest_actions( self, actions, data, domain ):
		if data['twitterUser'] is not None:
			if data['twitterUrl'] is not None and domain in data['twitterUrl']:
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'regular', 'description': 'Ideally, you should own the Twitter account matching your domain name' })
		else:
			actions.append({ 'status': 'regular', 'description': 'Register the twitter account %s before somebody else do it' % domain })

	def generate_html_node( self, data ):
		content = {}
		baseDomain = data['baseDomain']
		baseUrl = data['baseUrl']
		if data['twitterUser'] is not None:
			if data['twitterUrl'] is not None and baseUrl in data['twitterUrl']:
				content = 'The Twitter&trade; account <a href="http://twitter.com/%(username)s" rel="nofollow" class="external" target="_blank">@%(username)s</a> is booked and linked to your website. Great!' % { 'username': baseDomain }
			else:
				content = 'The Twitter&trade; account <a href="http://twitter.com/%(username)s" rel="nofollow" class="external" target="_blank">@%(username)s</a> is booked but it is not linked to your website.' % { 'username': baseDomain }
		else:
			baseUrl = 'xxx'
			newTwitterAccountUrl = 'http://twitter.com/signup?user[screen_name]=%s&user[name]=%s' % ( baseDomain, baseUrl )
			content = 'The Twitter&trade; Account @%s is free. <a href="%s" rel="nofollow" class="external" target="_blank">Book it now</a>!' % ( baseDomain, newTwitterAccountUrl ) 
		return content

