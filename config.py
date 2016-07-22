# coding=utf-8

import os

debug_active = os.environ['SERVER_SOFTWARE'].startswith( 'Dev' ) 

from local_config import instances

current_instance = None

def load_current_instance():
	global current_instance
	current_domain = os.environ['SERVER_NAME']
	for instance in instances:
		if instance['domain'] in current_domain:
			current_instance = instance
			break

