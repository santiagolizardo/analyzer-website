
from google.appengine.api import urlfetch

from library.task.base import BaseTask

class TwitterAccountCheckerTask( BaseTask ):

	def getName( self ): return 'twitterAccount'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def start( self, baseDomain ):

		url = 'http://twitter.com/' + baseDomain
		result = urlfetch.fetch( url )

		content = self.getDefaultData() 
		actions = []

		if result.status_code == 200:
			content[ self.getName() ] = 'The twitter&trade; account @%s is booked but it is not linked to your website!' % baseDomain
			actions.append({ 'status': 'regular', 'description': 'Ideally, you should own the Twitter account matching your domain name' })

		elif result.status_code == 404:
			newTwitterAccountUrl = 'http://twitter.com/signup?user[name]=' + baseDomain
			content[ self.getName() ] = 'The Twitter&trade; Account @%s is free. <a href="%s" rel="nofollow" target="_blank">Book it now</a>!' % ( baseDomain, newTwitterAccountUrl ) 
			actions.append({ 'status': 'regular', 'description': 'Register the twitter account %s before somebody else do it' % baseDomain })

		self.sendAndSaveReport( baseDomain, content, actions )

