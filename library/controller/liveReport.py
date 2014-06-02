
from library.controller.page import StandardPageController
from library.utilities import uriFor
from library.model.report import SiteReport

import uuid, logging

from google.appengine.api.channel import create_channel

from library.sections import reportSections

class LiveReportController( StandardPageController ):

	def get( self, domainUrl ):
		report = SiteReport.all().filter( 'url =', domainUrl ).get()
		if report is not None:
			url = uriFor( 'staticReport', domainUrl = domainUrl )
			self.redirect( url )
			return

		self.addJavaScript( '/_ah/channel/jsapi' )
		self.addJavaScript( '/scripts/liveReport.js' )
		
		channelId = self.request.cookies.get( 'channelId' )
		if channelId is None:
			channelId = uuid.uuid4().hex
			self.response.set_cookie( 'channelId', channelId )
		clientId = create_channel( channelId )

		from datetime import date

		values = {
			'domain': domainUrl,
			'domainLength': len( domainUrl.replace( '.com', '' ) ),
			'clientId': clientId,
			'sbOptions': reportSections,
			'pageTitle': '%(domainUrl)s | Domain insights for %(domainUrl)s by Egosize' % { 'domainUrl': domainUrl },
			'pageDescription': 'Check %(domainUrl)s metrics on SEO, social and other relevant aspects thanks to Egosize'
		}

		html = self.renderTemplate( 'liveReport.html', values )
		self.writeResponse( html )


