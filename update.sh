#!/bin/bash

appengineapp=$1

appcfg.py --oauth2 --application=$appengineapp update .

