
from library.controller.page import StandardPageController

class ErrorPageController( StandardPageController ):

    def get( self ):
        self.addJavaScript( '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js' )
        self.addJavaScript( '/bootstrap/js/bootstrap.min.js' )
        
        self.addStyleSheet( '/bootstrap/css/bootstrap.min.css' )
        self.addStyleSheet( '/styles/allmedia.css' )

        values = {
            'pageTitle': 'See what DomainGrasp has to tell about your site and your competitors',
            'pageDescription': 'Check a detailed list of DomainGrasp features. All of them are free to use and immediately available.',
        }
        
        html = self.renderTemplate( 'errorPage.html', values)

	self.response.set_status( 404 )
        self.writeResponse( html )

