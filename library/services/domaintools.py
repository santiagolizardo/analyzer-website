		apiUsername = 'devsantiago.lizardo'
		apiKey = '2dc9a-aceb3-a310e-e73b3-54f1d'
		url = 'http://freeapi.domaintools.com/v1/%s/?format=json&api_username=%s&api_key=%s' % ( baseUrl, apiUsername, apiKey )
		result = urlfetch.fetch( url, deadline = 4 )
		if result.status_code == 200:
			data = json.loads( result.content )
			serverIp = data['response']['server']['ip_address']
			regDate = data['response']['registration']['created']
			expDate = data['response']['registration']['expires']
			owner = data['response']['registrant']['name']


