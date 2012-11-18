
import json, logging

from google.appengine.api import urlfetch
from google.appengine.api.channel import send_message

def runW3cValidation( url, channelId ):
    response = {
        'type': 'w3cValidation',
        'body': 'Unable to contact W3C servers',
    }
    
    url = 'http://validator.w3.org/check?uri=%s&charset=%%28detect+automatically%%29&doctype=Inline&group=1&output=json' % url
    result = urlfetch.fetch( url )
    if result.status_code == 200:
        try:
            data = json.loads( result.content )
            if len( data['messages'] ) == 0:
                response['body'] = 'No errors detected. Great!'
            else:
                counting = { 'info': 0, 'error': 0, 'warning': 0 }
                for message in data['messages']:
                    counting[ message['type'] ] += 1
                del counting['info']
    
                response['body'] = 'Your HTML has %d error(s) and %d warning(s).' % tuple( counting.itervalues() )
        except Error, e:
            logging.error( e )

    send_message( channelId, json.dumps( response ) )
