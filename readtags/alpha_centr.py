# -*- coding: utf-8 -*-
import time, datetime, os
from datetime import datetime, timedelta
from config_project import *
from bson.objectid import ObjectId

import cx_Oracle
conn=cx_Oracle.connect("s1/s1@172.27.102.3/orcl")
cur = conn.cursor()

ts = datetime.now()
delta = timedelta(days=1)
period = ts-delta
period = period.strftime("%d-%m-%Y")
yesterday = ts-2*delta
yesterday = yesterday.strftime("%d-%m-%Y")

end_for_mongo = datetime(ts.year,ts.month,ts.day)
end_for_mongo = time.mktime(end_for_mongo.timetuple())
start_for_mongo = end_for_mongo-86400

# Выбираем теги по группе
gid=str(items.find_one({'type':'group','environment':'alpha_centr'})['_id'])
tags=list(items.find({'type':'tag', 'groups':{'$in':[gid]}}).sort('_id',1))

for tag in tags:
	if tag['fid']<7:
		n_gr_integr = 1
	elif tag['fid']>6 and tag['fid']<18 and tag['n_gr_ty']==1:
		n_gr_integr = 10
	elif tag['fid']>6 and tag['fid']<18 and tag['n_gr_ty']==2:
		n_gr_integr = 9
	else:
		n_gr_integr = 5
	value1=list(cur.execute("select sum(b.RASH_POLN) \
		from CNT.GR_GR a, CNT.BUF_V_INT b, CNT.FID c, CNT.OBEKT d  \
		where a.N_OB_TY = b.N_OB and a.SYB_RNK_TY = b.SYB_RNK \
		and a.N_FID = b.N_FID and a.N_GR_TY = b.N_GR_TY and c.N_OB = a.N_OB_TY and c.SYB_RNK = a.SYB_RNK_TY \
		and c.N_FID = a.N_FID and d.N_OB = a.N_OB_TY and d.SYB_RNK = a.SYB_RNK_TY  \
		and a.N_OB = 24580001 \
		and d.syb_rnk=1 \
		and b.N_INTER_RAS>36 \
		and a.ZNAK = 1 \
		and a.N_OB_TY = 24580001 \
		and a.N_GR_INTEGR = %s \
		and b.DD_MM_YYYY = TO_DATE('%s', 'DD-MM-YYYY') and c.n_fid= %s and a.N_GR_TY=%s " % (n_gr_integr,yesterday, tag['fid'], tag['n_gr_ty'])))[0][0]
	value2=list(cur.execute("select sum(b.RASH_POLN) \
		from CNT.GR_GR a, CNT.BUF_V_INT b, CNT.FID c, CNT.OBEKT d  \
		where a.N_OB_TY = b.N_OB and a.SYB_RNK_TY = b.SYB_RNK \
		and a.N_FID = b.N_FID and a.N_GR_TY = b.N_GR_TY and c.N_OB = a.N_OB_TY and c.SYB_RNK = a.SYB_RNK_TY \
		and c.N_FID = a.N_FID and d.N_OB = a.N_OB_TY and d.SYB_RNK = a.SYB_RNK_TY  \
		and a.N_OB = 24580001 \
		and d.syb_rnk=1 \
		and b.N_INTER_RAS<37 \
		and a.ZNAK = 1 \
		and a.N_OB_TY = 24580001 \
		and a.N_GR_INTEGR = %s \
		and b.DD_MM_YYYY = TO_DATE('%s', 'DD-MM-YYYY') and c.n_fid= %s and a.N_GR_TY=%s " % (n_gr_integr,period, tag['fid'], tag['n_gr_ty'])))[0][0]
	if not value1:
		value1=0
	if not value2:
		value2=0
	average=({'tag_id': ObjectId(tag['_id']), 'value':float(value1+value2),'start':start_for_mongo,'end':end_for_mongo, 'err_state':0})
	average_day.insert(average)