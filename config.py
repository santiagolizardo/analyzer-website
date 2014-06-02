
import os

debug_active = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 

instances = [
	{
		'domains': ( 'egosize.com' ),
		'language': 'en',
		'url': 'egosize.com',
		'domain': 'egosize.com',
	},
	{
		'domains': ( 'egosize.com.dev' ),
		'language': 'en',
		'url': 'egosize.dev:9090',
		'domain': 'egosize.dev',
	},
	{
		'domains': ( 'egosize.es' ),
		'language': 'es',
		'url': 'egosize.es',
		'domain': 'egosize.es',
	},
	{
		'domains': ( 'egosize.es.dev' ),
		'language': 'es',
		'url': 'egosize.es.dev:9090',
		'domain': 'egosize.es.dev',
	},
]

current_instance = None

def load_current_instance():
	global current_instance
	current_domain = os.environ['SERVER_NAME']
	for instance in instances:
		for domain in instance['domains']:
			if domain in current_domain:
				current_instance = instance
				return

