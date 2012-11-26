
import sys, logging, json

from library.task.base import BaseTask

from google.appengine.api import urlfetch

class FacebookCounterTask( BaseTask ):
    
    def getName(self):
        return 'facebook'
    
    def getDefaultData(self):
        return {
            'likeCount': 0,
            'commentcount': 0
        }
        
    def start(self, domainUrl):
        content = self.getDefaultData()
        actions = []
        
        import urllib
        params = {
            'query': 'select total_count,like_count,comment_count,share_count,click_count from link_stat where url=\'%s\'' % domainUrl,
            'format': 'json'
        }
        url = 'https://api.facebook.com/method/fql.query?' + urllib.urlencode(params)
        logging.info(url)
        result = urlfetch.fetch( url )
        if result.status_code == 200:
            try:
                data = json.loads( result.content )[0]
                logging.info(data)
                content['likeCount'] = data['like_count']
                content['commentCount'] = data['comment_count']
            except:
                ex = sys.exc_info()[1]
                logging.error(ex)

        
        self.sendAndSaveReport( domainUrl, content, actions)
