
from google.appengine.api import memcache
from google.appengine.api import search

from library.controller.page import StandardPageController

import logging, json, sys, os

from datetime import datetime
import gettext

from bs4 import BeautifulSoup

from library.model.report import SiteReport, SiteRating
from library.model.site import SiteReview
from library.model.report import TaskReport

from library.services.shorturl import createShortUrl

import library.task.manager

import config

from local_config import twitter as twitter_config, addthisPubId

from library.sections import reportSections

class StaticReportController( StandardPageController ):

	def get( self, domainUrl ):
		cache_key = 'page_' + domainUrl
		pageHtml = memcache.get( cache_key )
		if pageHtml is None:
			pageHtml = self.generate_static_report( domainUrl )
			memcache.set( key = cache_key, value = pageHtml, time = 86400 )

		self.writeResponse( pageHtml )

	def generate_static_report( self, domainUrl ):
		siteReport = SiteReport.gql( 'WHERE url = :url', url = domainUrl ).get()
	
		if siteReport is None:
			self.response.set_status( 404 )
			self.response.write( 'Report not found' )
			return

		siteRating = SiteRating.all().filter( 'domain =', domainUrl ).get()
		userRating = None
		if siteRating is not None:
			userRating = siteRating.rating_overall

		self.addJavaScript( 'https://www.google.com/jsapi' )
		self.addJavaScript( '/scripts/staticReport.js' )

		baseUrl = 'http://' + self.current_instance['url'] 
			
		values = {
			'baseUrl': baseUrl,
			'domain': domainUrl,
			'userRating': userRating,
			'domainLength': len( domainUrl.replace( '.com', '' ) ),
			'sbOptions': reportSections,
			'generatedDate': siteReport.creationDate.date().isoformat(),
			'generatedDateTime': siteReport.creationDate.date().isoformat(),
			'pageTitle': '%(domainUrl)s SEO and SEM performance metrics - %(siteName)s' % { 'domainUrl': domainUrl.capitalize(), 'siteName': self.current_instance['name'] },
			'pageDescription': 'Review %(domainUrl)s website report including SEO and SEM KPI and improvements. Learn how to do better at SERP to increase conversions.' % { 'domainUrl': domainUrl },
			'addthisPubId': addthisPubId
		}

		self.set_twitter_card( domainUrl )

		tasks = library.task.manager.findAll()

		all_data = {}
		actions = []

		for task in tasks:
			subreport = task.getSavedReport( domainUrl )
			task.suggest_actions( actions, subreport, domainUrl )
			
		site_reviews = SiteReview.all().filter( 'domain = ', domainUrl ).fetch( limit = 5 )
		values['user_reviews'] = site_reviews

		values['shortUrl'] = self.request.url
		if config.debug_active is False:
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
			beauty.find( 'div', 'progress-bar progress-bar-success' )['style'] = 'width: %d%%;' % ( ( statuses['good'] * 100 ) / totalStatuses )
			beauty.find( 'div', 'progress-bar progress-bar-warning' )['style'] = 'width: %d%%;' % ( ( statuses['regular'] * 100 ) / totalStatuses )
			beauty.find( 'div', 'progress-bar progress-bar-danger' )['style'] = 'width: %d%%;' % ( ( statuses['bad'] * 100 ) / totalStatuses )

		for task in tasks:
			subreport = task.getSavedReport( domainUrl )
			if dict == type( subreport ) and 'content' in subreport:
				data.update( subreport['content'] )

			all_data[ task.getName() ] = subreport

			task.updateView( beauty, subreport )

		try:
			report_id = str( siteReport.key().id() )
			index = search.Index( name = 'domains' )
			doc = index.get( report_id )
			if doc is None:
				fields = [
					search.TextField( name = 'url', value = domainUrl ), 
					#search.TextField( name = 'title', value = all_data['pageTitle'] ), 
					#search.TextField( name = 'description', value = all_data['pageDescription'] ),
					search.DateField( name = 'generation_date', value = siteReport.creationDate.date() ),
				]
				if 'pageKeywords' in all_data:
					fields.append( search.TextField( name = 'keywords', value = ','.join( all_data['pageKeywords'] ) ) )

				doc = search.Document( doc_id = report_id, fields = fields )
				index.put( doc )
		except search.Error:
			logging.exception('Put failed')

		return beauty.encode( formatter = None )

	def set_twitter_card( self, domainUrl ):	
		self.pageMetas.append({ 'name': 'twitter:card', 'content': 'summary' })
		self.pageMetas.append({ 'name': 'twitter:site', 'content': '@' + twitter_config['username'] })
		self.pageMetas.append({ 'name': 'twitter:title', 'content': '%s SEO and SEM performace metrics' % domainUrl })
		self.pageMetas.append({ 'name': 'twitter:description', 'content': 'Detailed report for %s Website with all major metrics and improvement points' % domainUrl })
		self.pageMetas.append({ 'name': 'twitter:creator', 'content': '@' + twitter_config['username'] })

		screenshotReport = TaskReport.all().filter( 'url =', domainUrl ).filter( 'name = ', 'screenshot' ).get()
		if screenshotReport:
		    screenshot = json.loads( screenshotReport.messageEncoded )
		    if screenshot is not None:
			    self.pageMetas.append({ 'name': 'twitter:image:src', 'content': screenshot })

