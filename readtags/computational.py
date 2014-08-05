# -*- coding: utf-8 -*-
import time, redis, datetime
from config_project import *
from datetime import datetime

class Computational():
	result, status = None, None

	def __call__(self, request):
		# ID группы, прописанной у устройства
		g_id = str(request[0][0])

		def get_group_id(env):
			return str(items.find_one({'type':'group','environment':env})['_id'])

		sum_dv=0
		sum_ds=0
		
		# Выбираем нужные теги
		tags=items.find({"type":"tag", "$and":[{'groups':{'$in':[g_id]}}, {'groups':{'$in':[get_group_id('all_dutyevye'),get_group_id('all_mmt'),get_group_id('all_dymosos')]}}]})
		# Температура пп за котлом. Вытаскиваем из редиса. Если нет значения - не считаем ничего.
		try:
			qpp=items.find_one({'type':'tag',"$and":[{'groups':{'$in':[g_id]}}, {'groups':{'$in':[get_group_id('all_Q_pp_after_KA')]}}]})['_id']
			Qpp=float(r.hget(qpp, 'value'))
		except:
			Qpp = None

		# Получаем 20 последних значений тега.
		for tag in tags:
			try:
				last_20_values=eval(r.hget(str(tag['_id']), 'list_values'))
			except:
				last_20_values=[]

			if len(last_20_values)>1 and float(last_20_values[-1]['value'])>0:
				dvalue = float(last_20_values[-1]['value'])-float(last_20_values[0]['value'])
				dtime = float(last_20_values[-1]['time'])-float(last_20_values[0]['time'])
			elif len(last_20_values)==1 and float(last_20_values[0]['value'])>0:
				dvalue = 0
				dtime = 1
			else:
				dvalue = 0
				dtime = 1
			
			if get_group_id('all_dutyevye') in tag['groups']:
				sum_dv = sum_dv+dvalue/dtime*3600
			elif get_group_id('all_dymosos') in tag['groups']:
				sum_ds = sum_ds+dvalue/dtime*3600

			if Qpp:
				sum_div_qpp={
					'sum_dv':sum_dv/Qpp,
					'sum_ds':sum_ds/Qpp,
					'sum_dv_ds':sum_dv/Qpp+sum_ds/Qpp,
				}
				self.status='Ok'
			else:
				sum_div_qpp={
					'sum_dv':None,
					'sum_ds':None,
					'sum_dv_ds':None
				}
				self.status=u'Нет данных о Q пп за котлом'
			
			result={}
			tags4save=['sum_dv','sum_ds','sum_dv_ds']
			for tag4save in tags4save:
				if sum_div_qpp[tag4save] is not None:
					result[tag4save] = sum_div_qpp[tag4save]
				else:
					result[tag4save] = "Error"

		self.result=result

		return {'status':self.status, 'result':self.result}