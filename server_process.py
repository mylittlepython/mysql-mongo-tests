#server gets client request, sends input data to databse for processing and returns result to client
#two databases: mysql, mongo

import sys, os
import MySQLdb as mdb
import pymongo
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from pymongo import Connection
from tornado.options import define, options

#tornado represents web server, these are tornado specific settings
define("port", default=8888, help="run on the given port", type=int)
          
#send query to mongodb                                                                                                                                                                                                       
def mondio(param1, param2):
	mongo = Connection('localhost', 27017)
	modb = mongo['db_name']#or collection, don't remember
	query = modb[param1].find({'document_attribute':param2},{'return_doc_attribute':1, 'return_doc_attribute':1})
	rcount = int(query.count())
	return rcount

#send query to mysql 
def runsel(param1, param2, param3):
	con = mdb.connect(unix_socket='unix_socket_connection_path/mysqld.sock', user='user', passwd='psswd', db='db_name');
	cur = con.cursor()
	query = "SELECT COUNT(*) FROM some_table, %s where some_table.sth = %s.%s and some_table.sth_else = '%s' LIMIT 1000" % (param1, param1, param2, param3)
	print query
	cur.execute(query)
	rcount = int(cur.rowcount)
	cur.close()
	con.close()
	return rcount

#handlers
#make sure server gets value parameters
class MondioHandler(tornado.web.RequestHandler):
	def get(self):
		param1 = self.get_argument("param1", None)
		param2  = self.get_argument("param2", None)
		param3  = self.get_argument("param3", None)

		if (param1 is None or param2 is None or param3 is None):
			self.write("ERROR: parameter missing.\n")
		else:
			rowcount = mondio(param1, param2, param3)
			print "rowcount:", rowcount
			self.write("1")

def main():
	tornado.options.parse_command_line()
	application = tornado.web.Application([
		(r'/dio', MainHandler),
		#add more handlers accordingly
	])
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
