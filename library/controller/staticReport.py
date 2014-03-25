
from google.appengine.api import memcache

from library.controller.page import StandardPageController

import logging, json, sys, os

from bs4 import BeautifulSoup

from library.model.report import SiteReport
from library.model.report import TaskReport

from library.services.shorturl import createShortUrl

import library.task.manager

from library.sections import reportSections

class StaticReportController( StandardPageController ):

	def get( self, domainUrl ):

		self.is_dev_env = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

		cache_key = 'page_' + domainUrl
		pageHtml = memcache.get( cache_key )
		if self.is_dev_env or pageHtml is None:
			pageHtml = self.generate_static_report( domainUrl )
			memcache.set( key = cache_key, value = pageHtml, time = 86400 )

		self.writeResponse( pageHtml )

	def generate_static_report( self, domainUrl ):
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

		values = {
			'domain': domainUrl,
			'domainLength': len( domainUrl.replace( '.com', '' ) ),
			'sbOptions': reportSections,
			'generatedOnDate': siteReport.creationDate.date().isoformat(),
			'pageTitle': '%(domainUrl)s SEO and SEM performance metrics - EGOsize' % { 'domainUrl': domainUrl.capitalize() },
			'pageDescription': 'Review %(domainUrl)s website report including SEO and SEM KPI and improvements. Learn how to do better at SERP to increase conversions.' % { 'domainUrl': domainUrl },
		}

		self.set_twitter_card( domainUrl )

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
		values['actions'] = actions

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

		return beauty.encode( formatter = None )

	def set_twitter_card( self, domainUrl ):

		screenshotReport = TaskReport.all().filter( 'url =', domainUrl ).filter( 'name = ', 'screenshot' ).get()
		screenshot = json.loads( screenshotReport.messageEncoded )
	
		self.pageMetas.append({ 'name': 'twitter:card', 'content': 'summary' })
		self.pageMetas.append({ 'name': 'twitter:site', 'content': '@egosizereports' })
		self.pageMetas.append({ 'name': 'twitter:title', 'content': '%s SEO and SEM performace metrics' % domainUrl })
		self.pageMetas.append({ 'name': 'twitter:description', 'content': 'Detailed report for %s Website with all major metrics and improvement points' % domainUrl })
		self.pageMetas.append({ 'name': 'twitter:creator', 'content': '@egosizereports' })
		self.pageMetas.append({ 'name': 'twitter:image:src', 'content': screenshot['content']['screenshot'] })

