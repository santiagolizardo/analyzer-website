
from google.appengine.api import urlfetch

from library.task.base import BaseTask

class TwitterAccountCheckerTask( BaseTask ):

	def start( self, baseDomain ):

	    url = 'http://twitter.com/' + baseDomain
	    result = urlfetch.fetch( url )

	    content = 'N/A'
	    if result.status_code == 200:
		content = 'The twitter&trade; account @%s is booked but it is not linked to your website!' % baseDomain
	    elif result.status_code == 404:
		newTwitterAccountUrl = 'http://twitter.com/signup?user[name]=' + baseDomain
		content = 'The Twitter&trade; Account @%s is free. <a href="%s" rel="nofollow" target="_blank">Book it now</a>!' % ( baseDomain, newTwitterAccountUrl ) 
		self.saveReport( baseDomain, content )
		self.sendMessage( content )

