#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, urllib2, time, sys
from datetime import datetime, timedelta
from config_project import *
from bson.objectid import ObjectId
import elementtree.ElementTree as ET



# Вычитывание суточных архивов для тегов, временно читающихся по http. Потом удалить.
# Запускать с датой или без.

# Даты для запроса
try:
	ts = time.strptime(sys.argv[1], "%d.%m.%Y")
	ts = datetime(ts.tm_year,ts.tm_mon,ts.tm_mday)
except:
	ts = datetime.now()

delta = timedelta(days=1)
new_period = ts-delta
end = datetime(ts.year,ts.month,ts.day).strftime('%d.%m.%Y+%H:%M:%S')
start = datetime(new_period.year,new_period.month,new_period.day).strftime('%d.%m.%Y+%H:%M:%S')

end_for_mongo = datetime(ts.year,ts.month,ts.day)
end_for_mongo = time.mktime(end_for_mongo.timetuple())
start_for_mongo = end_for_mongo-86400

# Получаем список id для запроса
tags = items.find({'type':'tag','alt_arch_parameter':{'$exists': True}},{'alt_arch_parameter':1, '_id':0})
ltags = ",".join(str(tag['alt_arch_parameter']) for tag in tags)

# Строка запроса
def get_response():
	try:
		request="http://172.27.81.199:8080/OSS/bridge/getGraphArc?deltaDateTime=86400&startDate=%s&endDate=%s&queryString=select+[*]+from+Objects[@id+in('%s')]&useScheme=resArchive" % (start,end,ltags)
		resp=urllib2.urlopen(url=request, timeout=30)
		return resp
	except Exception as err:
		print "Timeout", err
		return None
		
response = get_response()

while response is None:
	response = get_response()

# Разбор ответа, запись в БД
root = ET.fromstring(response.read())
for record in root.getiterator('record'):
	for tag in record.getiterator('tag'):
		tag_info=items.find_one({'type':'tag', 'alt_arch_parameter':{'$exists': True}, 'alt_arch_parameter':int(tag.attrib['id'])},{'tag_name':1, '_id':1})
		average=({'tag_id': ObjectId(tag_info['_id']), 'err_state':0, 'tagname':tag_info['tag_name'],'value':float(tag.attrib['value']),'start':start_for_mongo,'end':end_for_mongo})
		average_day.insert(average)
