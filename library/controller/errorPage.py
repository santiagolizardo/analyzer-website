
from library.controller.page import StandardPageController

class ErrorPageController(StandardPageController):

    def get( self ):
        values = {
            'pageTitle': 'See what %s has to tell about your site and your competitors' % self.current_instance['name'],
            'pageDescription': 'Check a detailed list of %s features. All of them are free to use and immediately available.' % self.current_instance['name'],
        }
        
        html = self.renderTemplate('errorPage.html', values)

	self.response.set_status( 404 )
        self.writeResponse( html )

