
import httplib

prhost = 'toolbarqueries.google.com'
prpath = '/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'
 
def getHash( query ):
	SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."
	Result = 0x01020345
	for i in range(len(query)) :
		Result ^= ord(SEED[i%len(SEED)]) ^ ord(query[i])
		Result = Result >> 23 | Result << 9
		Result &= 0xffffffff
	return '8%x' % Result
 
def getPageRank( query ):
	conn = httplib.HTTPConnection(prhost)
	hash = getHash(query)
	path = prpath % (hash,query)
	conn.request("GET", path)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	return data.split(":")[-1]

