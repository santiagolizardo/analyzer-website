
import webapp2

import config

def uriFor( routeName, **namedParams ):
	app_domain = config.current_instance['url']

	specialRoutes = {
		'liveReport': 'live-report.' + app_domain,
		'staticReport': 'report.' + app_domain,
	}
    
	netLoc = None
	if routeName in specialRoutes:
		netLoc = specialRoutes[ routeName ]
    
	namedParams['_netloc'] = netLoc
    
	return webapp2.uri_for( routeName, **namedParams )

