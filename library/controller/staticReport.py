
from google.appengine.ext import deferred
from library.controller.page import PageController

import uuid, logging

from datetime import date

from google.appengine.api.channel import create_channel

class StaticReportController( PageController ):

	def get( self, domainUrl ):
		self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
		self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
		
		self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
		self.addStyleSheet( '/styles/allmedia.css' )

		sbOptions = (
			{ 'id': 'priority-actions', 'label': 'Priority actions' },
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
		self.writeResponse( html )


