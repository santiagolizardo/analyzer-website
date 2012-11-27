
import sys, logging, json

from library.task.base import BaseTask

from google.appengine.api import urlfetch

class FacebookCounterTask( BaseTask ):
    
    def getName(self):
        return 'facebook'
    
    def getDefaultData(self):
        return {
            'facebookLikes': 0,
            'facebookComments': 0,
            'facebookShares': 0
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
                content['facebookLikes'] = data['like_count']
                content['facebookComments'] = data['comment_count']
                content['facebookShares'] = data['share_count']
                
                totalCount = sum( content.values() )
                if totalCount < 10:
                    actions.append({ 'status': 'bad', 'description': 'Your social activity is almost null. You have to be more social on Facebook' })
                elif totalCount < 100:
                    actions.append({ 'status': 'regular', 'description': 'Your social activity on Facebook is good, but try to engage more users' })
                else:
                    actions.append({ 'status': 'good' })
            except:
                ex = sys.exc_info()[1]
                logging.error(ex)

        
        self.sendAndSaveReport( domainUrl, content, actions)
