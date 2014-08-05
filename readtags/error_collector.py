# -*- coding: utf-8 -*-
from config_project import *
import datetime, os, time, json
from datetime import datetime, date

class Error_Collection():
	def __call__(self, tagid, e_type):
		curr_collection={}
		for key, value in e_type.items():
			curr_collection.update({'e_type':key,'e_value':value})

		try:
			pred_collection = eval(r.hget(tagid, 'state'))
		except:
			pred_collection={}


		if pred_collection != curr_collection:
			r.hmset(tagid,{'state':''})
			r.hmset(tagid,{'state':json.dumps(curr_collection)})
			r.hmset(tagid,{'state_checked':False})

		return json.dumps(curr_collection)

class Error_Logger():
	def __call__(self, modification, error, message = None):
		now = date.today()
		if not os.access("/home/root2/mptt/readtags/logs/%s" % now, os.F_OK):
			os.mkdir("/home/root2/mptt/readtags/logs/%s" % now)
		log=open("/home/root2/mptt/readtags/logs/%s/%s.txt" % (now, modification), "a")
		print >> log, "%s | %s | %s" % (datetime.now(), error, message)
		log.close()


class Save2txt():
	ferror=Error_Logger()
	def __call__(self, tag, send):
		now = date.today()
		if not os.access("/home/root2/mptt/readtags/tags/%s" % now, os.F_OK):
			try:
				os.mkdir("/home/root2/mptt/readtags/tags/%s" % now)
			except Exception as err:
				ferror("save2txt_errors", err)

		record="{TIME};{VALUE}".format(
			TIME=datetime.fromtimestamp(float(time.time())).strftime('%H:%M:%S'),
			VALUE=repr(send['result']),
			)

		try:
			ftag=open("/home/root2/mptt/readtags/tags/%s/%s.csv" % (now, tag["short_name"].encode('utf-8')), "a")
			print >> ftag, record
			ftag.close()
		except Exception as err:
			ferror("save2txt_errors", err)