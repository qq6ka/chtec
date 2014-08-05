# # -*- coding: utf-8 -*-
from config_project import *
import time, random, threading, os, datetime
from bson.objectid import ObjectId
from datetime import datetime



ts=datetime.now()
start=datetime(ts.year,ts.month,ts.day)
start=time.mktime(start.timetuple())
print start
end=start+86399
print datetime.fromtimestamp(float(end))