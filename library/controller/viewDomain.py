
from google.appengine.ext import deferred
from library.controller.page import PageController

import uuid, logging

from google.appengine.api.channel import create_channel

class ViewDomainController( PageController ):

	def get( self, domainUrl ):
		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
		self.addJavaScript( '/_ah/channel/jsapi' )
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		self.addJavaScript( '/scripts/view.js' )
		
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		self.addStyleSheet( '/styles/allmedia.css' )

		sbOptions = (
			{ 'id': 'priority-actions', 'label': 'Priority actions' },
			{ 'id': 'visitors', 'label': 'Visitors' },
			{ 'id': 'social-monitoring', 'label': 'Social monitoring' },
			{ 'id': 'mobile', 'label': 'Mobile' },
			{ 'id': 'seo-basics', 'label': 'SEO basics' },
			{ 'id': 'seo-content', 'label': 'SEO content' },
			{ 'id': 'seo-links', 'label': 'SEO links' },
			{ 'id': 'seo-keywords', 'label': 'SEO keywords' },
			{ 'id': 'seo-authority', 'label': 'SEO authority' },
			{ 'id': 'seo-backlinks', 'label': 'SEO backlinks' },
			{ 'id': 'seo-usability', 'label': 'Usability' },
			{ 'id': 'seo-security', 'label': 'Security' },
			{ 'id': 'seo-technologies', 'label': 'Technologies' },
		)

		channelId = self.request.cookies.get( 'channelId' )
		if channelId is None:
			channelId = uuid.uuid4().hex
			self.response.set_cookie( 'channelId', channelId )
		clientId = create_channel( channelId )

		logging.info( 'channelId( %s ), clientId( %s )' % ( channelId, clientId ) )

		from datetime import date

		values = {
			'domain': domainUrl,
			'domainLength': len( domainUrl.replace( '.com', '' ) ),
			'clientId': clientId,
			'javaScripts': self.javaScripts,
			'styleSheets': self.styleSheets,
			'sbOptions': sbOptions,
			'generatedOnDate': date.today().isoformat(),
			'pageTitle': '%(domainUrl)s | Domain insights for %(domainUrl)s by DomainGrasp.com' % { 'domainUrl': domainUrl },
			'pageDescription': 'Check %(domainUrl)s metrics on SEO, social and other relevant aspects thanks to DomainGrasp'
		}

		logging.info( '>>>> Writing response' )
		html = self.renderTemplate( 'viewDomain.html', values )
		self.writeResponse( html )


