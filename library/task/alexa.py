
from library.task.base import BaseTask

import logging

class AlexaAnalyzerTask( BaseTask ):

	def getName( self ): return 'traffic'

	def start( self, baseUrl ):

		content = {
			'worldRank': 'N/A',
			'countryRank': 'N/A',
		}

		queryUrl = baseUrl.replace( 'http://', '' )

		from library.awis import AwisApi
		api = AwisApi( 'AKIAJDGJO3ACZ7KIGHCA', 'dIc3teMI2OoSw0W7z9EXgP9cQnvUlja8uSQN2MBT' )
		respXml = api.url_info( queryUrl, 'RelatedLinks', 'Categories', 'Rank', 'RankByCountry', 'UsageStats', 'ContactInfo', 'Speed', 'Language', 'Keywords', 'OwnedDomains', 'LinksInCount', 'SiteData' )
		respStatus = respXml.find( '//{%s}StatusCode' % api.NS_PREFIXES['alexa'] ).text
		if 'Success' == respStatus:
			from lxml import etree
			content['worldRank'] = respXml.find( '//{%s}Rank' % api.NS_PREFIXES['awis'] ).text
			if content['worldRank'] is None:
				content['worldRank'] = 'Unknown'

			temp = respXml.find( '//{%s}MedianLoadTime' % api.NS_PREFIXES['awis'] ).text
			if temp is not None:
				content['loadTime'] = temp + ' seconds'
				if int( respXml.find( '//{%s}Percentile' % api.NS_PREFIXES['awis'] ).text ) < 50:
					content['loadTime'] += ' (SLOW)'
				else:
					content['loadTime'] += ' (FAST)'

		self.saveReport( baseUrl, content )
		self.sendMessage( content )

