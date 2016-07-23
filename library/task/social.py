
import sys, logging, json

import urllib
from library.task.base import BaseTask

from google.appengine.api import urlfetch

class FacebookCounterTask( BaseTask ):

	def getName(self):
		return 'facebook'

	def updateView( self, beauty, data ):
	    if data:
		beauty.find( id = 'facebookComments' ).string.replace_with( ( str( data['facebookComments'] ) ) )
		beauty.find( id = 'facebookLikes' ).string.replace_with( ( str( data['facebookLikes'] ) ) )
		beauty.find( id = 'facebookShares' ).string.replace_with( ( str( data['facebookShares'] ) ) )
        
	def start( self, domainUrl ):
		content = None 
		
		params = {
			'query': 'select total_count,like_count,comment_count,share_count,click_count from link_stat where url=\'%s\'' % domainUrl,
			'format': 'json'
		}
		url = 'https://api.facebook.com/method/fql.query?' + urllib.urlencode(params)

		try:
			result = urlfetch.fetch( url )
			if result.status_code == 200:
				data = json.loads( result.content )[0]
				content['facebookLikes'] = data['like_count']
				content['facebookComments'] = data['comment_count']
				content['facebookShares'] = data['share_count']
		except Exception, ex:
			logging.error( ex )
		
		self.sendAndSaveReport( domainUrl, content )

	def suggest_actions( self, actions, data, domain ):
	        if data is None:
	            logging.warning('data is None')
                    return

		totalCount = sum( data.values() )

		if totalCount < 10:
		    actions.append({ 'status': 'bad', 'description': 'Your social activity is almost null. You have to be more social on Facebook' })
		elif totalCount < 100:
		    actions.append({ 'status': 'regular', 'description': 'Your social activity on Facebook is good, but try to engage more users' })
		else:
		    actions.append({ 'status': 'good' })

	def generate_html_node( self, data ):
		return data

