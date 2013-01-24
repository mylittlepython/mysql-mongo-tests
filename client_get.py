#simulate http put request (client side) 
#client sends parameters to server via put for processing

from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue
import random
import time

#if threading is enabled let the process know how many threads to use
concurrent = #

#data input, list data that the client thread process randomly selects from
list1 = ['data1', 'data2', 'data3']
list2 = [ "data1", "data2","data3"]
#etc...

#keep track of elapsed time and rows returned
eltimes = []
rows = []
                                                                                                                                                                                                     
def doWork():
	while True:
		url=q.get()
		start = time.time()
		status, body = makeRequest(url)
		if status != 200:
			print status, body
			sys.exit(1)
		rows.append(body)
		et = time.time() - start
		eltimes.append(et)
		q.task_done()

def makeRequest(ourl):
	try:
		url = urlparse(ourl)
		conn = httplib.HTTPConnection(url.netloc)
		conn.request("GET", url.path+ '?'+url.query)
		conn.sock.settimeout(90)
		res = conn.getresponse()
		return res.status, res.read()
	except:
		return "error", ourl

def generateQuery():
	#randomize data and form parameters to send to server
	query = "list1=%s&list2=%s&list3=%s" % (list1[random.randint(0, len(list1)-1)],
		list2[list1], list3[random.randint(0, len(list3)-1)])
	return query

#initialize threads
q=Queue(concurrent)
for i in range(concurrent):
	t=Thread(target=doWork)
	t.daemon=True
	t.start()
try:   
	for i in range (2000):
		print generateQuery()
		q.put('http://where_to_send_the_request'+generateQuery())
	q.join()
	#here come the results back from the server
	countrows = 0
	for r in rows:
		countrows += int(r)
	#server communicates with a database, sends client parameters and sends the resultset back to client
	print "total number of queries: ", countrows
	et_sum = 0.0
	for et in eltimes:
		et_sum += et
	av_time = et_sum/len(eltimes)
	print "total average time: {:10.4f}".format(av_time)
except KeyboardInterrupt:
	sys.exit(1)
