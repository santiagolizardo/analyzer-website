
from library.task.base import BaseTask
from library.services.pagerank import getPageRank

import logging

class PageRankTask( BaseTask ):

	def getName( self ):
		return 'googlePageRank'

	def updateView( self, beauty, page_rank ):
		beauty.find( id = 'googlePageRank' ).string.replace_with( self.generate_html_node( page_rank ) )

	def start( self, domain ):
		page_rank = None
		try:
			page_rank  = getPageRank( domain )
		except Exception, ex:
			logging.error( ex )

		self.sendAndSaveReport( domain, page_rank )

	def suggest_actions( self, actions, page_rank, domain ):
		if page_rank < 3:
			actions.append({ 'status': 'bad', 'description': 'Your PageRank is too low. Follow Google webmaster guidelines to improve it.' })
		elif page_rank < 6:
			actions.append({ 'status': 'regular' })
		else:
			actions.append({ 'status': 'good' })

	def generate_html_node( self, page_rank ):
		return 'The domain has a PageRank %d' % page_rank 

