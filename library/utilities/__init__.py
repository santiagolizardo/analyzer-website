
import webapp2

import config
import unidecode

def uriFor( route_name, **named_params ):
	app_domain = config.current_instance['url']

	special_routes = {
		'liveReport': 'live-report.' + app_domain,
		'staticReport': 'report.' + app_domain,
		'search': 'search.' + app_domain,
	}
    
	named_params['_netloc'] = special_routes[ route_name ] if route_name in special_routes else None
	
	if 'search' == route_name:
		named_params['query'] = unidecode.unidecode( named_params['query'] ).lower().replace( ' ', '-' )
    
	return webapp2.uri_for( route_name, **named_params )

