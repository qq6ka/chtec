# -*- coding: utf-8 -*-
from config_project import *
import time, random, threading, os, sys, datetime, error_collector
from bson.objectid import ObjectId
from datetime import datetime

e_logger=error_collector.Error_Logger()

global_settings.update({'coal_pid': {'$exists': True}},{"$set":{'coal_pid':os.getpid()}})
print os.getpid()

# Последнее значения массы с весов
pred_lk3a=float(global_settings.find_one({'v3a_33': {'$exists': True}})['v3a_33'])
pred_lk3b=float(global_settings.find_one({'v3b_33': {'$exists': True}})['v3b_33'])

print pred_lk3a, pred_lk3b

# Скорость ленты
lk_speed=2.4

# Очередь угля
# if r.hget('queue_coal', 'value'):
# 	queue=eval(r.hget('queue_coal', 'value'))
# else:
# 	queue=[]

queue=[]

def get_group_id(env):
	return str(items.find_one({'type':'group','environment':env})['_id'])

def is_ok(tagid):
	try:
		return float(r.hget(tagid, 'value'))
	except Exception as e:
		# e_logger("coal_errors", e, tagname)
		return None

# Работа с плужками
def Get_Plows(group):
	global lk_speed
	global queue
	gid=str(items.find_one({'type':'group','environment':group})['_id'])

	while True:
		# print queue
		# t=open("/home/root2/mptt/readtags/test.txt", "a")
		# print >> t, group
		plows=list(items.find({'type':'tag', 'groups':{'$in':[gid]}}).sort('_id',1))

		# Пересчитываем местоположение угля
		for coal_pile in queue:
			if coal_pile['lk_id'] == group:
				coal_pile['distance']=coal_pile['distance']+lk_speed*5

		for plow in plows:
			if is_ok(str(plow['_id'])) == 1:
				distance=0
				for plow_group in plow['groups']:
					try:
						distance = float(items.find_one({'_id':ObjectId(plow_group)})['distance'])
						ka_id = items.find_one({'_id':ObjectId(plow_group)})['environment']
						continue
					except:
						pass
				for index, coal_pile in enumerate(queue):
					if abs(float(distance-coal_pile['distance'])) <= 12 and coal_pile['lk_id'] == group:
						Write_data_coal(coal_pile['type_coal'],coal_pile['lk_id'],ka_id,coal_pile['weight'])
						queue.pop(index)

		# Сыпем в 13 котел
		for index, coal_pile in enumerate(queue):
			if coal_pile['distance'] >= 328.5 and coal_pile['lk_id'] == group:
				Write_data_coal(coal_pile['type_coal'],coal_pile['lk_id'],u'ka-13',coal_pile['weight'])
				queue.pop(index)
				
		# r.hmset('queue_coal', {'value':queue})
		# print "___"
		# print eval(r.hget('queue_coal', 'value'))

		time.sleep(5)

# Запись данных по отгрузке в тег.
# В теги, идущие в отчет (тип угля по ЛК) делается кроном отдельно.
def Write_data_coal(type_coal,lk_id,ka_id,weight):
	import test_read_tags
	# Пишем в табличку данные по ссыпке
	ts=datetime.now()
	start=datetime(ts.year,ts.month,ts.day)
	start=time.mktime(start.timetuple())
	tag=items.find_one({'type':'tag',"$and":[{'groups':{'$in':[get_group_id(type_coal)]}}, {'groups':{'$in':[get_group_id(lk_id)]}}, {'groups':{'$in':[get_group_id(ka_id)]}}]})
	current_value=coal.find_one({'tag_id':tag['_id'],'time':{'$gt':start}})
	if current_value:
		coal.update({'_id':ObjectId(current_value['_id'])},{'$inc':{'value':weight},"$set":{'time':time.time()}})
	else:
		value=({'value':weight, 'tag_id':tag['_id'], 'time':time.time(), 'type_coal':type_coal, 'lk_id':lk_id, 'ka_id':ka_id})
		coal.insert(value)

	# Пишем в тег по смене и за сутки
	tags=items.find({'type':'tag',"$and":[{'groups':{'$in':[get_group_id('ttc_raspr_ka')]}}, {'groups':{'$in':[get_group_id(ka_id)]}}]})
	for tag in tags:
		send={}
		predecessor=is_ok(str(tag['_id']))
		if predecessor:
			send['result']=predecessor+weight
		else:
			send['result']=float(weight)
		
		send['status']='Ok'

		test_read_tags.Write_data(tag, send=send)


def Get_Coal_Pile():
	global queue
	global pred_lk3a
	global pred_lk3b
	while True:
		# Переключатель типа ленты
		# Узел пересыпки 3Б
		if is_ok('532b8858080b374f3055627e')==1:
			_3b_to_lk4a=True
		else:
			_3b_to_lk4a=False

		if is_ok('532b8858080b374f3055627f')==1:
			_3b_to_lk4b=True
		else:
			_3b_to_lk4b=False
		
		# Переключатель типа ленты
		# Узел пересыпки 3А
		if is_ok('532b8858080b374f3055627b')==1:
			_3a_to_lk4a=True
		else:
			_3a_to_lk4a=False

		if is_ok('532b8858080b374f3055627c')==1:
			_3a_to_lk4b=True
		else:
			_3a_to_lk4b=False


		# Получаем тип угля
		type_coal=items.find_one({'type':'group','manual':{'$exists': True}, 'manual':1})['environment']

		# Порция угля
		coal_pile={}

		# Весы 3А
		current_lk3a=is_ok('532785ce080b372d7ad15598')
		if current_lk3a > pred_lk3a:
			coal_pile['distance']=0
			coal_pile['type_coal']=type_coal
			if _3a_to_lk4b == True and _3a_to_lk4a == False:
				coal_pile['weight']=current_lk3a-pred_lk3a
				coal_pile['lk_id']='ttc_lk_4b'
				queue.insert(0,coal_pile)
			if _3a_to_lk4a == True and _3a_to_lk4b == False:
				coal_pile['weight']=current_lk3a-pred_lk3a
				coal_pile['lk_id']='ttc_lk_4a'
				queue.insert(0,coal_pile)
			if _3a_to_lk4b == True and _3a_to_lk4a == True:
				coal_pile['weight']=(current_lk3a-pred_lk3a)/2
				coal_pile['lk_id']='ttc_lk_4a'
				queue.insert(0,coal_pile)
				coal_pile['lk_id']='ttc_lk_4b'
				queue.insert(0,coal_pile)
			
		if current_lk3a:
			pred_lk3a = current_lk3a
			global_settings.update({'v3a_33': {'$exists': True}},{"$set":{'v3a_33':current_lk3a}})

		# Весы 3Б
		current_lk3b=is_ok('532787cc080b372d7ad1559b')
		if current_lk3b > pred_lk3b:
			coal_pile['distance']=0
			coal_pile['type_coal']=type_coal
			if _3b_to_lk4b == True and _3b_to_lk4a == False:
				coal_pile['weight']=current_lk3b-pred_lk3b
				coal_pile['lk_id']='ttc_lk_4b'
				queue.insert(0,coal_pile)
			if _3b_to_lk4a == True and _3b_to_lk4b == False:
				coal_pile['weight']=current_lk3b-pred_lk3b
				coal_pile['lk_id']='ttc_lk_4a'
				queue.insert(0,coal_pile)
			if _3b_to_lk4b == True and _3b_to_lk4a == True:
				coal_pile['weight']=(current_lk3b-pred_lk3b)/2
				coal_pile['lk_id']='ttc_lk_4a'
				queue.insert(0,coal_pile)
				coal_pile['lk_id']='ttc_lk_4b'
				queue.insert(0,coal_pile)

		if current_lk3b:
			pred_lk3b = current_lk3b
			global_settings.update({'v3b_33': {'$exists': True}},{"$set":{'v3b_33':current_lk3b}})

		time.sleep(5)

threading.Thread(target=Get_Plows, args=('ttc_lk_4a',)).start()
threading.Thread(target=Get_Plows, args=('ttc_lk_4b',)).start()
threading.Thread(target=Get_Coal_Pile).start()