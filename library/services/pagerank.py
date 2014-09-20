
import httplib

PAGERANK_HOST = 'toolbarqueries.google.com'
PAGERANK_PATH = '/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'
 
def calculateHash( domain ):
	seed = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."
	result = 0x01020345
	for i in range( len( domain ) ):
		result ^= ord( seed[ i % len( seed ) ] ) ^ ord( domain[ i ] )
		result = result >> 23 | result << 9
		result &= 0xffffffff
	return '8%x' % result
 
def getPageRank( domain ):
	hash = calculateHash( domain )
	conn = httplib.HTTPConnection( PAGERANK_HOST )
	path = PAGERANK_PATH % ( hash, domain )
	conn.request( 'GET', path )
	response = conn.getresponse()
	data = response.read()
	conn.close()

	pageRank = data.split(':')[-1]
	if pageRank is None or '' == pageRank:
		raise Exception( 'Unable to retrieve pagerank' )

	try:
		return int( pageRank )
	except ValueError:
		raise Exception( 'Unable to parse pagerank: ' + pageRank )

if __name__ == '__main__':
	import sys
	domain = sys.argv[1] if len( sys.argv ) > 1 else 'www.santiagolizardo.com'
	print 'Domain %s: Pagerank %d' % ( domain, getPageRank( domain ) )

