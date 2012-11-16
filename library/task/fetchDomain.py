
import webapp2
import logging
import urllib2
import json

from library.model.domain import Domain
from library.model.responseBody import ResponseBody

from google.appengine.api.channel import send_message

import time, re

from bs4 import BeautifulSoup, element

class FetchDomainTaskController( webapp2.RequestHandler ):

	def post( self ):
		url = self.request.get( 'url' )
		channelId = self.request.get( 'channelId' )
		logging.info( 'Analyzing domain: ' + url )
	
		try:
			result = urllib2.urlopen( 'http://' + url )
			body = result.read().decode( 'utf8' )
			
			respbody = ResponseBody( domain = url, length = len( body ), body = body )
			respbody.put()

			bSoup = BeautifulSoup( body )

			pageTitle = bSoup.title.string

			pageDescription = None
			metaDescriptions = bSoup.findAll( 'meta', attrs = { 'name': re.compile( '^description$', re.I ) } )
			if len( metaDescriptions ) > 0:
				pageDescription = metaDescriptions[0]['content']

			responseBody = {
				'pageTitle': pageTitle,
				'pageDescription': pageDescription,
				'googleAnalytics': ( '/ga.js' in body ),
				'docType': self.extractDocType( bSoup ),
			}
			
			logging.info( responseBody['docType'] )

			response = {
				'type': 'htmlBody',
				'body': responseBody, 
			}	

			send_message( channelId, json.dumps( response ) )
			logging.info( '>>>> Message sent to channel' )

		except urllib2.URLError, e:
			logging.error( e )

		domain = Domain( url = url )
		domain.put()
		
	def extractDocType( self, bSoup ):
		docType = None
		for child in bSoup.contents:
			if type( child ) == element.Doctype:
				docType = child.string
				break
		
		if 'html' == docType: docType = 'HTML5'	
		
		return docType
