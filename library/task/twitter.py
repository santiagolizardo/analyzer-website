
from google.appengine.api import urlfetch
import json

from library.task.base import BaseTask
		
from library.services.twitter import TwitterService

class TwitterAccountCheckerTask( BaseTask ):

	def getName( self ): return 'twitterAccount'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):

		beauty.find( id = 'twitterAccount' ).string.replace_with( data['twitterAccount'] )

	def start( self, baseUrl ):

		fullUrl = 'http://' + baseUrl

		url = 'http://tldextract.appspot.com/api/extract?url=' + fullUrl
		result = urlfetch.fetch( url )
		apiData = json.loads( result.content )
		baseDomain = apiData['domain']

		twitterService = TwitterService()
		twitterUser = twitterService.get_user( baseDomain )

		content = self.getDefaultData() 
		actions = []

		if twitterUser is not None:
			try:
				twitterUrl = twitterUser['entities']['url']['urls'][0]['expanded_url']
			except KeyError:
				twitterUrl = None
			if twitterUrl is not None and baseUrl in twitterUrl:
				content[ self.getName() ] = 'The Twitter&trade; account <a href="http://twitter.com/%(username)s" rel="nofollow" class="external" target="_blank">@%(username)s</a> is booked and linked to your website. Great!' % { 'username': baseDomain }
				actions.append({ 'status': 'good' })
			else:
				content[ self.getName() ] = 'The Twitter&trade; account <a href="http://twitter.com/%(username)s" rel="nofollow" class="external" target="_blank">@%(username)s</a> is booked but it is not linked to your website.' % { 'username': baseDomain }
				actions.append({ 'status': 'regular', 'description': 'Ideally, you should own the Twitter account matching your domain name' })

		else:
			newTwitterAccountUrl = 'http://twitter.com/signup?user[screen_name]=%s&user[name]=%s' % ( baseDomain, baseUrl )
			content[ self.getName() ] = 'The Twitter&trade; Account @%s is free. <a href="%s" rel="nofollow" class="external" target="_blank">Book it now</a>!' % ( baseDomain, newTwitterAccountUrl ) 
			actions.append({ 'status': 'regular', 'description': 'Register the twitter account %s before somebody else do it' % baseDomain })

		self.sendAndSaveReport( baseUrl, content, actions )

