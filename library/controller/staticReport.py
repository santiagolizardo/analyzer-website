
from library.controller.page import StandardPageController

import logging, json, sys, os

from datetime import date

from bs4 import BeautifulSoup, NavigableString

from library.task.html import HtmlAnalyzerTask 
from library.task.domain import DomainAnalyzerTask 
from library.task.twitter import TwitterAccountCheckerTask 
from library.task.robots import RobotsTxtCheckerTask, SitemapXmlCheckerTask 
from library.task.screenshot import ScreenshotGrabberTask 
from library.task.w3c import W3cValidatorTask
from library.task.alexa import AlexaAnalyzerTask
from library.task.social import FacebookCounterTask
from library.task.search import SearchTask 

from library.model.report import SiteReport

#short 
from google.appengine.api import app_identity
from google.appengine.api import urlfetch

def create_short_url(long_url):
    scope = "https://www.googleapis.com/auth/urlshortener"
    authorization_token, _ = app_identity.get_access_token(scope)
    logging.info("Using token %s to represent identity %s",
                 authorization_token, app_identity.get_service_account_name())
    payload = json.dumps({"longUrl": long_url})
    response = urlfetch.fetch(
            "https://www.googleapis.com/urlshortener/v1/url?pp=1",
            method=urlfetch.POST,
            payload=payload,
            headers = {"Content-Type": "application/json",
                       "Authorization": "OAuth " + authorization_token})
    if response.status_code == 200:
        result = json.loads(response.content)
        return result["id"]
    raise Exception("Call failed. Status code %s. Body %s",
                    response.status_code, response.content)

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
			'pageTitle': '%(domainUrl)s | Domain insights for %(domainUrl)s by DomainGrasp.com' % { 'domainUrl': domainUrl },
			'pageDescription': 'Check %(domainUrl)s metrics on SEO, social and other relevant aspects thanks to DomainGrasp',
		}

		htmlAnalyzer = HtmlAnalyzerTask()
		domainAnalyzer = DomainAnalyzerTask()
		screenshotGrabber = ScreenshotGrabberTask()
		w3cValidator = W3cValidatorTask()
		robotsChecker = RobotsTxtCheckerTask()
		sitemapChecker = SitemapXmlCheckerTask()
		twitterChecker = TwitterAccountCheckerTask()
		alexaAnalyzer = AlexaAnalyzerTask()

		tasks = (
			htmlAnalyzer,
			domainAnalyzer,
			screenshotGrabber, w3cValidator, robotsChecker, sitemapChecker, twitterChecker, alexaAnalyzer, FacebookCounterTask(),
			SearchTask(),
		)

		data = {}
		actions = []

		for task in tasks:
			report = task.getSavedReport( domainUrl )
			if 'actions' in report:
				actions.extend( report['actions'] )

			defaultData = task.getDefaultData()
			if 'content' in report:
				if type( report['content'] ) == dict:
					defaultData.update( report['content'] )
				else:
					defaultData[ task.getName() ] = report['content']
			data.update( defaultData )

		values['loadTimeMs'] = data['loadTimeMs']

		debugActive = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

		values['shortUrl'] = self.request.url
		if debugActive is False:
			try:
				values['shortUrl'] = create_short_url( self.request.url )
			except:
				logging.error( sys.exc_info()[1] )

		html = self.renderTemplate( 'staticReport.html', values )

		beauty = BeautifulSoup( html )

		beauty.find( id = 'pageTitle' ).replace_with( NavigableString( data['pageTitle'] ) )
		beauty.find( id = 'pageDescription' ).replace_with( NavigableString( data['pageDescription'] if data['pageDescription'] else 'Unknown' ) )
		beauty.find( id = 'docType' ).replace_with( NavigableString( data['docType'] ) )
		beauty.find( id = 'images' ).replace_with( NavigableString( data['images'] ) )
		beauty.find( id = 'headings' ).replace_with( NavigableString( data['headings'] ) )
		beauty.find( id = 'softwareStack' ).replace_with( NavigableString( data['softwareStack'] ) )
		beauty.find( id = 'googleAnalytics' ).replace_with( NavigableString( 'Yes' if data['googleAnalytics'] else 'No' ) )
		beauty.find( id = 'pageSize' ).replace_with( NavigableString( str( data['pageSize'] ) ) )
		beauty.find( id = 'serverIp' ).replace_with( NavigableString( data['serverIp'] ) )

		beauty.find( id = 'screenshot' )['src'] = data['screenshot']

		beauty.find( id = 'worldRank' ).replace_with( NavigableString( data['worldRank'] ) )
		beauty.find( id = 'loadTime' ).replace_with( NavigableString( data['loadTime'] ) )

		beauty.find( id = 'sitemapXml' ).replace_with( NavigableString( data['sitemapXml'] ) )

		beauty.find( id = 'robotsTxt' ).replace_with( NavigableString( data['robotsTxt'] ) )

		beauty.find( id = 'w3cValidity' ).replace_with( NavigableString( data['w3cValidation'] ) )
		
		beauty.find( id = 'facebookComments' ).replace_with( NavigableString( str( data['facebookComments'] ) ) )
		beauty.find( id = 'facebookLikes' ).replace_with( NavigableString( str( data['facebookLikes'] ) ) )
		beauty.find( id = 'facebookShares' ).replace_with( NavigableString( str( data['facebookShares'] ) ) )
		
		beauty.find( id = 'indexedPages' ).replace_with( NavigableString( data['indexedPages'] ) )

		beauty.find( id = 'score' ).contents[0].replace_with( str( siteReport.score ) )

		statuses = {
			'good': 0,
			'regular': 0,
			'bad': 0,
		}

		for action in actions:
			statuses[ action['status'] ] = statuses[ action['status'] ] + 1
		totalStatuses = sum( statuses.values() )

		beauty.find( id = 'goodStatuses' ).replace_with( NavigableString( str( statuses['good'] ) ) )
		beauty.find( id = 'regularStatuses' ).replace_with( NavigableString( str( statuses['regular'] ) ) )
		beauty.find( id = 'badStatuses' ).replace_with( NavigableString( str( statuses['bad'] ) ) )

		if totalStatuses > 0:
			beauty.find( 'div', 'bar bar-success' )['style'] = 'width: %d%%;' % ( ( statuses['good'] * 100 ) / totalStatuses )
			beauty.find( 'div', 'bar bar-warning' )['style'] = 'width: %d%%;' % ( ( statuses['regular'] * 100 ) / totalStatuses )
			beauty.find( 'div', 'bar bar-danger' )['style'] = 'width: %d%%;' % ( ( statuses['bad'] * 100 ) / totalStatuses )

		self.writeResponse( beauty.encode( formatter = None ) )


