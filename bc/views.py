# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
import string
import random
from models import *
from myforms import *
from django.http import HttpResponseRedirect, HttpRequest
from django import forms
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import os, urlparse, sys, datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.mail import send_mail
import base64
from xml.dom.minidom import *
import httplib, time
import mimetypes, json
import collections
import datetime, re, math
from datetime import datetime,timedelta
import md5
import serial
import threading
import subprocess
import Pyro4

sys.path.append("/home/root2/mptt/readtags")
from config_project import *

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

def custom_proc(request):
	gsettings=global_settings.find_one()
	connection.end_request()
	return{
        'global_settings': gsettings
    }

def Test(request):
	if request.method == 'POST':
		form = TestF(request.POST)
		if form.is_valid():
			f=form.save(commit=False)
			sotrudnik=Sotrudnik.objects.get(id = int(request.POST['sotrudnik']))
			f.sotrudnik=sotrudnik
			# oborudovanie=Oborudovanie.objects.get(id = int(request.POST['oborudovanie']))
			# f.oborudovanie=oborudovanie
			# f.save()
			f.save()
			return HttpResponseRedirect('')
	else:
		form = TestF()

	sotr=Sotrudnik.objects.all()
		
	return render_to_response("addtask.html", {'form':form, "sotr":sotr}, context_instance=RequestContext(request, processors=[custom_proc]))

def Ttc(request):
	return render_to_response("ttc_show.html", context_instance=RequestContext(request))

def ShowTtc(request):
	type_coal=items.find({'manual':{'$exists': True}, 'type':'group'})

	def get_group_id(env):
		return str(items.find_one({'type':'group','environment':env})['_id'])

	def GetRedisVal(tagid):
		if 'value' in r.hgetall(tagid):
			return r.hgetall(tagid)
		else:
			r.hmset(tagid, {'time':time.time(), 'value':0})
			GetRedisVal(tagid)
			

	def GetRedisValPlow(ka,lk,group=None):
		plows=[]
		tags=items.find({'type':'tag',"$and":[{'groups':{'$in':[get_group_id(ka)]}}, {'groups':{'$in':[get_group_id(lk)]}}, {'groups':{'$in':[get_group_id(group)]}}]}).sort('channel', 1)
		for tag in tags:
			plows.append(GetRedisVal(str(tag['_id'])))
		return plows


	# Весы 3А
	v3a_33=GetRedisVal('532785ce080b372d7ad15598')
	v3a_17=GetRedisVal('532786e2080b372d7ad15599')
	v3a_23=GetRedisVal('532786e3080b371bd1202647')

	# Весы 3Б
	v3b_33=GetRedisVal('532787cc080b372d7ad1559b')
	v3b_17=GetRedisVal('532787cc080b372d7ad1559e')
	v3b_23=GetRedisVal('532787cc080b372d7ad1559f')

	# Данные по котлам смена/сутки
	ka1_change=GetRedisVal('532a22de080b3753b403a989')
	ka1_day=GetRedisVal('532a5b67080b374bdeff4cda')
	ka2_change=GetRedisVal('532a5bb4080b374bdeff4cdb')
	ka2_day=GetRedisVal('532a5bef080b374bdeff4cdc')
	ka3_change=GetRedisVal('532a5c99080b374bdeff4cdd')
	ka3_day=GetRedisVal('532a5c9d080b374bdeff4cde')
	ka4_change=GetRedisVal('532a5dd0080b374bdeff4cdf')
	ka4_day=GetRedisVal('532a5dd2080b374bdeff4ce0')
	ka5_change=GetRedisVal('532a5f1e080b374bdeff4ce1')
	ka5_day=GetRedisVal('532a5f1e080b3745bcdb4532')
	ka6_change=GetRedisVal('532a601f080b3745bcdb4534')
	ka6_day=GetRedisVal('532a6017080b3745bcdb4533')
	ka7_change=GetRedisVal('532a6084080b374bdeff4ce2')
	ka7_day=GetRedisVal('532a6085080b3745bcdb4535')
	ka8_change=GetRedisVal('532a60f8080b374bdeff4ce3')
	ka8_day=GetRedisVal('532a60f8080b3745bcdb4536')
	ka9_change=GetRedisVal('532a615f080b3745bcdb4537')
	ka9_day=GetRedisVal('532a615f080b374bdeff4ce4')
	ka10_change=GetRedisVal('532a6218080b374bdeff4ce5')
	ka10_day=GetRedisVal('532a6218080b3745bcdb4538')
	ka11_change=GetRedisVal('532a62ff080b374bdeff4ce6')
	ka11_day=GetRedisVal('532a6300080b3745bcdb4539')
	ka12_change=GetRedisVal('532a63a7080b374bdeff4ce7')
	ka12_day=GetRedisVal('532a63aa080b374bdeff4ce8')
	ka13_change=GetRedisVal('532a63fe080b374bdeff4ce9')
	ka13_day=GetRedisVal('532a63ff080b3745bcdb453a')

	change_summ=float(ka1_change['value'])+float(ka2_change['value'])+float(ka3_change['value'])+float(ka4_change['value'])+float(ka5_change['value'])+float(ka6_change['value'])+float(ka7_change['value'])+float(ka8_change['value'])+float(ka9_change['value'])+float(ka10_change['value'])+float(ka11_change['value'])+float(ka12_change['value'])+float(ka13_change['value'])
	day_summ=float(ka1_day['value'])+float(ka2_day['value'])+float(ka3_day['value'])+float(ka4_day['value'])+float(ka5_day['value'])+float(ka6_day['value'])+float(ka7_day['value'])+float(ka8_day['value'])+float(ka9_day['value'])+float(ka10_day['value'])+float(ka11_day['value'])+float(ka12_day['value'])+float(ka13_day['value'])

	# Плужки 4А
	ka1_4a=GetRedisValPlow('ka-1','ttc_lk_4a','ttc_plug')
	ka2_4a=GetRedisValPlow('ka-2','ttc_lk_4a','ttc_plug')
	ka3_4a=GetRedisValPlow('ka-3','ttc_lk_4a','ttc_plug')
	ka4_4a=GetRedisValPlow('ka-4','ttc_lk_4a','ttc_plug')
	ka5_4a=GetRedisValPlow('ka-5','ttc_lk_4a','ttc_plug')
	ka6_4a=GetRedisValPlow('ka-6','ttc_lk_4a','ttc_plug')
	ka7_4a=GetRedisValPlow('ka-7','ttc_lk_4a','ttc_plug')
	ka8_4a=GetRedisValPlow('ka-8','ttc_lk_4a','ttc_plug')
	ka9_4a=GetRedisValPlow('ka-9','ttc_lk_4a','ttc_plug')
	ka10_4a=GetRedisValPlow('ka-10','ttc_lk_4a','ttc_plug')
	ka11_4a=GetRedisValPlow('ka-11','ttc_lk_4a','ttc_plug')
	ka12_4a=GetRedisValPlow('ka-12','ttc_lk_4a','ttc_plug')
	ka13_4a=GetRedisValPlow('ka-13','ttc_lk_4a','ttc_plug')

	# Плужки 4Б
	ka1_4b=GetRedisValPlow('ka-1','ttc_lk_4b','ttc_plug')
	ka2_4b=GetRedisValPlow('ka-2','ttc_lk_4b','ttc_plug')
	ka3_4b=GetRedisValPlow('ka-3','ttc_lk_4b','ttc_plug')
	ka4_4b=GetRedisValPlow('ka-4','ttc_lk_4b','ttc_plug')
	ka5_4b=GetRedisValPlow('ka-5','ttc_lk_4b','ttc_plug')
	ka6_4b=GetRedisValPlow('ka-6','ttc_lk_4b','ttc_plug')
	ka7_4b=GetRedisValPlow('ka-7','ttc_lk_4b','ttc_plug')
	ka8_4b=GetRedisValPlow('ka-8','ttc_lk_4b','ttc_plug')
	ka9_4b=GetRedisValPlow('ka-9','ttc_lk_4b','ttc_plug')
	ka10_4b=GetRedisValPlow('ka-10','ttc_lk_4b','ttc_plug')
	ka11_4b=GetRedisValPlow('ka-11','ttc_lk_4b','ttc_plug')
	ka12_4b=GetRedisValPlow('ka-12','ttc_lk_4b','ttc_plug')
	ka13_4b=GetRedisValPlow('ka-13','ttc_lk_4b','ttc_plug')


	# Переключатель типа ленты
	# Узел пересыпки 3Б
	_3b_to_lk4a=GetRedisVal('532b8858080b374f3055627e')
	_3b_to_lk4b=GetRedisVal('532b8858080b374f3055627f')

	# Переключатель типа ленты
	# Узел пересыпки 3А
	_3a_to_lk4a=GetRedisVal('532b8858080b374f3055627b')
	_3a_to_lk4b=GetRedisVal('532b8858080b374f3055627c')

	# Определение работающего конвеера
	lk_4a=GetRedisVal('532b8400080b374d97447afb')
	lk_4b=GetRedisVal('532b8400080b374d97447afc')

	# Определение работающих весов
	lk_3a=GetRedisVal('532b83ff080b374d97447af9')
	lk_3b=GetRedisVal('532b83ff080b374d97447afa')

	# Расход питьевой воды
	q_pv_east=GetRedisVal('528d8d8f080b374ccb3f6450')
	q_pv_west=GetRedisVal('528d8d8e080b374ccb3f644e')


	# Очередь угля
	# queue=GetRedisVal('queue_coal')

	# Активная мощность
	sum_pow=GetRedisVal('521d744a76c8150e48003f88')

	return render_to_response("ttc.html", {
		# 'queue':queue,
		'sum_pow':sum_pow,
		'change_summ':change_summ,
		'day_summ':day_summ,
		'q_pv_east':q_pv_east,
		'q_pv_west':q_pv_west,
		'lk_3a':lk_3a,
		'lk_3b':lk_3b,
		'lk_4a':lk_4a,
		'lk_4b':lk_4b,
		'3a_to_lk4b':_3a_to_lk4b,
		'3a_to_lk4a':_3a_to_lk4a,
		'3b_to_lk4b':_3b_to_lk4b,
		'3b_to_lk4a':_3b_to_lk4a,
		'type_coal':type_coal,
		'v3a_33':v3a_33,
		'v3a_17':v3a_17,
		'v3a_23':v3a_23,
		'v3b_33':v3b_33,
		'v3b_17':v3b_17,
		'v3b_23':v3b_23,
		'ka1_4a':ka1_4a,
		'ka2_4a':ka2_4a,
		'ka3_4a':ka3_4a,
		'ka4_4a':ka4_4a,
		'ka5_4a':ka5_4a,
		'ka6_4a':ka6_4a,
		'ka7_4a':ka7_4a,
		'ka8_4a':ka8_4a,
		'ka9_4a':ka9_4a,
		'ka10_4a':ka10_4a,
		'ka11_4a':ka11_4a,
		'ka12_4a':ka12_4a,
		'ka13_4a':ka13_4a,
		'ka1_4b':ka1_4b,
		'ka2_4b':ka2_4b,
		'ka3_4b':ka3_4b,
		'ka4_4b':ka4_4b,
		'ka5_4b':ka5_4b,
		'ka6_4b':ka6_4b,
		'ka7_4b':ka7_4b,
		'ka8_4b':ka8_4b,
		'ka9_4b':ka9_4b,
		'ka10_4b':ka10_4b,
		'ka11_4b':ka11_4b,
		'ka12_4b':ka12_4b,
		'ka13_4b':ka13_4b,
		'ka1_change':ka1_change,
		'ka1_day':ka1_day,
		'ka2_change':ka2_change,
		'ka2_day':ka2_day,
		'ka3_change':ka3_change,
		'ka3_day':ka3_day,
		'ka4_change':ka4_change,
		'ka4_day':ka4_day,
		'ka5_change':ka5_change,
		'ka5_day':ka5_day,
		'ka6_change':ka6_change,
		'ka6_day':ka6_day,
		'ka7_change':ka7_change,
		'ka7_day':ka7_day,
		'ka8_change':ka8_change,
		'ka8_day':ka8_day,
		'ka9_change':ka9_change,
		'ka9_day':ka9_day,
		'ka10_change':ka10_change,
		'ka10_day':ka10_day,
		'ka11_change':ka11_change,
		'ka11_day':ka11_day,
		'ka12_change':ka12_change,
		'ka12_day':ka12_day,
		'ka13_change':ka13_change,
		'ka13_day':ka13_day,
		}, context_instance=RequestContext(request, processors=[custom_proc]))

def Change_Coal(request,type_coal):
	items.update({'manual':{'$exists': True}, 'type':'group', 'manual':1},{"$set":{'manual':0}})
	items.update({'manual':{'$exists': True}, 'type':'group', 'environment':type_coal},{"$set":{'manual':1}})

def Kill(request):
	project=global_settings.find_one({'pid': {'$exists': True}})['pid']
	# coal=global_settings.find_one({'coal_pid': {'$exists': True}})['coal_pid']

	# os.kill(int(coal), 9)
	os.kill(int(project), 9)

	subprocess.Popen(['python', r'/home/root2/mptt/readtags/test_read_tags.py'])
	# subprocess.Popen(['python', r'/home/root2/mptt/readtags/computational_vesi.py'])
	
	if request.GET.get('path'):
		return HttpResponseRedirect(request.GET.get('path'))
	else:
		return HttpResponseRedirect('/')

@login_required
def ShowMain(request):
	def rec_del(did):
		childrens=items.find({'parent':ObjectId(did)})
		if childrens:
			for child in childrens:
				rec_del(str(child["_id"]))
		else:
			items.remove({'_id':ObjectId(did)})
		items.remove({"$or":[{'_id':ObjectId(did)}, {"parent":ObjectId(did)}]})


	if request.GET.get('off'):
		items.update({"_id" :ObjectId(request.GET.get('off'))},{"$set":{'interview':False}})
		return HttpResponseRedirect('#_'+str(request.GET.get('off')))

	elif request.GET.get('on'):
		items.update({"_id" :ObjectId(request.GET.get('on'))},{"$set":{'interview':True}})
		return HttpResponseRedirect('#_'+str(request.GET.get('on')))
	
	elif request.GET.get('del'):
		rec_del(request.GET.get('del'))
		return HttpResponseRedirect('?')
		
	tree=items.find({'type':'bus'})
	settings_tree=items.find({'type':'settings'})

	connection.end_request()

	return render_to_response("index.html",{'tree':tree,'settings_tree':settings_tree}, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def AddNode(request,parent=None):
	if parent:
		current_parrent=items.find_one({'_id':ObjectId(parent)})
	else:
		current_parrent=None
		
	if request.method == 'POST':
		node=({request.POST['field_name']:eval(request.POST['field_value']), 'interview': False, 'name':'Укажите имя', 'parent':ObjectId(parent)})
		items.insert(node)
		return HttpResponseRedirect('/#_'+str(parent))
	return render_to_response("add.html", {'current_parrent':current_parrent}, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def CloneNode(request,target):
	current_target=items.find_one({'_id':ObjectId(target)})
	child_of_target=items.find({'parent':ObjectId(target)})

	current_target['_id'] = ObjectId()
	current_target['interview'] = False
	current_target['name'] = current_target['name']+'_clone'
	items.insert(current_target)

	for child in child_of_target:
		child['_id']=ObjectId()
		child['parent']=ObjectId(current_target['_id'])
		child['interview']=False
		items.insert(child)
	return HttpResponseRedirect('/')


def CurrentTag(request):
	subprocess.Popen(['python', '/home/root2/mptt/bc/build_charts.py', request.GET.get('tag')])
	current_tag=r.hgetall(request.GET.get('tag'))

	return render_to_response("currenttag.html", {'current_tag':current_tag}, context_instance=RequestContext(request, processors=[custom_proc]))


def Arms(request,armid):
	current_arm=items.find_one({'_id':ObjectId(armid)})
	return render_to_response("currentarm.html", {'current_arm':current_arm}, context_instance=RequestContext(request, processors=[custom_proc]))

def Arch(request,device):
	if request.method == 'POST':
		subprocess.Popen(['python', '/home/root2/mptt/readtags/read_arch_tags.py', "1_d_repeat", request.POST['date'], device])
	device=items.find_one({"type":"device", "_id":ObjectId(device)})
	return render_to_response("read_arch.html", {'device':device}, context_instance=RequestContext(request, processors=[custom_proc]))

# Вычитывание значения канала с прибора
def Value(request,device):
	device=items.find_one({"type":"device", "_id":ObjectId(device)})
	if request.method == 'POST':
		todo=Pyro4.Proxy("PYRO:todo@localhost:5150")
		bus=items.find_one({"type":"bus", "_id":ObjectId(device['parent'])})
		tags_hash={}
		tags_hash['tagname']=[request.POST['channel'],request.POST['parameter']]
		# Генерируем случайное имя для записи в редис
		tmp_name=str(ObjectId())
		mrequest=[device['dad'], device['sad'], tags_hash, bus['port_address'], bus['port_baudrate'], bus['timeout'], tmp_name, 'read_value']
		todo.add(bus['_id'], mrequest, 1)

		# Ждем, пока не будет ответа в редисе
		def get_response():
			result = r.hgetall(tmp_name)
			if result:
				return result
			else:
				return None

		result = get_response()

		while result is None:
			result = get_response()
	else:
		result=u"Укажите канал и параметр"
	return render_to_response("read_value.html", {'device':device, 'result':result}, context_instance=RequestContext(request, processors=[custom_proc]))

# Запись значения в канал прибора
def wValue(request, device):
	device=items.find_one({"type":"device", "_id":ObjectId(device)})
	if request.method == 'POST':
		todo=Pyro4.Proxy("PYRO:todo@localhost:5150")
		bus=items.find_one({"type":"bus", "_id":ObjectId(device['parent'])})
		tags_hash={}
		tags_hash['tagname']=[request.POST['channel'],request.POST['parameter'],request.POST['value']]
		# Генерируем случайное имя для записи в редис
		tmp_name=str(ObjectId())
		mrequest=[device['dad'], device['sad'], tags_hash, bus['port_address'], bus['port_baudrate'], bus['timeout'], tmp_name, 'write_value']
		todo.add(bus['_id'], mrequest, 1)

		# Ждем, пока не будет ответа в редисе
		def get_response():
			result = r.hgetall(tmp_name)
			if result:
				return result
			else:
				return None

		result = get_response()

		while result is None:
			result = get_response()
	else:
		result=u"Укажите канал, параметр и значение"
	return render_to_response("write_value.html", {'device':device, 'result':result}, context_instance=RequestContext(request, processors=[custom_proc]))

def CurrArm(request,armid):
	unsorted_dict={}
	sorted_groups=[]

	arm = items.find_one({"type":"arm",'_id':ObjectId(armid)})
	groups = items.find({"type":"group", "_id":{"$in":[ObjectId(group) for group in arm['groups']]}})
	for group in arm['groups']:
		sort_order = sorted_c.find_one({"gid":ObjectId(armid), "tid":ObjectId(group)},{"order":1})
		if sort_order:
			unsorted_dict[group]=int(sort_order["order"])
		else:
			unsorted_dict[group]=999
	sorted_dict = collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda t: t[1]))

	for key, value in sorted_dict.items():
		try:
			sorted_groups.append(filter(lambda g: g["_id"] == ObjectId(key), groups.clone())[0])
		except:
			# Пустые группы. Выяснить.
			pass

	return render_to_response("sort_arm.html", {'arm':arm, 'groups':sorted_groups}, context_instance=RequestContext(request, processors=[custom_proc]))


def CurrGroup(request,group):
	if request.GET.get('del'):
		items.update({'_id':ObjectId(request.GET.get('del'))},{"$pull":{"groups":group}})

	tags = items.find({"type":"tag",'groups':{'$in':[str(group)]}})
	unsorted_dict={}
	sorted_tags=[]
	for tag in tags:
		sort_order = sorted_c.find_one({"gid":ObjectId(group), "tid":ObjectId(str(tag["_id"]))},{"order":1})
		if sort_order:
			unsorted_dict[str(tag["_id"])]=int(sort_order["order"])
		else:
			unsorted_dict[str(tag["_id"])]=999
	sorted_dict = collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda t: t[1]))

	for key, value in sorted_dict.items():
		sorted_tags.append(filter(lambda g: g["_id"] == ObjectId(key), tags.clone())[0])

	group=items.find_one({"_id":ObjectId(group)},{'name':1, '_id':1})
	return render_to_response("currentgroup.html", {'tags':sorted_tags,'group':group}, context_instance=RequestContext(request, processors=[custom_proc]))

def AllArms(request):
	arms=items.find({"type":"arm"})
	current_arms=reports.find({"current":1})
	if request.method == 'POST':
		return HttpResponseRedirect('/eco/%s' % ",".join(sorted(request.POST.keys())))

	return render_to_response("arms.html", {'arms':arms, 'current_arms':current_arms}, context_instance=RequestContext(request, processors=[custom_proc]))

def Buses(request,busid): 
	def rec_del(did):
		childrens=items.find({'parent':ObjectId(did)})
		if childrens:
			for child in childrens:
				rec_del(str(child["_id"]))
		else:
			items.remove({'_id':ObjectId(did)})
		items.remove({"$or":[{'_id':ObjectId(did)}, {"parent":ObjectId(did)}]})
				
	if request.GET.get('off'):
		items.update({"_id" :ObjectId(request.GET.get('off'))},{"$set":{'interview':False}})
		return HttpResponseRedirect('#_'+str(request.GET.get('off')))

	elif request.GET.get('on'):
		items.update({"_id" :ObjectId(request.GET.get('on'))},{"$set":{'interview':True}})
		return HttpResponseRedirect('#_'+str(request.GET.get('on')))
	
	elif request.GET.get('del'):
		rec_del(request.GET.get('del'))
		return HttpResponseRedirect('?')

	current_bus=items.find_one({'_id':ObjectId(busid)})
	connection.end_request()	

	return render_to_response("currentbus.html", {'current_bus':current_bus}, context_instance=RequestContext(request, processors=[custom_proc]))

def ShowSettings(request):
	return render_to_response("settings.html", context_instance=RequestContext(request, processors=[custom_proc]))


def Checked_state(request):
	if request.GET.get('tags'):
		tags=request.GET.get('tags').split(',')
		for tag in tags:
			r.hmset(tag,{'state_checked':True})


def Errors(request):
	tags_status={}
	tags=items.find({'type':'tag', 'interview':True})

	def get_interview(parent):
		device = items.find_one({'_id':ObjectId(parent)})
		bus = items.find_one({'_id':ObjectId(device['parent'])})
		return {'device_interview':device['interview'], 'bus_interview':bus['interview']}	

	for tag in tags:
		interview = get_interview(tag['parent'])
		if interview['device_interview'] is True and interview['bus_interview'] is True:
			check_tag_update(str(tag['_id']))
			tag_info=r.hgetall(str(tag['_id']))
			if int(tag_info['status']) != 0:
				tags_status[str(tag['_id'])] = tag_info
	return render_to_response("errors.html", {'tags_status':tags_status}, context_instance=RequestContext(request))

def ShowErrors(request):
	return render_to_response("show_errors.html", context_instance=RequestContext(request))

def Sorted(request):
	if request.GET.get('order') and request.GET.get('group'):
		tags=request.GET.get('order').split(',')
		for tag in tags[0:-1]:
			sorted_c.update({"gid":ObjectId(request.GET.get('group')),'tid':ObjectId(tag.split(':')[0])},{"$set":{'order':tag.split(':')[1]}}, True)
	return HttpResponseRedirect('/eco/')

import error_collector
e_collection=error_collector.Error_Collection()
def MyData(request):
	if request.GET.get('tags'):
		load_tags={}
		tags=request.GET.get('tags').split(',')
		#Выбираем значения приборов
		for tag in tags:
			load_tags[tag]=r.hgetall(tag)

		sorted_tags = collections.OrderedDict(sorted(load_tags.items()))
		return render_to_response("mydata.html", {'load_tags':sorted_tags}, context_instance=RequestContext(request))

	elif request.GET.get('groups'):
		groups=request.GET.get('groups').split(',')[:-1]
		tags_status={}
		gid=items.find({'_id':{'$in':[ObjectId(group) for group in groups]}},{'_id':1,'name':1})
		groups_of_tag = gid.clone()
		unsorted_dict={}
		arm = items.find_one({"_id":ObjectId(request.GET.get('armid'))})
		if 'errors' in arm and arm['errors'] is True:
			show_errors = True
		else:
			show_errors = False

		# Сортируем блочки
		for group in gid.clone():
			sort_order=sorted_c.find_one({"gid":ObjectId(request.GET.get('armid')), "tid":group['_id']})
			if sort_order:
				unsorted_dict[group['name']]=int(sort_order["order"])
			else:
				unsorted_dict[group['name']]=999
		groups_load_tags = collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda t: t[1]))

		def get_interview(parent):
			device = items.find_one({'_id':ObjectId(parent)})
			bus = items.find_one({'_id':ObjectId(device['parent'])})
			return {'device_interview':device['interview'], 'bus_interview':bus['interview']}

		for group in groups_of_tag:
			tags=items.find({'type':'tag', 'interview':True, 'groups':{'$in':[str(group['_id'])]}},{'_id':1, 'parent':1})
			load_tags=collections.OrderedDict()
			unsorted_dict={}

			# Получаем данные о сортировке тегов в блочках
			for tag in tags:
				sort_order = sorted_c.find_one({"gid":ObjectId(str(group["_id"])), "tid":ObjectId(str(tag["_id"]))},{"order":1})
				if sort_order:
					unsorted_dict[str(tag["_id"])]=[sort_order["order"], str(tag["parent"])]
				else:
					unsorted_dict[str(tag["_id"])]=[999, str(tag["parent"])]

			sorted_dict = collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda t: t[1][0]))

			for tagid, value in sorted_dict.items():
				interview = get_interview(value[1])
				if interview['device_interview'] is True and interview['bus_interview'] is True:
					check_tag_update(tagid)
					tag_info=r.hgetall(tagid)
					load_tags[tagid]=tag_info
					if tag_info.has_key('state_checked') and tag_info['state_checked'] == 'False' and int(tag_info['status']) != 0:
						tags_status[tagid] = tag_info

			groups_load_tags[group['name']]=load_tags
			tags.close()

		connection.end_request()
		return render_to_response("mydata.html", {'show_errors':show_errors ,'groups_load_tags':groups_load_tags, 'tags_status':tags_status}, context_instance=RequestContext(request))


def GetTags(request):
	all_groups=items.find({'environment': {'$exists': True}})
	return render_to_response("gettags.html", {'all_groups':all_groups}, context_instance=RequestContext(request))

def ShowDrags(request, tagid):
	tag=items.find_one({"type":"tag","_id":ObjectId(tagid)})
	buses=items.find({'type':'bus', 'interview':True})
	devices=items.find({'type':'device', 'interview':True})
	tags=items.find({'type':'tag', 'interview':True})
	return render_to_response("drags.html", {'tagid':tagid, 'tag':tag, 'buses':buses, 'devices':devices, 'tags':tags}, context_instance=RequestContext(request))

def Drags(request):
	buses=items.find({'type':'bus', 'interview':True})
	devices=items.find({'type':'device', 'interview':True})
	tags=items.find({'type':'tag', 'interview':True})
	return render_to_response("drags.html", {'buses':buses, 'devices':devices, 'tags':tags}, context_instance=RequestContext(request))

def SelectChildren(request, parentid):
	childrens=items.find({'parent':ObjectId(parentid), 'interview':True})
	return render_to_response("for_select.html", {'childrens':childrens}, context_instance=RequestContext(request))

# JSON для графика одного тега с автообновлением
def CurrentValuesForGraphAutoupdate(request, tagid):
	tag = r.hgetall(tagid)
	errors=[]
	vals_and_times=[]
	server_time = time.time()

	if tag['value'] == 'Error':
		# Вытаскиваем последнее нормальной значение
		ts = datetime.now()
		collection = datetime(ts.year,ts.month,ts.day,ts.hour)
		data = db_arch[collection.strftime("%Y-%m-%d %H:%M:%S")]
		tag_from_mongo = data.find({"tag_id":ObjectId(tagid), 'value':{'$ne':'Error'}}).limit(1).sort("_id", -1)

		vals_and_times=[{
			"description": json.loads(tag['state'])['e_type'],
			"value": tag_from_mongo[0]['value'],
			"time": datetime.fromtimestamp(float(tag['time'])).strftime("%d.%m.%Y %H:%M:%S")
		}]
		# Время для окончания ошибки
		if float(tag['time']) <= server_time:
			time_to_err_end=server_time
		else:
			time_to_err_end=tag['time']

		errors=[{
			'category': datetime.fromtimestamp(float(tag_from_mongo[0]['time'])).strftime("%d.%m.%Y %H:%M:%S"),
			'toCategory': datetime.fromtimestamp(float(time_to_err_end)).strftime("%d.%m.%Y %H:%M:%S"),
			'lineColor': "#CC0000",
			'lineAlpha': 1,
			'fillAlpha': 0.1,
			'fillColor': "#CC0000",
			'dashLength': 2,
			'inside': True,
			'labelRotation': 90,
			'label': json.loads(tag['state'])['e_type']			
		}]
	else:
		vals_and_times=[{
			"description": round(float(tag['value']),2),
			"value": round(float(tag['value']),2),
			"time": datetime.fromtimestamp(float(tag['time'])).strftime("%d.%m.%Y %H:%M:%S")
		}]

	result={'vals_and_times':vals_and_times, 'errors':errors, 'server_time':server_time}
	result=json.dumps(result)
	return render_to_response("get_last_value_for_graph.html", {'result':result}, context_instance=RequestContext(request, processors=[custom_proc]))

# JSON для графика одного тега
def CurrentValuesForGraph(request, tagid):
	vals=[]
	times=[]
	errors=[]
	vals_and_times=[]
	collections=[]

	if request.GET.get('start_date') and request.GET.get('end_date'):
		start = datetime.strptime(request.GET.get('start_date'), '%d-%m-%Y')
		start_read=time.mktime(start.timetuple())
		end = datetime.strptime(request.GET.get('end_date'), '%d-%m-%Y')
		for collection in db_arch.collection_names():
			try:
				collection_range = datetime.strptime(collection, '%Y-%m-%d %H:%M:%S')
				if start <= collection_range <= end:
					collections.append(collection_range)
			except:
				pass
	else:
		ts=datetime.now()
		delta = timedelta(hours=1)
		new_period=ts-delta
		prev_collection=datetime(new_period.year,new_period.month,new_period.day,new_period.hour)
		start_read=time.mktime(new_period.timetuple())
	
		for collection in db_arch.collection_names():
			try:
				collection_range = datetime.strptime(collection, '%Y-%m-%d %H:%M:%S')
				if collection_range >= prev_collection:
					collections.append(collection_range)
			except:
				pass


	for current_collection in collections:
		data=db_arch[str(current_collection)]
		tag_values=data.find({'tag_id':ObjectId(tagid), 'time':{'$gte':start_read}},{'value':1,'time':1, 'state':1, '_id':0})

		for tag in tag_values:
			try:
				# Хорошее значение
				vals.append(round(float(tag['value']),2))
				times.append(datetime.fromtimestamp(tag['time']).strftime("%d.%m.%Y %H:%M:%S"))
			except:
				# Ошибка. Пишем предыдущее значение и текущую дату.
				if vals:
					vals.append(vals[-1])
					times.append(datetime.fromtimestamp(tag['time']).strftime("%d.%m.%Y %H:%M:%S"))
					
					tag_e={}
					tag_e['category']=times[-2]
					tag_e['toCategory']=datetime.fromtimestamp(tag['time']).strftime("%d.%m.%Y %H:%M:%S")
					tag_e['lineColor']="#CC0000"
					tag_e['lineAlpha']=1
					tag_e['fillAlpha']=0.2
					tag_e['fillColor']="#CC0000"
					tag_e['dashLength']=2
					tag_e['inside']=True
					tag_e['labelRotation']=90
					tag_e['label']=json.loads(tag['state'])['e_type']
					errors.append(tag_e)

	# Находим максимум и минимум
	def find_min_max(val, time):
		tag_v={}

		if val==max(vals):
			tag_v['value']=val
			tag_v['time']=time
			tag_v['bullet']="triangleUp"
			tag_v['fillColors']="#E3094A"
			tag_v['bulletBorderColor']="#E3094A"
			tag_v['description']='Максимум: %s' % val
		elif val==min(vals):
			tag_v['value']=val
			tag_v['time']=time
			tag_v['bullet']='triangleDown'
			tag_v['fillColors']='#00A6FF'
			tag_v['bulletBorderColor']='#00A6FF'
			tag_v['description']='Минимум: %s' % val
		else:
			tag_v['value']=val
			tag_v['time']=time
			tag_v['description']=val

		return tag_v

	for h in map(find_min_max, vals, times):
		vals_and_times.append(h)

	connection.end_request()
	result={'vals_and_times':vals_and_times, 'errors':errors}
	result=json.dumps(result)
	return render_to_response("get_tag_by_id.html", {'result':result, "dates":collections}, context_instance=RequestContext(request, processors=[custom_proc]))


@login_required
def EditNode(request,target=None):
	if request.method == 'POST':
		try:
			items.update({"_id" :ObjectId(target)},{"$set":{request.POST['field_name']:eval(request.POST['field_value'])}})
		except:
			items.update({"_id" :ObjectId(target)},{"$set":{request.POST['field_name']:request.POST['field_value']}})
		return HttpResponseRedirect('')
	if request.GET.get('del'):
		items.update({'_id':ObjectId(target)},{"$unset":{request.GET.get('del'):1}})
		
	result=items.find_one({'_id':ObjectId(target)})
	return render_to_response("edit.html", {'result':result}, context_instance=RequestContext(request, processors=[custom_proc]))


def Groups(request,tid=None):
	groups=items.find({'type':'group'}).sort('name',1)
	tag=items.find_one({'_id':ObjectId(tid)})
	if request.method == 'POST':
		items.update({"_id" :ObjectId(tid)},{"$set":{'groups':request.POST.keys()}})
		return HttpResponseRedirect('')
	# groups.close()
	return render_to_response("groups.html", {'groups':groups, 'tag':tag}, context_instance=RequestContext(request, processors=[custom_proc]))


def AddReports(request):
	if request.GET.get('del'):
		cells.remove({"parent":ObjectId(request.GET.get('del'))})
		reports.remove({"_id":ObjectId(request.GET.get('del'))})
		return HttpResponseRedirect('/reports/')

	if request.method == 'POST':
		node=({'report_name':request.POST['report_name'], 'x':request.POST['rows'], 'y':request.POST['columns'], 'current':float(request.POST['report_type'])})
		reports.insert(node)
		return HttpResponseRedirect('')
	all_reports=reports.find()

	return render_to_response("add_report.html", {'all_reports':all_reports}, context_instance=RequestContext(request))

def CurrentTec2(request):
	return render_to_response("current_tec2.html", context_instance=RequestContext(request, processors=[custom_proc]))

def CurrentKa(request):
	return render_to_response("current_ka.html", context_instance=RequestContext(request, processors=[custom_proc]))

def CurrentCw(request):
	return render_to_response("current_cw.html", context_instance=RequestContext(request, processors=[custom_proc]))

def Protect(request):
	return render_to_response("protect.html", context_instance=RequestContext(request, processors=[custom_proc]))

def ProtectState(request):
	return render_to_response("protect_state.html", context_instance=RequestContext(request, processors=[custom_proc]))


# Метод для отображения схемы бойлерных
def GetTagByShortname(request):

	def GetRedisVal(shortname):
		tag = items.find_one({"short_name":shortname})
		value = r.hgetall(str(tag['_id']))['value']
		if value == 'Error':
			return value
		else:
			return round(float(value),1)

	tags={
		'1':GetRedisVal("БУ-5 Q подающ. калориф."),
		'2':GetRedisVal("БУ-1 Q подающ. трубопр."),
		'3':GetRedisVal("БУ-1 Т подающ. трубопр."),
		'4':GetRedisVal("БУ-1 Т за ОБ-1"),
		'5':GetRedisVal("БУ-1 Т обрат. трубопр."),
		'6':GetRedisVal("БУ-2 Q подающ."),
		'7':GetRedisVal("БУ-2 Т подающ. трубопр."),
		'8':GetRedisVal("БУ-2 Т за ОБ-2"),
		'9':GetRedisVal("БУ-2 Т обрат. трубопр."),
		'10':GetRedisVal("КСК ГЩУ Q трубопр ХО подп КСК"),
		'11':GetRedisVal("БУ-3 Q подающ трубопр"),
		'12':GetRedisVal("БУ-3 Т за обводом подающ трубопр"),
		'13':GetRedisVal("БУ-4 Q подающ. трубопр."),
		'14':GetRedisVal("БУ-4 Т подающ. трубопр."),
		'15':GetRedisVal("БУ-4 Т обрат. трубопр"),
		'16':GetRedisVal("БУ-5 Q подающ."),
		'17':GetRedisVal("БУ-5 Т подающ. трубопр."),
		'18':GetRedisVal("БУ-6 Т подающ. трубопр."),
		'19':GetRedisVal("БУ-6 Q подающ. трубопр."),
		'20':GetRedisVal("БУ-4 Т за ОБ-4"),
		'21':GetRedisVal("БУ-5 Т за ОБ-5"),
		'22':GetRedisVal("БУ-6 Т за ОБ-6"),
		'23':GetRedisVal("БУ-5 Т обрат. трубопр."),
		'24':GetRedisVal("БУ-6 Т обрат. трубопр."),
		'25':GetRedisVal("Город ГЩУ Q прям. 1000"),
		'26':GetRedisVal("Город ГЩУ Т прям. 1000"),
		'27':GetRedisVal("Город ГЩУ Р прям. 1000"),
		'28':GetRedisVal("КСК ГЩУ Р подающ. трубопр."),
		'29':GetRedisVal("КСК ГЩУ Т подающ. трубопр."),
		'30':GetRedisVal("КСК ГЩУ Q подающ. трубопр."),
		'31':GetRedisVal("КСК ГЩУ Р обрат. трубопр."),
		'32':GetRedisVal("КСК ГЩУ Т обрат. трубопр."),
		'33':GetRedisVal("КСК ГЩУ Q обрат. трубопр."),
		'34':GetRedisVal("НАПТС-3 Q 1 оч. "),
		'35':GetRedisVal("Город ГЩУ Р прям. 800"),
		'36':GetRedisVal("Город ГЩУ Т прям. 800"),
		'37':GetRedisVal("Город ГЩУ Q прям. 800"),
		'38':GetRedisVal("Город ГЩУ Р обрат. 800"),
		'39':GetRedisVal("Город ГЩУ Т обрат. 800"),
		'40':GetRedisVal("Город ГЩУ Q обрат. 800"),
		'41':GetRedisVal("Город ГЩУ Р обрат. 1000"),
		'42':GetRedisVal("Город ГЩУ Т обрат. 1000"),
		'43':GetRedisVal("Город ГЩУ Q обрат. 1000"),
		'44':GetRedisVal("БУ-4 Q подп. ХОВ"),
		'45':GetRedisVal("БУ-2 Т подводов ХОВ к деаэр"),
		'46':GetRedisVal("БУ-3 Т обрат. трубопр."),
		'47':GetRedisVal("БУ-1 W по магистр."),
		'48':GetRedisVal("БУ-2 W по магистр."),
		'49':GetRedisVal("КСК ГЩУ W по магистр."),
		'50':GetRedisVal("БУ-3 W по магистр."),
		'51':GetRedisVal("БУ-4 W по магистр."),
		'52':GetRedisVal("БУ-5 W по магистр."),
		'53':GetRedisVal("БУ-6 W по магистр."),
		'54':GetRedisVal("Город ГЩУ W по магистр. 1000"),
		'55':GetRedisVal("Город ГЩУ W по магистр. 800"),
		'56':GetRedisVal("БУ-4 Q трубопр. отопл."),
		'57':GetRedisVal("БУ-5 Q подающ. отопл."),
		'58':GetRedisVal("БУ-1 Q прям. на отопл."),
		'59':GetRedisVal("ПСГ W по магистр св"),
		'60':GetRedisVal("АПТС Q 2 оч."),
		'61':GetRedisVal("ПСГ Q св прямой трубопр"),
		'62':GetRedisVal("ПСГ Т св обрат трубопр"),
		'63':GetRedisVal("ПСГ Р св обрат трубопр"),
		'64':GetRedisVal("ПСГ Т св прямой трубопр"),
		'65':GetRedisVal("ПСГ Р св прямой трубопр"),
	}
	tags=json.dumps(tags)
	return render_to_response("get_tag_by_shortname.html", {'tags':tags}, context_instance=RequestContext(request, processors=[custom_proc]))

# @csrf_exempt
def GetTagByShortnameTec1(request):

	def GetRedisVal(shortname):
		tag = items.find_one({"short_name":shortname})
		value = r.hgetall(str(tag['_id']))['value']
		if value == 'Error':
			return value
		else:
			return round(float(value),1)

	tags={
		'1':GetRedisVal("Город ГЩУ Р обрат. 1000"),
		'2':GetRedisVal("Город ГЩУ Р обрат. 800"),
		'3':GetRedisVal("КСК ГЩУ Р обрат. трубопр."),
		'4':GetRedisVal("БУ-4 Q подп. ХОВ"),
		'5':GetRedisVal("Город ГЩУ Р прям. 1000"),
		'6':GetRedisVal("КСК ГЩУ Р подающ. трубопр."),
		'7':GetRedisVal("Город ГЩУ Р прям. 800"),
		'8':GetRedisVal("Город ГЩУ Q прям. 1000"),
		'9':GetRedisVal("Город ГЩУ Q обрат. 1000"),
		'10':GetRedisVal("Город ГЩУ Т прям. 1000"),
		'11':GetRedisVal("Город ГЩУ Т обрат. 1000"),
		'12':GetRedisVal("Город ГЩУ W по магистр. 1000"),
		'13':GetRedisVal("Город ГЩУ Q прям. 800"),
		'14':GetRedisVal("Город ГЩУ Q обрат. 800"),
		'15':GetRedisVal("Город ГЩУ Т прям. 800"),
		'16':GetRedisVal("Город ГЩУ Т обрат. 800"),
		'17':GetRedisVal("Город ГЩУ W по магистр. 800"),
		'18':GetRedisVal("КСК ГЩУ Q подающ. трубопр."),
		'19':GetRedisVal("КСК ГЩУ Q обрат. трубопр."),
		'20':GetRedisVal("КСК ГЩУ Т подающ. трубопр."),
		'21':GetRedisVal("КСК ГЩУ Т обрат. трубопр."),
		'22':GetRedisVal("КСК ГЩУ W по магистр."),
		'23':GetRedisVal("КСК ГЩУ Q трубопр ХО подп КСК"),
		'24':GetRedisVal("АПТС Q 2 оч."),
		'25':GetRedisVal("КСК Q ав. подп."),
	}
	tags=json.dumps(tags)
	return render_to_response("get_tag_by_shortname.html", {'tags':tags}, context_instance=RequestContext(request, processors=[custom_proc]))


def ShowBuScheme(request):
	return render_to_response("bu_scheme.html", context_instance=RequestContext(request, processors=[custom_proc]))


def CurrentBu(request):
	return render_to_response("current_bu.html", context_instance=RequestContext(request, processors=[custom_proc]))

def BuSchemeShow(request):
	return render_to_response("bu_scheme_show.html", context_instance=RequestContext(request, processors=[custom_proc]))



def CurrentTg(request):
	return render_to_response("current_tg.html", context_instance=RequestContext(request, processors=[custom_proc]))

def Ecos(request,ecoid):
	all_ka=ecoid.split(',')
	if "" in all_ka:
		all_ka.remove("")
	return render_to_response("currenteco.html", {'all_ka':all_ka}, context_instance=RequestContext(request, processors=[custom_proc]))

import test_read_tags
def Eco_ka(request):
	def get_group_id(env):
		return str(items.find_one({'type':'group','environment':env})['_id'])

	all_ka=request.GET.get('groups').split(',')
	all_ka.remove("")
	# Имя коллекции, первой за текущие сутки
	ts=datetime.now()
	start_coll = str(datetime(ts.year,ts.month,ts.day))

	for ka in all_ka:
		ka_name=items.find_one({'type':'group','environment':ka})['name']
		sum_dv=0
		sum_ds=0
		sum_mmt=0
		
		current_sum_dv=0
		current_sum_ds=0
		current_sum_mmt=0

		result_dv={}
		result_ds={}
		result_mmt={}
		# Выбираем нужные теги
		tags=items.find({"type":"tag", "$and":[{'groups':{'$in':[get_group_id(ka)]}}, {'groups':{'$in':[get_group_id('all_dutyevye'),get_group_id('all_mmt'),get_group_id('all_dymosos')]}}]})
		# Температура пп за котлом. Вытаскиваем из редиса. Если нет значения - не считаем ничего.
		try:
			qpp=items.find_one({'type':'tag',"$and":[{'groups':{'$in':[get_group_id(ka)]}}, {'groups':{'$in':[get_group_id('all_Q_pp_after_KA')]}}]})['_id']
			Qpp=float(r.hget(str(qpp), 'value'))
		except:
			Qpp = None

		# Получаем 20 последних значений тега.
		for tag in tags:
			last_20_values=eval(r.hget(str(tag['_id']), 'list_values'))
			# Первое значение тега за сутки. Если нет, делаем равным 0.
			first_value_tag=db_arch[start_coll].find_one({'tag_id':tag['_id'], "value":{"$lte":float(last_20_values[-1]['value'])}}, {'value':1, 'time':1, '_id':0})

			if first_value_tag:
				first_value=float(first_value_tag['value'])
			else:
				first_value=0


			if len(last_20_values)>1 and float(last_20_values[-1]['value'])>0:
				cvalue = float(last_20_values[-1]['value'])-first_value
				if float(last_20_values[-1]['value']) > float(last_20_values[0]['value']):
					dvalue = float(last_20_values[-1]['value'])-float(last_20_values[0]['value'])
					dtime = float(last_20_values[-1]['time'])-float(last_20_values[0]['time'])
				else:
					dvalue = float(last_20_values[-1]['value']) - first_value
					dtime = float(last_20_values[-1]['time'])-float(first_value_tag['time'])
			elif len(last_20_values)==1 and float(last_20_values[0]['value'])>0:
				cvalue = float(last_20_values[0]['value'])-first_value
				dvalue = 0
				dtime = 1
			else:
				dvalue = 0
				dtime = 1
				cvalue = 0

			
			if get_group_id('all_dutyevye') in tag['groups']:
				sum_dv = sum_dv+dvalue/dtime*3600
				result_dv[tag['name']]=dvalue/dtime*3600
				current_sum_dv=current_sum_dv+cvalue
			elif get_group_id('all_mmt') in tag['groups']:
				sum_mmt = sum_mmt+dvalue/dtime*3600
				result_mmt[tag['name']]=dvalue/dtime*3600
				current_sum_mmt=current_sum_mmt+cvalue
			elif get_group_id('all_dymosos') in tag['groups']:
				sum_ds = sum_ds+dvalue/dtime*3600
				result_ds[tag['name']]=dvalue/dtime*3600
				current_sum_ds=current_sum_ds+cvalue
	

			day_dv_ds = (sum_dv+sum_ds)*24
			day_sum_mmt = sum_mmt*24
			sum_day_mmt_ds_dv = day_dv_ds+day_sum_mmt
			
			if Qpp:
				sum_div_qpp={
					'sum_day_mmt_ds_dv':sum_day_mmt_ds_dv/Qpp,
					'day_sum_mmt':day_sum_mmt/Qpp,
					'day_dv_ds':day_dv_ds/Qpp,
					'sum_dv':sum_dv/Qpp,
					'sum_mmt':sum_mmt/Qpp,
					'sum_ds':sum_ds/Qpp,
					'sum_dv_ds':sum_dv/Qpp+sum_ds/Qpp,
				}
			else:
				sum_div_qpp={
					'sum_day_mmt_ds_dv':None,
					'day_sum_mmt':None,
					'day_dv_ds':None,
					'sum_dv':None,
					'sum_mmt':None,
					'sum_ds':None,
				}

		result_dv=collections.OrderedDict(sorted(result_dv.items()))
		result_ds=collections.OrderedDict(sorted(result_ds.items()))
		result_mmt=collections.OrderedDict(sorted(result_mmt.items()))


	return render_to_response("eco.html", {'current_sum_mmt':current_sum_mmt,'current_sum_ds':current_sum_ds,'current_sum_dv':current_sum_dv,'ka_name':ka_name, 'sum_div_qpp':sum_div_qpp, 'sum_day_mmt_ds_dv':sum_day_mmt_ds_dv, 'day_sum_mmt':day_sum_mmt, 'day_dv_ds':day_dv_ds, 'sum_dv':sum_dv, 'sum_mmt':sum_mmt, 'sum_ds':sum_ds, 'result_dv':result_dv, 'result_ds':result_ds, 'result_mmt':result_mmt, 'qpp':Qpp}, context_instance=RequestContext(request))


def EditReport(request, reportid):
	# Показываем отчет
	# log=open(r'C:\mptt\bc\log.txt','w')
	# Инфа по отчету
	report=reports.find_one({'_id':ObjectId(reportid)})
	reportx=int(report['y'])
	reporty=int(report['x'])

	if request.GET.get('show'):
		# Если в адресной строке есть дата
		if request.GET.get('date'):
			date=datetime.strptime(request.GET.get('date'), '%d-%m-%Y')
			date2select=time.mktime(date.timetuple())
		else:
			ts=datetime.now()
			delta = timedelta(days=1)
			new_period=ts-delta
			start=datetime(new_period.year,new_period.month,new_period.day)
			date2select=time.mktime(start.timetuple())

		# Матрица с конечными результатами
		matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		report_cells=cells.find({'parent':ObjectId(reportid)})

		# Матрица с формулами
		tmp_matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		report_cells_clone=report_cells.clone()
		for cell in report_cells_clone:
			cell_name=eval(cell['cell_name'])
			cell_expression=cell['cell_expression']
			tmp_matrix[cell_name[0]][cell_name[1]]=cell_expression

		# Функция вычисления значения
		def eval_expression(expression, tmp_matrix, report=None, x=None, y=None):
			expression=expression.replace(':','')
			if expression[:1]=='@':
				expression=get_tag(expression[1:], report, x, y)
				eval_expression(str(expression),tmp_matrix, report, x, y)
			try:
				result=eval(expression)
				return result
			except:
				params = re.findall(r'{[^}]+}', expression)
				for param_ in params:
					if '@' in param_:
						param=param_[2:-1]
						result=get_tag(param, report, x, y)
					else:
						param=param_.replace('{','tmp_matrix[').replace(',','][').replace('}',']')
						result=eval_expression(param, tmp_matrix, report, x, y)
					expression=expression.replace(unicode(param_),unicode(result))
				result = eval_expression(unicode(expression), tmp_matrix, report, x, y)
				return result

		def get_tag(shortname, report=None, x=None, y=None):
			tag=items.find_one({"short_name":shortname.encode("utf-8")})
			if tag:
				predecessor=average_day.find({'tag_id':ObjectId(tag["_id"]), 'start':date2select}).limit(1).sort('_id',-1)
				try:
					err_state = predecessor[0]['err_state']
					tag_value = predecessor[0]['value']
				except:
					err_state = 1
					tag_value = 0
			else:
				err_state = 1
				tag_value = 0

			if err_state == 1:
				r.hmset(reportid+str(cell_name[0])+str(cell_name[1]), {'x':cell_name[0], 'y':cell_name[1], 'color':'#e44b07'})
			else:
				r.hmset(reportid+str(cell_name[0])+str(cell_name[1]), {'x':cell_name[0], 'y':cell_name[1], 'color':'transparent'})

			return round(float(tag_value),2)


		# Получаем значения ячеек текущего отчета и отправляем в функцию, вычисляющую выражение
		for cell in report_cells:
			cell_name=eval(cell['cell_name'])
			expression=cell['cell_expression']
			# Пробуем перевести во float значение
			try:
				matrix[cell_name[0]][cell_name[1]]=float(expression)
			except:
				# Значение тега
				if expression != '' and expression[:1] == '@':
					result=get_tag(expression[1:], report, cell_name[0], cell_name[1])
					matrix[cell_name[0]][cell_name[1]]=result
				# Формула
				elif expression != '' and expression[:1] == ':':
					expression=expression.replace(':','')
					params = re.findall(r'{[^}]+}', expression)
					for param_ in params:
						if '@' in param_:
							param=param_[2:-1]
							result=get_tag(param, report, cell_name[0], cell_name[1])
						else:
							param=param_.replace('{','tmp_matrix[').replace(',','][').replace('}',']')
							result=eval_expression(param, tmp_matrix, report, cell_name[0], cell_name[1])
						expression=expression.replace(param_,unicode(result))

					matrix[cell_name[0]][cell_name[1]]=eval_expression(expression, tmp_matrix, report, cell_name[0], cell_name[1])
				# Пустая ячейка или текст
				else:
					matrix[cell_name[0]][cell_name[1]]=expression

		return render_to_response("showmatrix.html", {'matrix':matrix, 'report':report, 'date2select':date2select}, context_instance=RequestContext(request))
	# Режим редактирования отчета
	else:
		current_cells=cells.find({'parent':ObjectId(reportid)})
		tags=items.find({'type':'tag'})

		# Собираем матрицу с текущими значениями ячеек
		matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		for cell in current_cells:
			cell_name=eval(cell['cell_name'])
			cell_expression=cell['cell_expression']
			try:
				matrix[cell_name[0]][cell_name[1]]=float(cell_expression)
			except:
				matrix[cell_name[0]][cell_name[1]]=cell_expression.replace('math.log','LN').replace('if', u'ЕСЛИ').replace('else', u'ИНАЧЕ').replace('==','=').replace("<span style='background-color:#F7E4D5'>","[color1]").replace("<span style='background-color:#E3F2DF'>","[color2]").replace("<span style='background-color:#D5E8F7'>","[color3]").replace("<span style='background-color:#E3D5F7'>","[color4]").replace("<span style='background-color:#E9F7D5'>","[color5]").replace("<span style='background-color:#F7D5DB'>","[color6]").replace("<span style='background-color:#E8C6BC'>","[color7]").replace("<span style='background-color:#BCE8BF'>","[color8]").replace("<span style='background-color:#FFFB80'>","[color9]").replace("<span style='background-color:#C2BCE8'>","[color10]").replace("</span>","[/color]").replace("<b>","[b]").replace("</b>","[/b]")

		if request.method == 'POST':
			for cell_name, cell_expression in request.POST.items():
				try:
					# Пробуем преобразовать в число
					cells.update({"cell_name":cell_name,'parent':ObjectId(reportid)},{"$set":{'cell_expression':float(cell_expression)}}, True)
				except:
					# Это либо текст, либо формула.
					cells.update({"cell_name":cell_name,'parent':ObjectId(reportid)},{"$set":{'cell_expression':cell_expression.replace('LN','math.log').replace(u'ЕСЛИ', 'if').replace(u'ИНАЧЕ', 'else').replace('=','==').replace("[color1]","<span style='background-color:#F7E4D5'>").replace("[color2]","<span style='background-color:#E3F2DF'>").replace("[color3]","<span style='background-color:#D5E8F7'>").replace("[color4]","<span style='background-color:#E3D5F7'>").replace("[color5]","<span style='background-color:#E9F7D5'>").replace("[color6]","<span style='background-color:#F7D5DB'>").replace("[color7]","<span style='background-color:#E8C6BC'>").replace("[color8]","<span style='background-color:#BCE8BF'>").replace("[color9]","<span style='background-color:#FFFB80'>").replace("[color10]","<span style='background-color:#C2BCE8'>").replace("[/color]","</span>").replace("[b]","<b>").replace("[/b]","</b>")}}, True)

			return HttpResponseRedirect('')

		return render_to_response("matrix.html", {'matrix':matrix, 'tags':tags}, context_instance=RequestContext(request))


# Метод, проверяющий давность вычитывания тега и его обновление.
# Если разница с текущим и временем последнего опроса больше 120 секунд - регистрируем ошибку.
# Красим тег и выставляем значение в 'Error'
def check_tag_update(tagid):
	ts=time.time()
	tag_info=r.hgetall(tagid)
	tag_time=float(tag_info['time'])
	dtime=float(ts)-tag_time
	if dtime > 120:
		state=e_collection(tagid,{u"Данные не обновлялись больше %.f минут" % (dtime/60.0):True})
		r.hmset(tagid, {'status':2, 'value':'Error', 'state':state})


def CurrentValuesForReport(request):

	def GetRedisVal(shortname):
		tag = items.find_one({"short_name":shortname})
		check_tag_update(str(tag['_id']))
		value = r.hgetall(str(tag['_id']))
		return {'value':value, 'tagid':str(tag['_id'])}

	tags=cells.find({"parent":ObjectId(request.GET.get('report'))})
	tags_json={}
	for tag in tags:
		if tag['cell_expression'] and tag['cell_expression'][0]==":":
			short_name=tag['cell_expression'][3:-1]
			r_val=GetRedisVal(short_name)
			tags_json[r_val['tagid']]=r_val['value']

	tags=json.dumps(tags_json)
	return render_to_response("get_tag_by_shortname.html", {'tags':tags}, context_instance=RequestContext(request, processors=[custom_proc]))

def EditReportCurr(request, reportid):
	report=reports.find_one({'_id':ObjectId(reportid)})
	reportx=int(report['y'])
	reporty=int(report['x'])

	if request.GET.get('show'):
		# Матрица с конечными результатами
		matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		report_cells=cells.find({'parent':ObjectId(reportid)})

		# Матрица с формулами
		tmp_matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		report_cells_clone=report_cells.clone()
		for cell in report_cells_clone:
			cell_name=eval(cell['cell_name'])
			cell_expression=cell['cell_expression']
			tmp_matrix[cell_name[0]][cell_name[1]]=cell_expression


		def get_tag(shortname):
			tag=items.find_one({"short_name":shortname.encode("utf-8")})
			# Запрашиваем текущие значения
			tag=r.hgetall(str(tag['_id']))
			return tag

		# Получаем значения ячеек текущего отчета и отправляем в функцию, вычисляющую выражение
		for cell in report_cells:
			cell_name=eval(cell['cell_name'])
			expression=cell['cell_expression']
			if expression != '' and expression[0]==':':
				result=get_tag(expression[3:-1])
			else:
				result=expression
			matrix[cell_name[0]][cell_name[1]]=result


		return render_to_response("showmatrix_current.html", {'matrix':matrix, 'report':report}, context_instance=RequestContext(request))

	# Режим редактирования отчета
	else:
		current_cells=cells.find({'parent':ObjectId(reportid)})
		tags=items.find({'type':'tag'})

		# Собираем матрицу с текущими значениями ячеек
		matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		for cell in current_cells:
			cell_name=eval(cell['cell_name'])
			cell_expression=cell['cell_expression']
			matrix[cell_name[0]][cell_name[1]]=cell_expression.replace('math.log','LN').replace('if', u'ЕСЛИ').replace('else', u'ИНАЧЕ').replace('==','=').replace("<span class='green'>","[g]").replace("<b>","[b]").replace("</span>","[/g]").replace("</b>","[/b]")

		if request.method == 'POST':
			for cell_name, cell_expression in request.POST.items():
				cells.update({"cell_name":cell_name,'parent':ObjectId(reportid)},{"$set":{'cell_expression':cell_expression.replace('LN','math.log').replace(u'ЕСЛИ', 'if').replace(u'ИНАЧЕ', 'else').replace('=','==').replace("[g]","<span class='green'>").replace("[b]","<b>").replace("[/g]","</span>").replace("[/b]","</b>")}}, True)

			return HttpResponseRedirect('')

		return render_to_response("matrix.html", {'matrix':matrix, 'tags':tags}, context_instance=RequestContext(request))


# Для Гриши.
def DateRangeReport(request, reportid):
	report=reports.find_one({'_id':ObjectId(reportid)})
	reportx=int(report['y'])
	reporty=int(report['x'])

	# Список со всем матрицами за все даты
	all_matrix=[]

	# Высчитываем даты в указанном диапазоне
	def date_range(start, end):
		ts=datetime.now()
		ts=datetime(ts.year,ts.month,ts.day)
		delta=timedelta(days=1)
		start = datetime.strptime(start, '%d-%m-%Y')
		end = datetime.strptime(end, '%d-%m-%Y')
		if end >= ts:
			end=ts-delta
		
		all_dates=[]

		while end >= start:
			all_dates.append(time.mktime(start.timetuple()))
			start=start+delta

		return all_dates

	# Складываем значение списков
	def sum(val1, val2):
		try:
			return val1+val2
		except:
			return val1


	if request.GET.get('show'):
		if request.GET.get('start_date') and request.GET.get('end_date'):
			dates=date_range(request.GET.get('start_date'),request.GET.get('end_date'))
			
			# Список, накапливающий сумму за дни
			summary=[0 for x in xrange(reportx)]

			for cdate in dates:
				# Матрица с конечными результатами
				matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
				report_cells=cells.find({'parent':ObjectId(reportid)})

				# Матрица с формулами
				tmp_matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
				report_cells_clone=report_cells.clone()
				for cell in report_cells_clone:
					cell_name=eval(cell['cell_name'])
					cell_expression=cell['cell_expression']
					tmp_matrix[cell_name[0]][cell_name[1]]=cell_expression

				# Функция вычисления значения
				def eval_expression(expression, tmp_matrix):
					expression=expression.replace(':','')
					if expression[:1]=='@':
						expression=get_tag(expression[1:])
						eval_expression(str(expression),tmp_matrix)
					try:
						result=eval(expression)
						return result
					except:
						params = re.findall(r'{[^}]+}', expression)
						for param_ in params:
							if '@' in param_:
								param=param_[2:-1]
								result=get_tag(param)
							else:
								param=param_.replace('{','tmp_matrix[').replace(',','][').replace('}',']')
								result=eval_expression(param,tmp_matrix)
							expression=expression.replace(unicode(param_),unicode(result))
						result = eval_expression(unicode(expression),tmp_matrix)
						return result

				def get_tag(shortname):
					tag=items.find_one({"short_name":shortname.encode("utf-8")})
					predecessor=average_day.find({'tag_id':ObjectId(tag["_id"]), 'start':cdate}).limit(1).sort('_id',-1)
					for tag_value in predecessor:
						tag_value=tag_value['value']

						return round(float(tag_value),2)


				# Получаем значения ячеек текущего отчета и отправляем в функцию, вычисляющую выражение
				for cell in report_cells:
					cell_name=eval(cell['cell_name'])
					expression=cell['cell_expression']
					# Пробуем перевести во float значение
					try:
						matrix[cell_name[0]][cell_name[1]]=float(expression)
					except:
						# Значение тега
						if expression != '' and expression[:1] == '@':
							result=get_tag(expression[1:])
							matrix[cell_name[0]][cell_name[1]]=result
						# Формула
						elif expression != '' and expression[:1] == ':':
							expression=expression.replace(':','')
							params = re.findall(r'{[^}]+}', expression)
							for param_ in params:
								if '@' in param_:
									param=param_[2:-1]
									result=get_tag(param)
								else:
									param=param_.replace('{','tmp_matrix[').replace(',','][').replace('}',']')
									result=eval_expression(param, tmp_matrix)
								expression=expression.replace(param_,unicode(result))

							matrix[cell_name[0]][cell_name[1]]=eval_expression(expression,tmp_matrix)
						# Пустая ячейка или текст
						else:
							matrix[cell_name[0]][cell_name[1]]=expression

				curren_matrix={}
				curren_matrix['date']=cdate
				curren_matrix['matrix']=matrix

				all_matrix.append(curren_matrix)

				summary=map(sum, summary, matrix[1])

			return render_to_response("showmatrix_summ.html", {'all_matrix':all_matrix, 'report':report, 'dates':dates, 'summary':summary}, context_instance=RequestContext(request))
		else:
			return render_to_response("showmatrix_summ.html", {'report':report}, context_instance=RequestContext(request))

	# Режим редактирования отчета
	else:
		current_cells=cells.find({'parent':ObjectId(reportid)})
		tags=items.find({'type':'tag'})

		# Собираем матрицу с текущими значениями ячеек
		matrix = [[None for x in xrange(reportx)] for x in xrange(reporty)]
		for cell in current_cells:
			cell_name=eval(cell['cell_name'])
			cell_expression=cell['cell_expression']
			try:
				matrix[cell_name[0]][cell_name[1]]=float(cell_expression)
			except:
				matrix[cell_name[0]][cell_name[1]]=cell_expression.replace('math.log','LN').replace('if', u'ЕСЛИ').replace('else', u'ИНАЧЕ').replace('==','=').replace("<span class='green'>","[g]").replace("<b>","[b]").replace("</span>","[/g]").replace("</b>","[/b]")

		if request.method == 'POST':
			for cell_name, cell_expression in request.POST.items():
				try:
					# Пробуем преобразовать в число
					cells.update({"cell_name":cell_name,'parent':ObjectId(reportid)},{"$set":{'cell_expression':float(cell_expression)}}, True)
				except:
					# Это либо текст, либо формула.
					cells.update({"cell_name":cell_name,'parent':ObjectId(reportid)},{"$set":{'cell_expression':cell_expression.replace('LN','math.log').replace(u'ЕСЛИ', 'if').replace(u'ИНАЧЕ', 'else').replace('=','==').replace("[g]","<span class='green'>").replace("[b]","<b>").replace("[/g]","</span>").replace("[/b]","</b>")}}, True)

			return HttpResponseRedirect('')

		return render_to_response("matrix.html", {'matrix':matrix, 'tags':tags}, context_instance=RequestContext(request))




import graph
def ShowGraph(request):
	return graph.show_graph(request)

def GraphData(request):
	return graph.data_graph(request)

def GraphHelp(request):
	return graph.help_graph(request)
#from django.contrib import admin
#def i18n_javascript(request):
#	return admin.site.i18n_javascript(request)