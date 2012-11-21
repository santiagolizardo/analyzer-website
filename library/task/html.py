
import webapp2
import logging
import urllib2
import json

from library.model.domain import Domain
from library.model.responseBody import ResponseBody

from google.appengine.api.channel import send_message

import time, re, sys

from bs4 import BeautifulSoup, element

from library.task.base import BaseTask

class HtmlAnalyzerTask( BaseTask ):

	def getName( self ): return 'htmlBody'

	def start( self, baseUrl, url, channelId ):
		logging.info( 'Analyzing domain: ' + url )

		content = {
			'pageTitle': 'N/A',
			'pageDescription': 'N/A',
			'googleAnalytics': 'N/A',
			'docType': 'N/A',
			'headings': 'N/A',
			'images': 'N/A',
			'softwareStack': 'N/A',
			'pageSize': 'N/A',
		}

		try:
			httpResponse = urllib2.urlopen( url )
			body = httpResponse.read().decode( 'utf8' )
			
			respbody = ResponseBody( domain = url, length = len( body ), body = body )
			respbody.put()

			
			bSoup = BeautifulSoup( body )

			pageTitle = bSoup.title.string

			pageDescription = None
			metaDescriptions = bSoup.findAll( 'meta', attrs = { 'name': re.compile( '^description$', re.I ) } )
			if len( metaDescriptions ) > 0:
				pageDescription = metaDescriptions[0]['content']

			content = {
				'pageTitle': pageTitle,
				'pageDescription': pageDescription,
				'googleAnalytics': ( '/ga.js' in body ),
				'docType': extractDocType( bSoup ),
				'headings': extractHeadings( bSoup ),
				'images': extractImages( bSoup ),
				'softwareStack': extractSoftwareStack( httpResponse ),
				'pageSize': extractPageSize( httpResponse ),
			}

			self.saveReport( baseUrl, content )

		except:
			e = sys.exc_info()[0]
			logging.error( e )

		self.sendMessage( response )

		domain = Domain.gql( 'WHERE url = :url', url = url ).get()
		if domain is None:
			domain = Domain( url = baseUrl )
			domain.put()
		
def extractDocType( bSoup ):
	docType = None
	for child in bSoup.contents:
		if type( child ) == element.Doctype:
			docType = child.string.lower()
			break
	
	if 'html' == docType: docType = 'HTML5'	
	
	return docType

def extractImages( bSoup ):
	images = bSoup.find_all( 'img' )
	numImages = len( images )
	numImageswithoutAlt = 0
	for image in images:
		numImageswithoutAlt += 1 if 'alt' not in image.attrs else 0
	
	response = '<p>We found %d images on this website.</p>' % numImages
	response += '<p>%s ALT attributes are empty or missing</p>' % ( 'No' if numImageswithoutAlt == 0 else numImageswithoutAlt )

	return response

def extractHeadings( bSoup ):
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

def extractSoftwareStack( httpResponse ):
	softwareStack = []
	if 'Server' in httpResponse.headers:
		if re.match( 'apache', httpResponse.headers['Server'], re.I ):
			softwareStack.append( 'Apache Web (HTTP) server' )
	return '<br />'.join( softwareStack )

def extractPageSize( httpResponse ):
	if 'Content-Length' in httpResponse.headers:
		return httpResponse.headers['Content-Length']
	elif 'content-length' in httpResponse.headers:
		return httpResponse.headers['content-length']
	else:
		return len( httpResponse.read() )
	
