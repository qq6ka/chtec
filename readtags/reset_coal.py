# -*- coding: utf-8 -*-
from config_project import *
import time, random, threading, os, sys, datetime
from bson.objectid import ObjectId
from datetime import datetime, timedelta

def get_group_id(env):
	return str(items.find_one({'type':'group','environment':env})['_id'])

# Обнуляем значения по углю за сутки и смену

def Reset(working_time):
	# t=open("/home/root2/mptt/readtags/123.txt", 'a')
	import test_read_tags
	if working_time == 'change':
		# Выбираем значения угля за смену
		tags=items.find({'type':'tag','groups':{'$in':[get_group_id('ttc_raspr_smena')]}})
	if working_time == 'day':
		# Выбираем значения угля за сутки
		tags=items.find({'type':'tag','groups':{'$in':[get_group_id('ttc_raspr_sutki')]}})

	# print >> t, tags.count()
	for tag in tags:
		send={}
		send['result']=0
		send['status']='Ok'
		test_read_tags.Write_data(tag, send=send)



# Генерация суточного отчета
def Gen_report():
	# Даты для выбора из БД
	ts=datetime.now()
	delta = timedelta(days=1)
	start=ts-delta

	# Таймштамп для чтения
	start_ts=datetime(start.year,start.month,start.day)
	start_ts=time.mktime(start_ts.timetuple())
	end_ts=datetime(ts.year,ts.month,ts.day)
	end_ts=time.mktime(end_ts.timetuple())

	tags=items.find({'type':'tag','groups':{'$in':[get_group_id('ttc_raspr_lk')]}})
	for tag in tags:
		day_value=coal.find_one({'tag_id':ObjectId(tag['_id']), 'time':{'$gt':start_ts,'$lt':end_ts}})
		if day_value:
			value = day_value['value']
		else:
			value = 0
		average=({'err_state':0, 'value':repr(value),'start':start_ts,'end':end_ts, 'tag_id':tag['_id']})
		average_day.insert(average)

if __name__ == "__main__":
	if sys.argv[1] == 'change' or sys.argv[1] =='day':
		Reset(sys.argv[1])

	if sys.argv[1]=='gen_reports':
		Gen_report()