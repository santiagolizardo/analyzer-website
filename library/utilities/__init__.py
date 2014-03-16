
import os, webapp2

def isDebugActive():
    return os.environ['SERVER_SOFTWARE'].startswith( 'Dev' )

def uriFor( routeName, **namedParams ):
    domainExt = 'dev:9090' if isDebugActive() else 'com' 

    specialRoutes = {
        'liveReport': 'live-report.egosize.' + domainExt,
        'staticReport': 'report.egosize.' + domainExt,
    }
    
    netLoc = None
    if routeName in specialRoutes:
        netLoc = specialRoutes[ routeName ]
    
    namedParams['_netloc'] = netLoc
    
    return webapp2.uri_for( routeName, **namedParams )
