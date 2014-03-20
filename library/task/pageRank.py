
from library.task.base import BaseTask
		
from library.services.pagerank import getPageRank

class PageRankTask( BaseTask ):

	def getName( self ): return 'googlePageRank'

	def getDefaultData( self ):

		return { self.getName(): 'N/A' }

	def updateView( self, beauty, data ):

		beauty.find( id = 'googlePageRank' ).string.replace_with( data['googlePageRank'] )

	def start( self, baseUrl ):

		pageRank  = getPageRank( baseUrl )

		content = self.getDefaultData() 
		actions = []

		if pageRank is None or '' == pageRank:
			pageRank = '0'

		pageRank = int( pageRank )
		content[ self.getName() ] = 'The domain has a PR%d' % pageRank
		if pageRank < 3:
			actions.append({ 'status': 'bad', 'description': 'Your Page Rank is too low. Try to publish original content more often.' })
		elif pageRank < 6:
			actions.append({ 'status': 'regular' })
		else:
			actions.append({ 'status': 'good' })

		self.sendAndSaveReport( baseUrl, content, actions )

