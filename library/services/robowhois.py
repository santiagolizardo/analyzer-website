import urllib2, json
 
class RoboWhois:
	def __init__(self):
		self.username = '7735f18d13df1a015cf347113518362f'
		self.password = "X"

	def whois(self, domain):
		template  = "http://api.robowhois.com/whois/%s/properties"

		passman   = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, "http://api.robowhois.com/", self.username, self.password)
		handler   = urllib2.HTTPBasicAuthHandler(passman)
		opener    = urllib2.build_opener(handler)
		request   = urllib2.Request(template % domain)
		response  = opener.open(request)

		body = response.read()
		return json.loads( body )['response']['properties']

