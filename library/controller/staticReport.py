
from library.controller.page import PageController

import logging, json

from datetime import date

from library.model.report import TaskReport

from bs4 import BeautifulSoup, NavigableString

class StaticReportController( PageController ):

	def get( self, domainUrl ):
		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		self.addStyleSheet( '/styles/allmedia.css' )

		sbOptions = (
			{ 'id': 'priority-actions', 'label': 'Priority actions' },
			{ 'id': 'domain', 'label': 'Domain' },
			{ 'id': 'visitors', 'label': 'Visitors' },
			{ 'id': 'social-monitoring', 'label': 'Social monitoring' },
			{ 'id': 'content-optimization', 'label': 'Content optimization' },
			{ 'id': 'usability', 'label': 'Usability' },
			{ 'id': 'mobile', 'label': 'Mobile' },
			{ 'id': 'seo-basics', 'label': 'SEO basics' },
			{ 'id': 'seo-keywords', 'label': 'SEO keywords' },
			{ 'id': 'seo-authority', 'label': 'SEO authority' },
			{ 'id': 'seo-backlinks', 'label': 'SEO backlinks' },
			{ 'id': 'security', 'label': 'Security' },
			{ 'id': 'technologies', 'label': 'Technologies' },
		)

		values = {
			'domain': domainUrl,
			'appUrl': self.app.config.get( 'url' ),
			'domainLength': len( domainUrl.replace( '.com', '' ) ),
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
			'sbOptions': sbOptions,
			'generatedOnDate': date.today().isoformat(),
			'pageTitle': '%(domainUrl)s | Domain insights for %(domainUrl)s by DomainGrasp.com' % { 'domainUrl': domainUrl },
			'pageDescription': 'Check %(domainUrl)s metrics on SEO, social and other relevant aspects thanks to DomainGrasp'
		}

		html = self.renderTemplate( 'staticReport.html', values )

		beauty = BeautifulSoup( html )

		actions = []

		taskReport = TaskReport.gql( "WHERE name = 'htmlBody' AND url = :1", domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )
			actions.extend( data['actions'] )
			data = data['content']

			beauty.find( id = 'pageTitle' ).replace_with( NavigableString( data['pageTitle'] ) )
			beauty.find( id = 'pageDescription' ).replace_with( NavigableString( data['pageDescription'] if data['pageDescription'] else 'Unknown' ) )
			beauty.find( id = 'docType' ).replace_with( NavigableString( data['docType'] ) )
			beauty.find( id = 'images' ).replace_with( NavigableString( data['images'] ) )
			beauty.find( id = 'headings' ).replace_with( NavigableString( data['headings'] ) )
			beauty.find( id = 'softwareStack' ).replace_with( NavigableString( data['softwareStack'] ) )
			beauty.find( id = 'googleAnalytics' ).replace_with( NavigableString( 'Yes' if data['googleAnalytics'] else 'No' ) )
			beauty.find( id = 'pageSize' ).replace_with( NavigableString( str( data['pageSize'] ) ) )
			beauty.find( id = 'serverIp' ).replace_with( NavigableString( data['serverIp'] ) )

		taskReport = TaskReport.gql( "WHERE name = 'screenshot' AND url = :1", domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )
			actions.extend( data['actions'] )
			data = data['content']
			beauty.find( id = 'screenshot' )['src'] = data

		taskReport = TaskReport.gql( "WHERE name = 'traffic' AND url = :1", domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )
			actions.extend( data['actions'] )
			data = data['content']
			beauty.find( id = 'worldRank' ).replace_with( NavigableString( data['worldRank'] ) )
			beauty.find( id = 'loadTime' ).replace_with( NavigableString( data['loadTime'] ) )

		taskReport = TaskReport.gql( "WHERE name = 'sitemapXml' AND url = :1", domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )
			actions.extend( data['actions'] )
			data = data['content']
			beauty.find( id = 'sitemapXml' ).replace_with( NavigableString( data ) )

		taskReport = TaskReport.gql( "WHERE name = 'robotsTxt' AND url = :1", domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )
			actions.extend( data['actions'] )
			data = data['content']

			beauty.find( id = 'robotsTxt' ).replace_with( NavigableString( data ) )

		taskReport = TaskReport.gql( "WHERE name = 'w3cValidation' AND url = :1", domainUrl ).get()
		if taskReport is not None:
			data = json.loads( taskReport.messageEncoded )
			actions.extend( data['actions'] )
			data = data['content']

			beauty.find( id = 'w3cValidity' ).replace_with( NavigableString( data ) )

		statuses = {
			'good': 0,
			'regular': 0,
			'bad': 0,
		}
		totalStatuses = 0

		for action in actions:
			statuses[ action['status'] ] = statuses[ action['status'] ] + 1
			totalStatuses = totalStatuses + 1

		beauty.find( id = 'goodStatuses' ).replace_with( NavigableString( str( statuses['good'] ) ) )
		beauty.find( id = 'regularStatuses' ).replace_with( NavigableString( str( statuses['regular'] ) ) )
		beauty.find( id = 'badStatuses' ).replace_with( NavigableString( str( statuses['bad'] ) ) )

		beauty.find( 'div', 'bar bar-success' )['style'] = 'width: %d%%;' % ( ( statuses['good'] * 100 ) / totalStatuses )
		beauty.find( 'div', 'bar bar-warning' )['style'] = 'width: %d%%;' % ( ( statuses['regular'] * 100 ) / totalStatuses )
		beauty.find( 'div', 'bar bar-danger' )['style'] = 'width: %d%%;' % ( ( statuses['bad'] * 100 ) / totalStatuses )

		self.writeResponse( beauty.encode( formatter = None ) )


