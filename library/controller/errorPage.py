
from library.controller.page import StandardPageController

class ErrorPageController( StandardPageController ):

    def get( self ):

        values = {
            'pageTitle': 'See what EGO size has to tell about your site and your competitors',
            'pageDescription': 'Check a detailed list of EGO size features. All of them are free to use and immediately available.',
        }
        
        html = self.renderTemplate( 'errorPage.html', values)

	self.response.set_status( 404 )
        self.writeResponse( html )

