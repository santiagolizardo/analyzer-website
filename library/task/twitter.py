
import json

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

def checkTwitterAccount( baseDomain, channelId ):
    url = 'http://twitter.com/' + baseDomain
    result = urlfetch.fetch( url )

    body = 'N/A'
    if result.status_code == 200:
        body = 'The twitter&trade; account @%s is booked but it is not linked to your website!' % baseDomain
    elif result.status_code == 404:
        newTwitterAccountUrl = 'http://twitter.com/signup?user[name]=' + baseDomain
        body = 'The Twitter&trade; Account @%s is free. <a href="%s" rel="nofollow" target="_blank">Book it now</a>!' % ( baseDomain, newTwitterAccountUrl ) 

    response = {
        'type': 'twitterAccount',
        'body': body,
    }

    send_message( channelId, json.dumps( response ) )


