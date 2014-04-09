
import logging
import urllib2
import json

import pycountry

from library.model.responseBody import ResponseBody

import re, sys

from bs4 import BeautifulSoup, element

from library.task.base import BaseTask

class HtmlAnalyzerTask( BaseTask ):

	def getName( self ): return 'htmlBody'

	def getDefaultData( self ):

		return {
			# Page Metadata
			'pageTitle': 'N/A',
			'pageDescription': 'N/A',
			'pageKeywords': 'N/A',

			'googleAnalytics': 'N/A',
			'docType': 'N/A',
			'headings': 'N/A',
			'images': 'N/A',
			'softwareStack': 'N/A',
			'pageSize': 'N/A',

			'textHtmlRatio': 'N/A',

			'declaredLanguage': None,
			
			'encoding': None,
			
			'emailAddresses': None,
			
			'internalLinks': None,

			'containsFlash': None,
			'pageCompression': None,
		}

	def updateView( self, beauty, data ):

		# Page Metadata
		beauty.find( id = 'pageTitle' ).string.replace_with( data['pageTitle'] )
		beauty.find( id = 'pageDescription' ).string.replace_with( data['pageDescription'] if data['pageDescription'] else 'Unknown' )
		beauty.find( id = 'pageKeywords' ).string.replace_with( data['pageKeywords'] if data['pageKeywords'] else 'Unknown' )

		beauty.find( id = 'docType' ).string.replace_with( data['docType'] )
		beauty.find( id = 'images' ).string.replace_with( data['images'] )
		beauty.find( id = 'headings' ).contents[0].replace_with( data['headings'] )
		beauty.find( id = 'softwareStack' ).string.replace_with( data['softwareStack'] )
		beauty.find( id = 'googleAnalytics' ).string.replace_with( 'Yes' if data['googleAnalytics'] else 'No' )
		beauty.find( id = 'pageSize' ).string.replace_with( str( data['pageSize'] ) )
		
		try:
			beauty.find( id = 'textHtmlRatio' ).string.replace_with( '%.2f%%' % float( data['textHtmlRatio'] * 100 ) )
		except:
			logging.error(sys.exc_info()[0])
			beauty.find( id = 'textHtmlRatio' ).string.replace_with( 'N/A' )
	
		if 'declaredLanguage' in data and data['declaredLanguage'] is not None:
			beauty.find( id = 'declaredLanguage' ).string.replace_with( data['declaredLanguage'] )
		else:
			beauty.find( id = 'declaredLanguage' ).string.replace_with( 'N/A' )

		if 'encoding' in data and data['encoding'] is not None:
			beauty.find( id = 'encoding' ).string.replace_with( data['encoding'] )
		else:
			beauty.find( id = 'encoding' ).string.replace_with( 'N/A' )

		if 'emailAddresses' in data and data['emailAddresses'] is not None:
			beauty.find( id = 'emailAddresses' ).string.replace_with( data['emailAddresses'] )

		if 'internalLinks' in data and data['internalLinks'] is not None:
			beauty.find( id = 'internalLinks' ).string.replace_with( data['internalLinks'] )

		if 'containsFlash' in data and data['containsFlash'] is not None:
			beauty.find( id = 'containsFlash' ).string.replace_with( data['containsFlash'] )

	def start( self, baseUrl ):

		url = 'http://' + baseUrl
		
		content = self.getDefaultData()
		actions = []

		try:
			httpReq = urllib2.Request( url )
			httpResp = urllib2.urlopen( httpReq )
			body = httpResp.read().decode( 'utf8' )

			respbody = ResponseBody( domain = url, length = len( body ), body = body )
			respbody.put()

			bSoup = BeautifulSoup( body )

			pageTitle = bSoup.title.string

			page_size = extractPageSize( httpResp, body )

			try:
				textHtmlRatio = len( bSoup.get_text() ) / float( page_size )
			except:
				logging.error(sys.exc_info()[0])
				textHtmlRatio = 'N/A'

			email_addresses_list = extractEmailAddresses( body )
			if len( email_addresses_list ) > 0:
				actions.append({ 'status': 'bad', 'description': 'Remove or encode the found email addresses to prevent be victim of spammers.' })

			content.update({
				'googleAnalytics': ( '/ga.js' in body ),
				'docType': extractDocType( bSoup ),
				'headings': extractHeadings( bSoup ),
				'images': extractImages( bSoup ),
				'softwareStack': extractSoftwareStack( httpResp ),
				'pageSize': page_size,
				
				'textHtmlRatio': textHtmlRatio,

				'declaredLanguage': extractLanguage( bSoup ),
				
				'encoding': extractEncoding( httpResp ),

				'emailAddresses': ', '.join( email_addresses_list ),
				
				'internalLinks': extractInternalLinks( bSoup, baseUrl ),

				'containsFlash': containsFlash( body, actions ),
				'pageCompression': pageCompression( httpResp, actions ),
			})

			# Page Metadata
			metaDescription = bSoup.find( 'meta', attrs = { 'name': re.compile( '^description$', re.I ) } )
			if metaDescription is not None:
				content['pageDescription'] = metaDescription['content']
			metaKeywords = bSoup.find( 'meta', attrs = { 'name': re.compile( '^keywords$', re.I ) } )
			if metaKeywords is not None:
				content['pageKeywords'] = metaKeywords['content']

			if pageTitle is None:
				actions.append({ 'status': 'bad', 'description': 'Your page title is missing. This is critical for SEO and should be fixed ASAP.' })
			elif len( pageTitle ) > 70:
				actions.append({ 'status': 'regular', 'description': 'Your page title is too long. Most of it will be left out from search results.' })
				content['pageTitle'] = pageTitle
			else:
				actions.append({ 'status': 'good' })
				content['pageTitle'] = pageTitle

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

def containsFlash( body, actions ):
	if '.swf"' in body:
		actions.append({ 'status': 'bad', 'description': 'Replace your Flash content with JavaScript for UI enhancements and interaction' })
		return 'The page contains Flash content'
	return 'No Flash has been found in the page'

def extractDocType( bSoup ):
	detected_doc_type = None
	for child in bSoup.contents:
		if type( child ) == element.Doctype:
			detected_doc_type = child.string
			break

	if detected_doc_type is None:
		return 'N/A'

	doc_types = (
		{
			'name': 'XHTML 1.1',
			'string': 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"',
			'sub_string': 'DTD XHTML 1.1',
		},
		{
			'name': 'XHTML 1.0 Frameset',
			'string': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"',
			'sub_string': 'DTD XHTML 1.0 Frameset',
		},
		{
			'name': 'XHTML 1.0 Transitional',
			'string': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"',
			'sub_string': 'DTD XHTML 1.0 Transitional',
		},
		{
			'name': 'XHTML 1.0 Strict',
			'string': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"',
			'sub_string': 'DTD XHTML 1.0 Strict',
		},
		{
			'name': 'HTML 4.01 Frameset',
			'string': 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"',
			'sub_string': 'DTD HTML 4.01 Frameset',
		},
		{
			'name': 'HTML 4.01 Transitional',
			'string': 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"',
			'sub_string': 'DTD HTML 4.01 Transitional',
		},
		{
			'name': 'HTML 4.01 Strict',
			'string': 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"',
			'sub_string': 'DTD HTML 4.01',
		},
		{
			'name': 'HTML 5',
			'string': 'html',
			'sub_string': 'html',
		}
	)

	# First try full string
	for doc_type in doc_types:
		if doc_type['string'].lower() == detected_doc_type.lower():
			return doc_type['name']

	# Second try sub string
	for doc_type in doc_types:
		if doc_type['sub_string'].lower() == detected_doc_type.lower():
			return doc_type['name']

	# Else unknown
	return 'Unknown (%s)' % detected_doc_type	

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
		temp = heading.text
		if len( temp ) > 0:
			response[ heading.name.lower() ].append( temp )
		
	count = [ len( items ) for items in response.values() ]

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
	""" % tuple( count )

	listing = [ '<ul>' ]
	for headerSize, headerValues in response.items():
		for headerValue in headerValues:
			listing.append( '<li><strong>%s</strong> %s</li>' % ( headerSize, headerValue ) )
	listing.append( '</ul>' )

	html = html + ''.join( listing )
	
	return html

def pageCompression( httpResp, actions ):
	if 'Content-Encoding' in httpResp.headers:
		if 'gzip' in httpResp.headers['Content-Encoding']:
			return 'Gzip is enabled. Great!'
		else:
			actions.append({ 'status': 'regular', 'description': 'Your server does not have Gzip compression enabled. Activate it to deliver faster pages.' })

	return 'N/A'

def extractSoftwareStack( httpResp ):
	softwareStack = []
	if 'Server' in httpResp.headers:
		if re.match( 'apache', httpResp.headers['Server'], re.I ):
			softwareStack.append( 'Apache Web (HTTP) server' )
	return '<br />'.join( softwareStack )

def extractEncoding( httpResp ):
	if 'Content-Type' in httpResp.headers:
		match = re.search( 'charset=(.*)', httpResp.headers['Content-Type'] )
		if match:
			encod = match.group( 1 ).upper()
			return encod
		return None

	#dic_of_possible_encodings = chardet.detect(unicode(soup))
	#encod = dic_of_possible_encodings['encoding'] 

	return None

def extractPageSize( httpResp, body ):
	if 'Content-Length' in httpResp.headers:
		return int( httpResp.headers['Content-Length'] )
	elif 'content-length' in httpResp.headers:
		return int( httpResp.headers['content-length'] )
	else:
		return len( body )
	
def extractLanguage( bSoup ):
	if 'lang' not in bSoup.html:
		return 'N/A'

	try:
		language = bSoup.html['lang']
		try:
			return pycountry.languages.get( alpha2 = language ).name
		except:
			logging.error( sys.exc_info()[0] )
	except:
		logging.error( sys.exc_info()[0] )
		return 'N/A'

def extractEmailAddresses( body ):
	email_re = re.compile( r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}' )
	return set( email_re.findall( body ) )

def extractInternalLinks( bSoup, domain ):
	links = bSoup.find_all( 'a', href = re.compile( domain ) )
	if len( links ) > 0:
		links = links[:3]
		html = [ '<ul>' ]
		for link in links:
			html.append( '<li><a href="%s" class="external" rel="nofollow" target="_blank">%s</a></li>' % ( link['href'], link['href'] ) )
		html.append( '</ul>' )
		return ''.join( html )
	return 'N/A'

