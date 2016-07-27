
import logging
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

from library.task.base import BaseTask

class HttpsProtocolTask( BaseTask ):

	def getName( self ):
		return 'httpsProtocol'

	def updateView(self, beauty, https_protocol):
		beauty.find( id = 'httpsProtocol' ).string.replace_with( self.generate_html_node(https_protocol) )

	def start(self, domain):
		https_protocol = None 
		try:
		    url = self.create_url(domain)
		    requests.get(url, verify = True, timeout = 5)
		    https_protocol = {
		            'enabled': True,
		            'url': url
		            }
		except requests.exceptions.SSLError, ex:
		    logging.warning(ex)
		except Exception, ex:
		    logging.error(ex)
		
		self.sendAndSaveReport(domain, https_protocol)

	def create_url( self, domain ):
		return 'https://' + domain

	def suggest_actions(self, actions, https_protocol, domain):
	        if https_protocol is None: return

	        if not https_protocol['enabled']:
		    message = ('HTTPS is <u>not enabled</u> for the URL <a href="%(url)s" rel="nofollow">%(url)s</a> which presents a security problem for your users.') % https_protocol
    		    actions.append({ 'status': 'bad', 'description': message })
		else:
		    actions.append({ 'status': 'good' })

	def generate_html_node(self, https_protocol):
            if https_protocol is None: return ('N/A')
            if not https_protocol['enabled']:
                return ('Not enabled (security risk)')

            return ('HTTPS enabled for the URL <a href="%(url)s" rel="nofollow">%(url)s</a>.') % https_protocol

