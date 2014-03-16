
import logging
import urllib2
import json

from library.model.responseBody import ResponseBody

import time, re, sys

from bs4 import BeautifulSoup, element

from library.task.base import BaseTask

import library.geoip as geoip

from bs4 import BeautifulSoup, NavigableString

class HtmlAnalyzerTask( BaseTask ):

	def getName( self ): return 'htmlBody'

	def getDefaultData( self ):

		return {
			'pageTitle': 'N/A',
			'pageDescription': 'N/A',
			'googleAnalytics': 'N/A',
			'docType': 'N/A',
			'headings': 'N/A',
			'images': 'N/A',
			'softwareStack': 'N/A',
			'pageSize': 'N/A',
			'serverIp': 'N/A',
		}

	def updateView( self, beauty, data ):

		beauty.find( id = 'pageTitle' ).replace_with( NavigableString( data['pageTitle'] ) )
		beauty.find( id = 'pageDescription' ).replace_with( NavigableString( data['pageDescription'] if data['pageDescription'] else 'Unknown' ) )
		beauty.find( id = 'docType' ).replace_with( NavigableString( data['docType'] ) )
		beauty.find( id = 'images' ).replace_with( NavigableString( data['images'] ) )
		beauty.find( id = 'headings' ).contents[0].replace_with( NavigableString( data['headings'] ) )
		beauty.find( id = 'softwareStack' ).replace_with( NavigableString( data['softwareStack'] ) )
		beauty.find( id = 'googleAnalytics' ).replace_with( NavigableString( 'Yes' if data['googleAnalytics'] else 'No' ) )
		beauty.find( id = 'pageSize' ).replace_with( NavigableString( str( data['pageSize'] ) ) )
		beauty.find( id = 'serverIp' ).replace_with( NavigableString( data['serverIp'] ) )

	def start( self, baseUrl ):

		url = 'http://' + baseUrl
		
		content = self.getDefaultData()
		actions = []

		try:
			httpReq = urllib2.Request( url )
			httpResp = urllib2.urlopen( httpReq )
			body = httpResp.read().decode( 'utf8' )

			# logging.info( geoip.query( '74.117.156.228', True ) )

			respbody = ResponseBody( domain = url, length = len( body ), body = body )
			respbody.put()

			bSoup = BeautifulSoup( body )

			pageTitle = bSoup.title.string

			pageDescription = None
			metaDescriptions = bSoup.findAll( 'meta', attrs = { 'name': re.compile( '^description$', re.I ) } )
			if len( metaDescriptions ) > 0:
				pageDescription = metaDescriptions[0]['content']

			content.update({
				'pageTitle': pageTitle,
				'pageDescription': pageDescription,
				'googleAnalytics': ( '/ga.js' in body ),
				'docType': extractDocType( bSoup ),
				'headings': extractHeadings( bSoup ),
				'images': extractImages( bSoup ),
				'softwareStack': extractSoftwareStack( httpResp ),
				'pageSize': extractPageSize( httpResp ),
				'serverIp': '%s (%s)' % ( httpReq.get_host(), 'country not available' ),
			})

			if pageTitle is None:
				actions.append({ 'status': 'bad', 'description': 'Your page title is missing. This is critical for SEO and should be fixed ASAP.' })
			elif len( pageTitle ) > 70:
				actions.append({ 'status': 'regular', 'description': 'Your page title is too long. Most of it will be left out from search results.' })
			else:
				actions.append({ 'status': 'good' })

			if not content['googleAnalytics']:
				actions.append({ 'status': 'regular', 'description': 'Add the Google Analytics script to your page to get valuable insights about your visitors' })

			if content['pageSize'] < 20000:
				actions.append({ 'status': 'good' })
			else:
				actions.append({ 'status': 'bad', 'description': 'The page size is too big and should be reduced' })

		except:
			e = sys.exc_info()[1]
			logging.error( str( e ) )

		self.sendAndSaveReport( baseUrl, content, actions )

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
	</table>
	""" % count
	
	return html

def extractSoftwareStack( httpResp ):
	softwareStack = []
	if 'Server' in httpResp.headers:
		if re.match( 'apache', httpResp.headers['Server'], re.I ):
			softwareStack.append( 'Apache Web (HTTP) server' )
	return '<br />'.join( softwareStack )

def extractPageSize( httpResp ):
	if 'Content-Length' in httpResp.headers:
		return httpResp.headers['Content-Length']
	elif 'content-length' in httpResp.headers:
		return httpResp.headers['content-length']
	else:
		return len( httpResp.read() )
	
