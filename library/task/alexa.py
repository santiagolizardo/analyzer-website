
from library.task.base import BaseTask

import logging

class AlexaAnalyzerTask( BaseTask ):

	def getName( self ): return 'traffic'

	def getDefaultData( self ):

		return {
			'worldRank': 'N/A',
			'countryRank': 'N/A',
			'loadTimeMs': 0,
			'loadTime': 'N/A'
		}

	def start( self, baseUrl ):

		content = self.getDefaultData()
		actions = []

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
				content['loadTimeMs'] = long( temp )
				content['loadTime'] = temp + ' milliseconds'
				if int( respXml.find( '//{%s}Percentile' % api.NS_PREFIXES['awis'] ).text ) < 50:
					content['loadTime'] += ' (SLOW)'
					actions.append({ 'status': 'regular', 'description': 'You have to speed up your site (e.g. serving smaller images, reducing the number of HTTP requests, compressing CSS and JavaScript files, etc...)' })
				else:
					actions.append({ 'status': 'good' })
					content['loadTime'] += ' (FAST)'


		from google.appengine.api.channel import send_message
		self.sendAndSaveReport( baseUrl, content, actions )

