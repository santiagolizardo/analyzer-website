
from library.controller.page import StandardPageController

from config import current_instance as site

class ErrorPageController( StandardPageController ):

    def get( self ):

        values = {
            'pageTitle': 'See what %s has to tell about your site and your competitors' % site['name'],
            'pageDescription': 'Check a detailed list of %s features. All of them are free to use and immediately available.' % site['name'],
        }
        
        html = self.renderTemplate('errorPage.html', values)

	self.response.set_status( 404 )
        self.writeResponse( html )

