
from library.task.base import BaseTask		
from library.services.pagerank import getPageRank

import logging
import random
import sys

class PageRankTask( BaseTask ):

	def getName( self ): return 'googlePageRank'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):

		beauty.find( id = 'googlePageRank' ).string.replace_with( data['googlePageRank'] )

	def start( self, baseUrl ):

		content = self.getDefaultData() 
		actions = []

		pageRank = 0

		if self.is_dev_env:
			pageRank = random.randint( 0, 10 )
		else:
			pageRank  = getPageRank( baseUrl )
			if pageRank is None or '' == pageRank:
				pageRank = 0
			try:
				pageRank = int( pageRank )
			except:
				logging.error( sys.exc_info()[0] )

		content[ self.getName() ] = 'The domain has a PR%d' % pageRank
		if pageRank < 3:
			actions.append({ 'status': 'bad', 'description': 'Your Page Rank is too low. Try to publish original content more often.' })
		elif pageRank < 6:
			actions.append({ 'status': 'regular' })
		else:
			actions.append({ 'status': 'good' })

		self.sendAndSaveReport( baseUrl, content, actions )

