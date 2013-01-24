#load data from mysql to mongo
import MySQLdb as mdb
import json     
import collections
import datetime 
import decimal  
import pymongo  
from pymongo import Connection
from uuid import uuid4

mongo = Connection('localhost', 27017)

mongo_db = mongo['iaas']
mongo_collection = mongo_db['machine']

db = mdb.connect(unix_socket='', user='', passwd='', db='');
with db:
	cur = db.cursor()

query = """SELECT data to load"""

cur.execute(query)
rows=cur.fetchall()

for row in rows:
		d = collections.OrderedDict()
		d['_id']=uuid4().hex
		#now load data from the select query
		#example
		d['some_date']=row[0].isoformat()[:19].replace('T', ' ') 
		d['string']=row[1]
		d['make_int']=int(row[2])

		mongo_collection.insert(d)

db.close()
