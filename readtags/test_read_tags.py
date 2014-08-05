## -*- coding: utf-8 -*- 
import threading, time, queue_sender, os, redis, error_collector, datetime, dcon, mark, subprocess
from threading import Timer
from config_project import *
from datetime import datetime
import device as device_type
import Pyro4

e_collection=error_collector.Error_Collection()
aperture=0.001
save2txt=error_collector.Save2txt()
comp_dcon=dcon.Calculate_values()

def add_q(queue,bus,id):
	current_bus=items.find_one({'_id':ObjectId(bus['_id'])})
	if current_bus['interview']:
		init_bus=device_type.Bus()

		# Строки соединения может не быть, если это вычисляемые теги
		if 'connect' in current_bus:
			connect2bus=[]
			for param in current_bus['connect']:
				connect2bus.append(current_bus.get(param))

		for device in items.find({'parent':ObjectId(bus['_id']), 'interview':True}):
			init_device=device_type.Device()
			if device['modification']=='aist-tornado':
				tags=items.find({'parent':ObjectId(device['_id']), 'interview':True, 'groups':{'$in':[str(id)]}},{'tag_name':1, '_id':0})
				tags=[tag['tag_name'] for tag in tags]
				if tags:
					init_specification=device_type.Tornado(
						name=device['name'],
					    parent=device['parent'],
					    connection=connect2bus,
					    bus=init_bus,
					    interview=device['interview'],
					    _id=device['_id'],
					    tags=tags,
					    group=id,
					    device=init_device
					)
					queue.queue.append(init_specification)

			elif device['modification']=='dcon7053':
				init_specification=device_type.Dcon7053(
					name=device['name'],
					parent=device['parent'],
					bus=init_bus,
					interview=device['interview'],
					connection=connect2bus,
					_id=device['_id'],
					group=id,
					device=init_device,
					bus_address=device['bus_address']
				)
				queue.queue.append(init_specification)

			elif device['modification']=='mark-902':
				tags=items.find({'parent':ObjectId(device['_id']), 'type':'tag', 'interview':True, 'groups':{'$in':[str(id)]}})
				if tags:
					for tag in tags:
						init_specification=device_type.Mark902(
							name=device['name'],
							parent=device['parent'],
							bus=init_bus,
							interview=device['interview'],
							connection=connect2bus,
							_id=device['_id'],
							device=init_device,
							bus_address=device['bus_address'],
							channel=tag['channel'],
							parameter=tag['parameter'],
							group=id,
						)
						queue.queue.append(init_specification)

			elif device['modification']=='mark-602':
				tags=items.find({'parent':ObjectId(device['_id']), 'type':'tag', 'interview':True, 'groups':{'$in':[str(id)]}})
				if tags:
					for tag in tags:
						init_specification=device_type.Mark602(
							name=device['name'],
							parent=device['parent'],
							bus=init_bus,
							interview=device['interview'],
							connection=connect2bus,
							_id=device['_id'],
							device=init_device,
							bus_address=device['bus_address'],
							channel=tag['channel'],
							parameter=tag['parameter'],
							group=id,
						)
						queue.queue.append(init_specification)

			elif device['modification']=='dcon7017':
				init_specification=device_type.Dcon7017(
					name=device['name'],
					parent=device['parent'],
					bus=init_bus,
					interview=device['interview'],
					connection=connect2bus,
					_id=device['_id'],
					group=id,
					device=init_device,
					bus_address=device['bus_address']
				)
				queue.queue.append(init_specification)

			elif device['modification']=='logika':
				if current_bus['alt_mode'] == False:
					tags=list(items.find({'parent':ObjectId(device['_id']), 'type':'tag', 'interview':True, 'groups':{'$in':[str(id)]}},{'_id':1, 'channel':1, 'parameter':1}))
					tags_limit=15
					if len(tags) > 0:
						groups_tags = [tags[tag:tag+tags_limit] for tag in range(0, len(tags), tags_limit)]
						for group in groups_tags:
							tags_hash={}
							for tag in group:
								tags_hash[str(tag['_id'])]=[tag['channel'],tag['parameter']]

							init_specification=device_type.Logika(
								name=device['name'],
							    parent=device['parent'],
							    connection=connect2bus,
							    bus=init_bus,
							    interview=device['interview'],
							    _id=device['_id'],
							    tags=tags_hash,
							    group=id,
							    device=init_device,
							    dad=device['dad'],
							    sad=device['sad']
							)
							queue.queue.append(init_specification)
				elif current_bus['alt_mode'] == True:
					device['modification']=='alt-logika'
					tags=items.find({'alt_id': {'$exists': True}, 'parent':ObjectId(device['_id']), 'type':'tag', 'interview':True, 'groups':{'$in':[str(id)]}},{'alt_id':1, '_id':0})
					tags=[str(tag['alt_id']) for tag in tags]
					if tags:
						init_specification=device_type.AltLogika(
							name=device['name'],
						    parent=device['parent'],
						    bus=init_bus,
						    interview=device['interview'],
						    _id=device['_id'],
						    tags=tags,
						    group=id,
						    device=init_device
						)
						queue.queue.append(init_specification)
			elif device['modification']=='computational':
				tags=items.find({'parent':ObjectId(device['_id']), 'type':'tag', 'interview':True, 'groups':{'$in':[str(id)]}},{'_id':1})
				tags=[str(tag['_id']) for tag in tags]
				if tags:
					init_specification=device_type.Computational(
						name=device['name'],
					    parent=device['parent'],
					    bus=init_bus,
					    interview=device['interview'],
					    _id=device['_id'],
					    tags=tags,
					    group=id,
					    device=init_device,
					    groups=device['groups']
					)
					queue.queue.append(init_specification)

			elif device['modification']=='expression':
				tags=items.find({'parent':ObjectId(device['_id']), 'type':'tag', 'interview':True, 'groups':{'$in':[str(id)]}})
				if tags:
					for tag in tags:
						init_specification=device_type.Expression(
							name=device['name'],
						    parent=device['parent'],
						    bus=init_bus,
						    interview=device['interview'],
						    _id=device['_id'],
						    tag=tag,
						    group=id,
						    device=init_device,
						)
						queue.queue.append(init_specification)

			elif device['modification']=='modbus':
				functions=items.find({'parent':ObjectId(device['_id']), 'interview':True, 'groups':{'$in':[str(id)]}}).distinct('function')
				init_specification=device_type.Modbus(
					bus=init_bus,
					connection=connect2bus,
					channels=device['channels'],
					name=device['name'],
					parent=device['parent'],
					interview=device['interview'],
					_id=device['_id'],
					bus_address=device['bus_address'],
				    device=init_device
				)

				for function in functions:
					# Чтение аналоговых каналов Метрана
					if function == 4:
						init_specification.function=[init_specification.bus_address,function,0,init_specification.channels*2]
						init_specification.group=id
						queue.queue.append(init_specification)

def Get_Queue(queue):
	while True:
		# Вычитывание текущих данных
		if queue.queue:
			request=queue.queue.pop(0)
			response = request.read()

			if request.modification=='logika':
				if response['status']=='Ok':
					for channel, value in response['result'].items():
						tag=items.find_one({'parent':ObjectId(request._id), 'channel':int(channel[0]), 'parameter':int(channel[1]), 'interview':True, 'groups':{'$in':[str(request.group)]}})
						response={}
						if tag:
							try:
								response['status']='Ok'
								response['result'] = float(value)
								Write_data(tag, send=response)
							except Exception as e:
								response['result'] = 'Error'
								response['status'] = u'Выход за границы'
								state = e_collection(str(tag['_id']),{response['status']:True})
								Write_data(tag, state, send=response)
				elif response['status'] in (None, u'Нет соединения с устройством', u'Не совпала контрольная сумма', u'Нет соединения с шиной'):
					tags=items.find({'parent':ObjectId(request._id), 'interview':True, 'groups':{'$in':[str(request.group)]}})
					for tag in tags:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)
			elif request.modification == 'computational':
				if response['status']=='Ok':
					for tname, value in response['result'].items():
						tag=items.find_one({'parent':ObjectId(request._id), 'ident':tname, 'interview':True, 'groups':{'$in':[str(request.group)]}})
						response['status']='Ok'
						response['result'] = value
						Write_data(tag, send=response)
				else:
					tags=items.find({'parent':ObjectId(request._id), 'interview':True, 'groups':{'$in':[str(request.group)]}})
					for tag in tags:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)

			elif request.modification == 'expression':
				if response['status']=='Ok':
					Write_data(request.tag, send=response)
				else:
					response['result'] = 'Error'
					state = e_collection(str(request.tag['_id']),{response['status']:True})
					Write_data(request.tag, state, send=response)

			elif request.modification == 'modbus':
				if response['status']=='Ok':
					for channel, value in response['result'].items():
						tag=items.find_one({'parent':ObjectId(request._id), 'channel':channel, 'interview':True, 'function':request.function[1], 'groups':{'$in':[str(request.group)]}})
						response={}
						if tag and (str(value)=='inf' or str(value)=='nan'):
							response['result'] = 'Error'
							response['status'] = u'Выход за границы'
							state = e_collection(str(tag['_id']),{response['status']:True})
							Write_data(tag, state, send=response)
						elif tag:
							response['status']='Ok'
							response['result'] = value
							Write_data(tag, send=response)
				elif response['status'] in (None, u'Нет соединения с устройством', u'Не совпала контрольная сумма', u'Выход за границы', u'Нет соединения с шиной'):
					tags=items.find({'parent':ObjectId(request._id), 'interview':True, 'function':request.function[1], 'groups':{'$in':[str(request.group)]}})
					for tag in tags:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)

			elif request.modification == "dcon7053":
				if response['status']=='Ok':
					for channel, value in response['result'].items():
						tag=items.find_one({'parent':ObjectId(request._id), 'channel':channel, 'interview':True, 'groups':{'$in':[str(request.group)]}})
						response={}
						if tag:
							response['status']='Ok'
							response['result'] = value
							Write_data(tag, send=response)
				elif response['status'] in (u'Нет соединения с шиной', u'Нет соединения с устройством', u'Ошибка чтения с устройства'):
					tags=items.find({'parent':ObjectId(request._id), 'interview':True, 'groups':{'$in':[str(request.group)]}})
					for tag in tags:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)

			elif request.modification == "dcon7017":
				if response['status']=='Ok':
					for channel, value in response['result'].items():
						tag=items.find_one({'parent':ObjectId(request._id), 'channel':channel, 'interview':True, 'groups':{'$in':[str(request.group)]}})
						response={}
						if tag:
							response['status']='Ok'
							response['result'] = value
							r.hmset(tag["short_name"], {'value':value})
							# Write_data(tag, send=response)
					comp_dcon(request.name)
				elif response['status'] in (u'Нет соединения с шиной', u'Нет соединения с устройством', u'Ошибка чтения с устройства'):
					tags=items.find({'parent':ObjectId(request._id), 'interview':True, 'groups':{'$in':[str(request.group)]}})
					for tag in tags:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)

			elif request.modification=='aist-tornado':
				if response['status']=='Ok':
					for tagname, value in response['result'].items():
						tag=items.find_one({'tag_name':tagname})
						response['status']='Ok'
						response['result']=value
						Write_data(tag, send=response)
				elif response['status'] in ('Timeout',u'Нет соединения с шиной'):
					tags=items.find({'parent':ObjectId(request._id), 'interview':True, 'groups':{'$in':[str(request.group)]}})
					for tag in tags:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)

			elif request.modification in ("mark-902", "mark-602"):
				if response['status']=='Ok':
					tag = items.find_one({'parent':ObjectId(request._id), 'channel':response['channel'], 'parameter':response['parameter'], 'interview':True, 'groups':{'$in':[str(request.group)]}})
					if tag:
						response['status']='Ok'
						response['result'] = response['result']
						Write_data(tag, send=response)
				elif response['status'] in (None, u'Нет соединения с устройством', u'Не совпала контрольная сумма', u'Нет соединения с шиной'):
					tag = items.find_one({'parent':ObjectId(request._id), 'interview':True, 'groups':{'$in':[str(request.group)]}})
					if tag:
						response['result'] = 'Error'
						state = e_collection(str(tag['_id']),{response['status']:True})
						Write_data(tag, state, send=response)

			del response
		else:
			time.sleep(1)

		# Вычитывание из очереди, а которую добавляются архивные теги, вычитка и запись каналов. Выполняется с ожиданием завершения работы.
		todo=Pyro4.Proxy("PYRO:todo@localhost:5150")
		if todo.exist(queue.id):
			todo_request = todo.get(queue.id)
			if todo_request[-1] == "read_arch":
				# Вычитываем архивы
				todo_request = todo_request[:-1]
				subprocess.call(['python', '/home/root2/mptt/readtags/logika_arch.py', str(todo_request)])

			if todo_request[-1] == "read_value":
				todo_request = todo_request[:-1]
				subprocess.call(['python', '/home/root2/mptt/readtags/logika_value.py', str(todo_request)])

			if todo_request[-1] == "write_value":
				todo_request = todo_request[:-1]
				subprocess.call(['python', '/home/root2/mptt/readtags/logika_write.py', str(todo_request)])

def Write_data(tag, state=None, send=None):
	def get_group_id(env):
		group=items.find_one({'type':'group','environment':env})
		if group:
			return group['_id']

	# Получаем единицы измерения тега
	def get_units_by_group_id(groups):
		unit = items.find_one({'_id':{'$in':[ObjectId(x) for x in groups]},'environment':'units'},{'name':1, '_id':0})
		if unit:
			return unit['name']
		else:
			return u'н/а'

	unit = get_units_by_group_id(tag['groups'])


	ts=datetime.now()
	ts_second=time.time()
	last_coll = str(datetime(ts.year,ts.month,ts.day,ts.hour))
	data=db_arch[last_coll]
	predecessor=r.hget(str(tag['_id']), 'value')

	# Проверка ручного ввода
	try:
		send['result']=float(tag['manual'])
		send['status']='Ok'
	except:
		pass

	# Проверка подсветки
	if 'bg_color' in tag:
		bg_color = tag['bg_color']
	else:
		bg_color = 'transparent'

	if send['status']=='Ok':
		setpoint=items.find_one({'_id':ObjectId(tag['_id'])},{'normal':1, 'attention':1, '_id':0})
		if setpoint:
			if setpoint['normal'][0] < float(send['result']) < setpoint['normal'][1]:
				status=0
			elif setpoint['attention'][0] < float(send['result']) < setpoint['normal'][0] or setpoint['normal'][1] < float(send['result']) < setpoint['attention'][1]:
				status=1
			else:
				status=2
		else:
			status='0'

		state=e_collection(str(tag['_id']),{'Выход за уставки':status})

		if predecessor in ('Error', None) or aperture <= abs(float(predecessor)-float(repr(send['result']))):
			r.hmset(str(tag['_id']), {'bg_color':bg_color, 'tag_id':tag['_id'], 'unit':unit, 'value':repr(send['result']), 'status':status, 'time':time.time(), 'name':tag['name'], 'short_name':tag['short_name']})
			current_tag=({'tag_id':tag['_id'], 'value':float(repr(send['result'])),'time':time.time(),'status':status, 'state':state})
			data.insert(current_tag)
			save2txt(tag,send)
		elif aperture > abs(float(predecessor)-float(repr(send['result']))):
			r.hmset(str(tag['_id']), {'bg_color':bg_color, 'tag_id':tag['_id'], 'unit':unit, 'status':status, 'time':time.time(), 'name':tag['name'], 'short_name':tag['short_name'], 'state':state})

		# Пишем в Редис 20 значений если тег в соотв. группе
		if get_group_id('save2redis') in tag['groups']:
			result={
				'value':repr(send['result']),
				'time':time.time()
			}
			if r.hget(str(tag['_id']), 'list_values'):
				list_values=eval(r.hget(str(tag['_id']), 'list_values'))
				if len(list_values)<20:
					if float(list_values[-1]['value'])!=float(repr(send['result'])):
						list_values.append(result)
					else:
						if float(ts_second)-float(list_values[-1]['time']) >= 300:
							list_values=[]
							list_values.append(result)
				else:
					if float(list_values[-1]['value'])!=float(repr(send['result'])):
						list_values.pop(0)
						list_values.append(result)
					else:
						if float(ts_second)-float(list_values[-1]['time']) >= 300:
							list_values=[]
							list_values.append(result)
			else:
				list_values=[result]

			r.hmset(str(tag['_id']), {'list_values':list_values})

	elif send['status'] in (None, u'Ошибка в расчете', u'Нет данных о Q пп за котлом', u'Нет соединения с устройством', u'Не совпала контрольная сумма', u'Выход за границы', u'Нет соединения с шиной', u'Истек период ожидания'):
		status=2
		r.hmset(str(tag['_id']), {'bg_color':bg_color, 'tag_id':tag['_id'], 'unit':unit, 'value':'Error', 'status':status, 'time':time.time(), 'name':tag['name'], 'short_name':tag['short_name']})
		if predecessor != 'Error':
			current_tag=({'tag_id':tag['_id'], 'value':'Error','time':time.time(),'status':status, 'state':state})
			data.insert(current_tag)
			save2txt(tag,send)


def Sheduler(time2select,id,queue,bus):
	while True:
		if len(queue.queue) == 0:
			add_q(queue,bus,id)

		time.sleep(time2select)

if __name__ == "__main__":
	global_settings.update({'pid': {'$exists': True}},{"$set":{'pid':os.getpid()}})
	buses=items.find({'type':'bus'}).sort('interview')
	print "Last restart: ", datetime.now(), "PID: ", os.getpid(), "pymongo version:", pymongo.version
	for bus in buses:
		queue=queue_sender.Queue(bus['_id'])

		for settings in items.find({'time_repeat':{'$exists': True}}):
			Timer(settings['time_repeat'], Sheduler, args=(int(settings['time_repeat']), settings['_id'], queue, bus,)).start()

		threading.Thread(target=Get_Queue, args=(queue,)).start()