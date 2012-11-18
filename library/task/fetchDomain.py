
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
			httpResponse = urllib2.urlopen( 'http://' + url )
			body = httpResponse.read().decode( 'utf8' )
			
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
				'headings': self.extractHeadings( bSoup ),
				'images': self.extractImages( bSoup ),
				'softwareStack': self.extractSoftwareStack( httpResponse ),
				'pageSize': self.extractPageSize( httpResponse ),
			}
			
			logging.info( responseBody['docType'] )

			response = {
				'type': 'htmlBody',
				'body': responseBody, 
			}	

			send_message( channelId, json.dumps( response ) )

		except urllib2.URLError, e:
			logging.error( e )

		domain = Domain.gql( 'WHERE url = :url', url = url ).get()
		if domain is None:
			domain = Domain( url = url )
			domain.put()
		
	def extractDocType( self, bSoup ):
		docType = None
		for child in bSoup.contents:
			if type( child ) == element.Doctype:
				docType = child.string.lower()
				break
		
		if 'html' == docType: docType = 'HTML5'	
		
		return docType
	
	def extractImages( self, bSoup ):
		images = bSoup.find_all( 'img' )
		numImages = len( images )
		numImageswithoutAlt = 0
		for image in images:
			numImageswithoutAlt += 1 if 'alt' not in image.attrs else 0
		
		response = '<p>We found %d images on this website.</p>' % numImages
		response += '<p>%s ALT attributes are empty or missing</p>' % ( 'No' if numImageswithoutAlt == 0 else numImageswithoutAlt )

		return response
	
	def extractHeadings( self, bSoup ):
		headings = bSoup.find_all( ( 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' ) )
		response = {
			'h1': [],
			'h2': [],
			'h3': [],
			'h4': [],
			'h5': [],
			'h6': [],
		}
		for heading in headings:
			response[ heading.name ].append( heading.string )
			
		count = tuple( len( headingElements ) for headingKey, headingElements in response.items() )
		logging.info(count)
		html = """
		<table>
		<tr>
			<th>H1</th>
			<th>H2</th>
			<th>H3</th>
			<th>H4</th>
			<th>H5</th>
			<th>H6</th>
		</tr>
		<tr>
			<td>%d</td>
			<td>%d</td>
			<td>%d</td>
			<td>%d</td>
			<td>%d</td>
			<td>%d</td>
		</tr>
		""" % count
		
		return html

	def extractSoftwareStack( self, httpResponse ):
		softwareStack = []
		if 'Server' in httpResponse.headers:
			if re.match( 'apache', httpResponse.headers['Server'], re.I ):
				softwareStack.append( 'Apache Web (HTTP) server' )
		return '<br />'.join( softwareStack )
	
	def extractPageSize( self, httpResponse ):
		if 'Content-Length' in httpResponse.headers:
			return httpResponse.headers['Content-Length']
		elif 'content-length' in httpResponse.headers:
			return httpResponse.headers['content-length']
		else:
			return len( httpResponse.read() )
		