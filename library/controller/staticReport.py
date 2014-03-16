
from library.controller.page import StandardPageController

import logging, json, sys, os

from datetime import date

from bs4 import BeautifulSoup

from library.model.report import SiteReport

from library.services import createShortUrl

import library.task.manager

class StaticReportController( StandardPageController ):

	def get( self, domainUrl ):

		siteReport = SiteReport.gql( 'WHERE url = :url', url = domainUrl ).get()
	
		if siteReport is None:
			self.response.set_status( 404 )
			self.response.write( 'Report not found' )
			return

		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addJavaScript( 'https://www.google.com/jsapi' )
		self.addJavaScript( '/scripts/staticReport.js' )
		
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
			'domainLength': len( domainUrl.replace( '.com', '' ) ),
			'sbOptions': sbOptions,
			'generatedOnDate': date.today().isoformat(),
			'pageTitle': '%(domainUrl)s SEO and SEM performance metrics - EGOsize' % { 'domainUrl': domainUrl.capitalize() },
			'pageDescription': 'Review %(domainUrl)s website report including SEO and SEM KPI and improvements. Learn how to do better at SERP and increase conversions.' % { 'domainUrl': domainUrl },
		}

		tasks = library.task.manager.findAll()

		data = {}
		actions = []

		for task in tasks:
			subreport = task.getSavedReport( domainUrl )
			if 'actions' in subreport:
				actions.extend( subreport['actions'] )
			
		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

		values['shortUrl'] = self.request.url
		if debugActive is False:
			try:
				values['shortUrl'] = createShortUrl( self.request.url )
			except:
				logging.error( sys.exc_info()[1] )
		
		statuses = {
			'good': 0,
			'regular': 0,
			'bad': 0,
		}

		for action in actions:
			statuses[ action['status'] ] = statuses[ action['status'] ] + 1
		totalStatuses = sum( statuses.values() )
		
		values['loadTimeMs'] = 0
		html = self.renderTemplate( 'staticReport.html', values )
		beauty = BeautifulSoup( html )
		beauty.find( id = 'score' ).contents[0].replace_with( str( siteReport.score ) )

		beauty.find( id = 'goodStatuses' ).string.replace_with( str( statuses['good'] ) )
		beauty.find( id = 'regularStatuses' ).string.replace_with( str( statuses['regular'] ) )
		beauty.find( id = 'badStatuses' ).string.replace_with( str( statuses['bad'] ) )

		if totalStatuses > 0:
			beauty.find( 'div', 'bar bar-success' )['style'] = 'width: %d%%;' % ( ( statuses['good'] * 100 ) / totalStatuses )
			beauty.find( 'div', 'bar bar-warning' )['style'] = 'width: %d%%;' % ( ( statuses['regular'] * 100 ) / totalStatuses )
			beauty.find( 'div', 'bar bar-danger' )['style'] = 'width: %d%%;' % ( ( statuses['bad'] * 100 ) / totalStatuses )

		for task in tasks:
			subreport = task.getSavedReport( domainUrl )
			data = task.getDefaultData()
			if 'content' in subreport:
				data.update( subreport['content'] )

			task.updateView( beauty, data )

		self.writeResponse( beauty.encode( formatter = None ) )

