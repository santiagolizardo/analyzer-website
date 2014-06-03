
import os

debug_active = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 

instances = [
	{
		'domain': 'egosize.com.dev',
		'language': 'en',
		'url': 'egosize.dev:9090',
		'gaTrackingId': 'UA-48890472-1',
	},
	{
		'domain': 'egosize.com',
		'language': 'en',
		'url': 'egosize.com',
		'gaTrackingId': 'UA-48890472-1',
	},
	{
		'domain': 'egosize.es.dev',
		'language': 'es',
		'url': 'egosize.es.dev:9090',
		'gaTrackingId': 'UA-48890472-3',
	},
	{
		'domain': 'egosize.es',
		'language': 'es',
		'url': 'egosize.es',
		'gaTrackingId': 'UA-48890472-3',
	},
]

current_instance = None

def load_current_instance():
	global current_instance
	current_domain = os.environ['SERVER_NAME']
	for instance in instances:
		if instance['domain'] in current_domain:
			current_instance = instance
			break

