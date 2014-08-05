# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.shortcuts import render_to_response
import string
import random
from models import *
from myforms import *
from django.http import HttpResponseRedirect, HttpRequest,HttpResponse
from django import forms
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os, urlparse, sys, datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.mail import send_mail
import base64
from xml.dom.minidom import *
import httplib, time
import mimetypes
import sys
from bson.objectid import ObjectId
sys.path.append('/usr/local/lib/python2.7/site-packages/pymongo')
sys.path.append('/usr/local/lib/python2.7/site-packages/pymongo-2.5.2-py2.7.egg-info')
import pymongo
import xlwt
import styles

sys.path.append("/home/root2/mptt/readtags")
from config_project import *

#def toexcel(graph,data):
#    wbook = xlwt.Workbook()
#    sheet = wbook.add_sheet(u'sheet1')
#    row_top = 5
#    row = row_top
#    col = 0
#    for tag in data['series']:
#        sheet.write(row_top,col,u'Время',styles.styletoptable)
#        sheet.write(row_top,col+1,data['options']['labels'][tag],styles.styletoptable)
#        row = row_top+1
#        for tm in sorted(data['series'][tag]):
#            sheet.write(row,col,str(datetime.datetime.fromtimestamp(tm)),styles.stylebodytable)
#            sheet.write(row,col+1,data['series'][tag][tm],styles.stylebodytable)
#            row += 1
#        col += 2
#    row += 1
#    wbook.save(graph)

def toexcel_hourday(graph,data,db_ts,de_ts,kind_data):
    try:
        if kind_data == "hour":
            db = int(time.mktime(datetime.datetime.fromtimestamp(db_ts).replace(minute = 0,second = 0).timetuple()))
            de = int(time.mktime(datetime.datetime.fromtimestamp(de_ts).replace(minute = 0,second = 0).timetuple()))
            step_second = 3600
        if kind_data == "day":
            db = int(time.mktime(datetime.datetime.fromtimestamp(db_ts).replace(hour = 0,minute = 0,second = 0).timetuple()))
            de = int(time.mktime(datetime.datetime.fromtimestamp(de_ts).replace(hour = 0,minute = 0,second = 0).timetuple()))
            step_second = 86400
        wbook = xlwt.Workbook()
        sheet = wbook.add_sheet(u'sheet1')
        row_top = 5
        row = row_top
        col = 0
        dt = db
        sheet.write(row_top,col,u'Время',styles.styletoptable)
        row = row_top+1
### ### column of time
        while dt<=de:
            sheet.write(row,col,str(datetime.datetime.fromtimestamp(dt)),styles.stylebodytable)
            row += 1
            dt = dt + step_second
        col += 1
        for tag in data['series']:
            sheet.write(row_top,col,data['options']['labels'][tag],styles.styletoptable)
            row = row_top+1
            dt = db
            while dt<=de:
                if dt in data['series'][tag]:
                    sheet.write(row,col,data['series'][tag][dt],styles.stylebodytable)
                else:
                    sheet.write(row,col,"NaN",styles.stylebodytable)
                row += 1
                dt = dt + step_second
            col += 1
        wbook.save(graph)
    except Exception as E:
        f_log = open('/home/root2/mptt/bc/graph_log','w')
        print  >> f_log,"1-exception ! = ",E
        f_log.close()

def toexcel(graph,data,db,de):
    try:
        wbook = xlwt.Workbook()
        sheet = wbook.add_sheet(u'sheet1')
        row_top = 5
        row = row_top
        col = 0
        sheet.write(row_top,col,u'Время',styles.styletoptable)
        col = 1
        row = row_top + 1
#   #    sheet.write(row,col,str(dt),styles.stylebodytable)
        dt = db
        f_log = open('/home/root2/mptt/bc/graph_log','w')
########## column of time
        print  >> f_log,"befor while"
        while dt<=de:
            sheet.write(row,0,str(datetime.datetime.fromtimestamp(dt)),styles.stylebodytable)
            row += 1
            dt = dt + 5
########## data columns 
        print  >> f_log,"befor for"
        for tag in data['series']:
            sheet.write(row_top,col,data['options']['labels'][tag],styles.styletoptable)
            row = row_top+1
            dt = db
            prv_time = 0
            prv_val = 0
            print  >> f_log,"befor for 2"
            for tm in sorted(data['series'][tag]):
                if prv_time == 0:
                    if data['series'][tag][tm]=='Error':
                        continue
                    prv_time = db
                    prv_val = data['series'][tag][tm]
#                print  >> f_log,"befor while 5",data['series'][tag][tm],prv_val
                else:
                    if data['series'][tag][tm]=='Error':
                        continue
                while dt<=tm:
                    try:
                        if tm != prv_time:
                            sheet.write(row,col,(dt-prv_time)/(tm-prv_time)*(float(data['series'][tag][tm])-float(prv_val))+float(prv_val),styles.stylebodytable)
                        else:
                            sheet.write(row,col,data['series'][tag][tm],styles.stylebodytable)
                    except Exception as E:
                        print  >> f_log,"Exception 111 ",E
                    row += 1
                    dt = dt + 5
#                if data['series'][tag][tm]!='Error':
                prv_time = tm
                prv_val = data['series'][tag][tm]
            print  >> f_log,"befor while 2"
            print  >> f_log,str(datetime.datetime.fromtimestamp(dt)),str(datetime.datetime.fromtimestamp(de))
            while dt<=de:
                print  >> f_log,str(datetime.datetime.fromtimestamp(dt)),prv_val
                sheet.write(row,col,prv_val,styles.stylebodytable)
                row += 1
                dt = dt + 5
            col += 1
        print  >> f_log,"befor booksave",graph
        wbook.save(graph)
        print  >> f_log,"after booksave",graph
        f_log.close()
    except Exception as E:
        f_log = open('/home/root2/mptt/bc/graph_log','w')
        print  >> f_log,"2-exception ! = ",E
        f_log.close()

def help_graph(request):
    return render_to_response("help_graph.html")
def show_graph(request):
    coll=db['items']
    tags_select = None
    if request.method == "GET":
        if "reload" in request.GET:
            if request.GET["reload"]=="on":
                tags_select = coll.find({"groups":request.GET["graphs"]}).sort("name",1)
                sel_graph = request.GET['graphs']
                return HttpResponseRedirect("graph.html",{"groups":coll.find({"type":"group"}).sort("name",1),
                   "tags_select":tags_select,
                   "graphs":coll.find({"type":"group_graph"}).sort("name",1),
                   "sel_graph":sel_graph})
        else:
            return render_to_response("graph.html",{"groups":coll.find({"type":"group"}).sort("name",1),\
                                                "graphs":coll.find({"type":"group_graph"}).sort("name",1) })
    else:
        sel_graph = None
#        f_log = open('/home/root2/mptt/bc/graph_log','w')
#        print >>f_log,"POST = ",request.POST
        autorefresh = ""
        minY = ""
        maxY = ""
        tickY = ""
        if 'action'  in request.POST:
            if request.POST['action'] == 'del_graph' and 'graphs' in request.POST:
                coll.remove({ '_id':ObjectId(request.POST['graphs'])})
            if request.POST['action'] == 'add_tag' and 'tags_enable' in request.POST and 'graphs' in request.POST:
                if request.POST['graphs'] != "-1":
                    for tag in request.POST.getlist('tags_enable'):
                        coll.update({ '_id':ObjectId(tag)},{'$push': {'groups':request.POST['graphs']}},True )
                    sel_graph = request.POST['graphs']
                    tags_select = coll.find({"groups":request.POST["graphs"]}).sort("name",1)
            if request.POST['action'] == 'del_tag' and 'tags_select' in request.POST and 'graphs' in request.POST:
                for tag in request.POST.getlist('tags_select'):
                    coll.update({ '_id':ObjectId(tag)},{'$pull': {'groups':request.POST['graphs']}},True )
                sel_graph = request.POST['graphs']
                tags_select = coll.find({"groups":request.POST["graphs"]}).sort("name",1)
            if  request.POST['action'] == 'change_group' and 'groups' in request.POST :
                if 'graphs' in request.POST :
                    sel_graph = request.POST['graphs']
                    tags_select = coll.find({"groups":request.POST["graphs"]}).sort("name",1)
            if  request.POST['action'] == 'change_graph' and 'graphs' in request.POST:
                tags_select = coll.find({"groups":request.POST["graphs"]}).sort("name",1)
                sel_graph = request.POST['graphs']
            if  request.POST['action'] == 'save_graph' and 'graph_name' in request.POST:
                coll.insert({'type':'group_graph','name':request.POST['graph_name']})
                sel_graph = coll.find({'type':'group_graph','name':request.POST['graph_name']})
            if request.POST['action'] == 'reload' and 'graphs' in request.POST and 'autorefresh' in request.POST and 'discrete' in request.POST :
                if (request.POST["autorefresh"] == "on") and (request.POST["discrete"]=="real"):
#                    print >>f_log,"in you need"
                    sel_graph = request.POST['graphs']
                    tags_select = coll.find({"groups":request.POST["graphs"]}).sort("name",1)
                    autorefresh = "checked"
                    minY = request.POST['minY']
                    maxY = request.POST['maxY']
                    tickY = request.POST['tickY']
                    tickX = request.POST['tickX']
#                    f_log.close()
        return render_to_response("graph.html",{"groups":coll.find({"type":"group"}).sort("name",1),
                   "tags_enable":coll.find({"groups":request.POST["groups"]}).sort("name",1),
                   "tags_select":tags_select,
                   "graphs":coll.find({"type":"group_graph"}).sort("name",1),
                   "sel_graph":sel_graph,
                   "autorefresh":autorefresh,
                   "minY":minY,
                   "maxY":maxY,
                   "tickY":tickY,
                   "sel_group":request.POST['groups']})

import json
import datetime
def data_graph(request):
    f_log = open('/home/root2/mptt/bc/graph_log2','w')
    if request.method == "POST":
        print >>f_log,"GET = ",request.POST
        if 'discrete' in request.POST:
            print >>f_log,"discrete exist = "
            if 'graphs' in request.POST:
                print >>f_log,"graphs exist = "
                if request.POST['discrete']=='real':
                    print >>f_log,"real = "
                    f_log.close()
                    one_hour = 3600
                    conn_tags = pymongo.Connection()
                    db_tags = conn_tags['alldevices']
                    coll_tags=db_tags['items']
                    tags = coll_tags.find({"groups":request.POST['graphs']})
                    conn_data = pymongo.Connection()
                    db_data = conn_data['archives']
                    send_json = {}
                    series = {}
                    labels = {}
                    options = {}
                    send_json["series"] = series
                    send_json["options"] = options
                    options['labels'] = labels
                    max_val = 0
                    min_val = 0
#                    maxX_val = 0
#                    minX_val = 0
                    for tag in tags:
                        labels[str(tag['_id'])] = tag['name']
#                        try:
#                            datetime_beg = int(time.mktime(datetime.datetime.strptime('Dec 1 2013  1:00PM', '%b %d %Y %I:%M%p').timetuple()))
#                        except Exception as E:
#                            print  >> f_log,"begin_for --- 2 exception",E
#                        try:
#                            datetime_end = int(time.mktime(datetime.datetime.strptime('Dec 1 2013  2:00PM', '%b %d %Y %I:%M%p').timetuple()))
#                        except Exception as E:
#                            print  >> f_log,"begin_for --- 2 exception",E

                        try:
                            datetime_beg = int(float(request.POST['begin_dates_'+str(tag['_id'])]))
                        except Exception as E:
                            f_log = open('/home/root2/mptt/bc/graph_log','w')
                            print  >> f_log,"begin_for --- 2 exception",E
                            f_log.close()
                        try:
                            datetime_end = int(float(request.POST['end_dates_'+str(tag['_id'])]))
                        except:
                            datetime_end =int(time.mktime(datetime.datetime.now().timetuple()))
                        datetime_curr = datetime_beg
                        ser_dict = {}
                        series[str(tag['_id'])] = ser_dict
                        while datetime.datetime.fromtimestamp(datetime_curr).replace(minute = 0,second = 0) <= datetime.datetime.fromtimestamp(datetime_end).replace(minute = 0,second = 0):
                            try:
                                name_coll = datetime.datetime.fromtimestamp(datetime_curr).replace(minute = 0,second = 0).strftime("%Y-%m-%d %H:%M:%S")
                            except Exception as E:
                                f_log = open('/home/root2/mptt/bc/graph_log','w')
                                print  >> f_log,"3-exception ! = ",E
                                f_log.close()
                            coll_data=db_data[name_coll]
                            if datetime.datetime.fromtimestamp(datetime_beg).replace(minute = 0,second = 0) == datetime.datetime.fromtimestamp(datetime_end).replace(minute = 0,second = 0):
                                data = coll_data.find({"tag_id":tag["_id"],"time":{"$gte":datetime_beg,"$lte":datetime_end}}).sort("time",1)
                            elif datetime.datetime.fromtimestamp(datetime_curr).replace(minute = 0,second = 0) == datetime.datetime.fromtimestamp(datetime_beg).replace(minute = 0,second = 0):
                                try:
                                    data = coll_data.find({"tag_id":tag['_id'],'time':{'$gte':datetime_beg}}).sort('time',1)
                                except Exception as E:
                                    f_log = open('/home/root2/mptt/bc/graph_log','w')
                                    print  >> f_log,"4-exception ! = ",E
                                    f_log.close()
                            elif datetime.datetime.fromtimestamp(datetime_curr).replace(minute = 0,second = 0) == datetime.datetime.fromtimestamp(datetime_end).replace(minute = 0,second = 0):
                                data = coll_data.find({"tag_id":tag['_id'],'time':{'$lte':datetime_end}}).sort('time',1)
                            elif datetime.datetime.fromtimestamp(datetime_curr).replace(minute = 0,second = 0) > datetime.datetime.fromtimestamp(datetime_beg).replace(minute = 0,second = 0):
                                data = coll_data.find({"tag_id":tag['_id']}).sort('time',1)
                            for row in data:
                                try:
                                    if float(row['value'])>max_val:
                                        max_val=float(row['value'])
                                    if float(row['value'])<min_val:
                                        min_val=float(row['value'])
                                except Exception as E:
                                    f_log = open('/home/root2/mptt/bc/graph_log','w')
                                    print  >> f_log,"5-exception ! = ",E
                                    f_log.close()
                                try:
                                    ser_dict[int(float(row['time']))]=row['value']
                                except Exception as E:
                                    f_log = open('/home/root2/mptt/bc/graph_log','w')
                                    print  >> f_log,"6-exception ! = ",E
                                    f_log.close()
                            data = None
                            datetime_curr = datetime_curr + one_hour
                        if len(series[str(tag['_id'])]) == 0:
                            del series[str(tag['_id'])]
                            del labels[str(tag['_id'])]
                    options['min'] = min_val
                    options['max'] = max_val
                    options['minX'] = datetime_beg
                    options['maxX'] = datetime_end
                    try:
                        chart = coll_tags.find_one({'_id':ObjectId(request.POST['graphs'])})
                        options['name_chart'] = chart['name']
                    except Exception as E:
                        f_log = open('/home/root2/mptt/bc/graph_log','w')
                        print  >> f_log,"7-exception ! = ",E
                        f_log.close()
#                    try:
#                        json.dumps(send_json)
#                    except Exception as E:
#                        print >>f_log,'Error dumps ',E
#                    print >> f_log, "befor response  !!!!!!!!!!!"
#                    f_log.close()
                    try:
                        if "gettable" in request.POST:
                            f_log = open('/home/root2/mptt/bc/graph_log1','w')
                            print  >> f_log,"request.POST['gettable'] ",request.POST['gettable'],('http://172.27.81.208:8000/media/'+chart['name'].encode('utf-8')+'.xls').decode('utf-8').encode('utf-8')
                            f_log.close()
                            if request.POST['gettable'] == 'true':
                                toexcel((u'/home/root2/mptt/bc/media/'+chart['name']+'.xls').encode('utf-8'),send_json,datetime_beg,datetime_end)
                                return HttpResponse("", mimetype="application/json")
                        return HttpResponse(json.dumps(send_json), mimetype="application/json")
                    except Exception as E:
                        f_log = open('/home/root2/mptt/bc/graph_log5','w')
                        print  >> f_log,"nnnnnn8-exception ! = ",E
                        f_log.close()
                if request.POST['discrete']=='hour':
#                    print >>f_log,"hour = "
                    one_month = 3600
                    conn_tags = pymongo.Connection()
                    db_tags = conn_tags['alldevices']
                    coll_tags=db_tags['items']
                    tags = coll_tags.find({"groups":request.POST['graphs']})
                    conn_data = pymongo.Connection()
                    db_data = conn_data['archives']
                    send_json = {}
                    series = {}
                    labels = {}
                    options = {}
                    send_json["series"] = series
                    send_json["options"] = options
                    options['labels'] = labels
                    max_val = 0
                    min_val = 0
                    for tag in tags:
                        labels[str(tag['_id'])] = tag['name']
                        try:
                            datetime_beg = int(float(request.POST['begin_dates_'+str(tag['_id'])]))
                        except Exception as E:
                            f_log = open('/home/root2/mptt/bc/graph_log','w')
                            print  >> f_log,"9exception ! = ",E
                            f_log.close()
                        try:
                            datetime_end = int(float(request.POST['end_dates_'+str(tag['_id'])]))
                        except:
                            datetime_end =int(time.mktime(datetime.datetime.now().timetuple()))
                        datetime_curr = datetime_beg
                        ser_dict = {}
                        series[str(tag['_id'])] = ser_dict
                        while datetime.datetime.fromtimestamp(datetime_curr).replace(day = 1,hour = 0,minute = 0,second = 0) <= datetime.datetime.fromtimestamp(datetime_end).replace(day = 1,hour = 0,minute = 0,second = 0):
                            try:
                                name_coll = datetime.datetime.fromtimestamp(datetime_curr).strftime("%Y-%m")
                            except Exception as E:
                                f_log = open('/home/root2/mptt/bc/graph_log','w')
                                print  >> f_log,"10-exception ! = ",E
                                f_log.close()
                            coll_data=db_data[name_coll]
                            if datetime.datetime.fromtimestamp(datetime_beg).replace(day = 1,hour = 0,minute = 0,second = 0) == datetime.datetime.fromtimestamp(datetime_end).replace(day = 1,hour = 0,minute = 0,second = 0):
                                data = coll_data.find({"tag_id":tag["_id"],"start":{"$gte":datetime_beg,"$lte":datetime_end}}).sort("start",1)
                            elif datetime.datetime.fromtimestamp(datetime_curr).replace(day = 1,hour = 0,minute = 0,second = 0) == datetime.datetime.fromtimestamp(datetime_beg).replace(day = 1,hour = 0,minute = 0,second = 0):
                                try:
                                    data = coll_data.find({"tag_id":tag['_id'],'start':{'$gte':datetime_beg}}).sort('start',1)
                                except Exception as E:
                                    f_log = open('/home/root2/mptt/bc/graph_log','w')
                                    print  >> f_log,"11-exception ! = ",E
                                    f_log.close()
                            elif datetime.datetime.fromtimestamp(datetime_curr).replace(day = 1,hour = 0,minute = 0,second = 0) == datetime.datetime.fromtimestamp(datetime_end).replace(day = 1,hour = 0,minute = 0,second = 0):
                                data = coll_data.find({"tag_id":tag['_id'],'start':{'$lte':datetime_end}}).sort('start',1)
                            elif datetime.datetime.fromtimestamp(datetime_curr).replace(day = 1,hour = 0,minute = 0,second = 0) > datetime.datetime.fromtimestamp(datetime_beg).replace(day = 1,hour = 0,minute = 0,second = 0):
                                data = coll_data.find({"tag_id":tag['_id']}).sort('start',1)
                            for row in data:
                                try:
                                    if float(row['value'])>max_val:
                                        max_val=float(row['value'])
                                    if float(row['value'])<min_val:
                                        min_val=float(row['value'])
                                except Exception as E:
                                    f_log = open('/home/root2/mptt/bc/graph_log','w')
                                    print  >> f_log,"12-exception ! = ",E
                                    f_log.close()
                                try:
                                    ser_dict[int(float(row['start']))]=row['value']
                                except Exception as E:
                                    f_log = open('/home/root2/mptt/bc/graph_log','w')
                                    print  >> f_log,"13-exception ! = ",E
                                    f_log.close()
                            data = None
                            temp_date = datetime.datetime.fromtimestamp(datetime_curr)
                            if temp_date.month<12:
                                datetime_curr = int(time.mktime(datetime.datetime(temp_date.year,temp_date.month+1,temp_date.day).timetuple()))
                            else:
                                datetime_curr = int(time.mktime(datetime.datetime(temp_date.year+1,1,temp_date.day).timetuple()))
#                            datetime_end =int(time.mktime(datetime.datetime.now().timetuple()))
#                            datetime_curr = datetime_curr + one_month
                        if len(series[str(tag['_id'])]) == 0:
                            del series[str(tag['_id'])]
                            del labels[str(tag['_id'])]
                    options['min'] = min_val
                    options['max'] = max_val
                    options['minX'] = datetime_beg
                    options['maxX'] = datetime_end
                    try:
                        chart = coll_tags.find_one({'_id':ObjectId(request.POST['graphs'])})
                        options['name_chart'] = chart['name']
                    except Exception as E:
                        f_log = open('/home/root2/mptt/bc/graph_log','w')
                        print  >> f_log,"14-exception ! = ",E
                        f_log.close()
                    try:
                        if "gettable" in request.POST:
                            if request.POST['gettable'] == 'true':
                                toexcel_hourday((u'/home/root2/mptt/bc/media/'+chart['name']+'.xls').encode('utf-8'),send_json,datetime_beg,datetime_end,"hour")
                                return HttpResponse("", mimetype="application/json")
                        return HttpResponse(json.dumps(send_json), mimetype="application/json")
                    except Exception as E:
                        f_log = open('/home/root2/mptt/bc/graph_log','w')
                        print  >> f_log,"15-exception ! = ",E
                        f_log.close()
                if request.POST['discrete']=='day':
#                    print >>f_log,"day = "
                    one_month = 3600
                    conn_tags = pymongo.Connection()
                    db_tags = conn_tags['alldevices']
                    coll_tags=db_tags['items']
                    tags = coll_tags.find({"groups":request.POST['graphs']})
                    conn_data = pymongo.Connection()
                    db_data = conn_data['archives']
                    send_json = {}
                    series = {}
                    labels = {}
                    options = {}
                    send_json["series"] = series
                    send_json["options"] = options
                    options['labels'] = labels
                    max_val = 0
                    min_val = 0
                    for tag in tags:
                        labels[str(tag['_id'])] = tag['name']
                        try:
                            datetime_beg = int(float(request.POST['begin_dates_'+str(tag['_id'])]))
                        except Exception as E:
                            f_log = open('/home/root2/mptt/bc/graph_log','w')
                            print  >> f_log,"16-exception ! = ",E
                            f_log.close()
                        try:
                            datetime_end = int(float(request.POST['end_dates_'+str(tag['_id'])]))
                        except:
                            datetime_end =int(time.mktime(datetime.datetime.now().timetuple()))
                        ser_dict = {}
                        series[str(tag['_id'])] = ser_dict
                        name_coll = "average_day"
                        coll_data=db_data[name_coll]
                        data = coll_data.find({"tag_id":tag["_id"],"start":{"$gte":datetime_beg,"$lte":datetime_end}}).sort("start",1)
                        for row in data:
                            try:
                                if float(row['value'])>max_val:
                                    max_val=float(row['value'])
                                if float(row['value'])<min_val:
                                    min_val=float(row['value'])
                            except Exception as E:
                                f_log = open('/home/root2/mptt/bc/graph_log','w')
                                print  >> f_log,"17-exception ! = ",E
                                f_log.close()
                            try:
                                ser_dict[int(float(row['start']))]=row['value']
                            except Exception as E:
                                f_log = open('/home/root2/mptt/bc/graph_log','w')
                                print  >> f_log,"18-exception ! = ",E
                                f_log.close()
                        data = None
                        if len(series[str(tag['_id'])]) == 0:
                            del series[str(tag['_id'])]
                            del labels[str(tag['_id'])]
                    options['min'] = min_val
                    options['max'] = max_val
                    options['minX'] = datetime_beg
                    options['maxX'] = datetime_end
                    try:
                        chart = coll_tags.find_one({'_id':ObjectId(request.POST['graphs'])})
                        options['name_chart'] = chart['name']
                    except Exception as E:
                        f_log = open('/home/root2/mptt/bc/graph_log','w')
                        print  >> f_log,"19-exception ! = ",E
                        f_log.close()
                    try:
                        if "gettable" in request.POST:
                            if request.POST['gettable'] == 'true':
                                toexcel_hourday((u'/home/root2/mptt/bc/media/'+chart['name']+'.xls').encode('utf-8'),send_json,datetime_beg,datetime_end,"day")
                                return HttpResponse("", mimetype="application/json")
                        return HttpResponse(json.dumps(send_json), mimetype="application/json")
                    except Exception as E:
                        f_log = open('/home/root2/mptt/bc/graph_log','w')
                        print  >> f_log,"20-exception ! = ",E
                        f_log.close()


#from django.contrib import admin
#def i18n_javascript(request):
#    return admin.site.i18n_javascript(request)