
import webapp2, json

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

def checkForRobotsTxt( domain, channelId ):
    url = domain + '/robots.txt'
    result = urlfetch.fetch( url )

    body = 'N/A'
    if result.status_code == 200:
        body = url
    elif result.status_code == 404:
        body = 'Missing' 

    response = {
        'type': 'robotsTxt',
        'body': body,
    }

    send_message( channelId, json.dumps( response ) )

def checkForSitemapXml( domain, channelId ):
    url = domain + '/sitemap.xml'
    result = urlfetch.fetch( url )

    body = 'N/A'
    if result.status_code == 200:
        body = url
    elif result.status_code == 404:
        body = 'Missing' 

    response = {
        'type': 'sitemapXml',
        'body': body,
    }

    send_message( channelId, json.dumps( response ) )



