# -*- coding: utf-8 -*-
from django import template
register = template.Library()

import sys
sys.path.append("/home/root2/mptt/readtags")
from config_project import *

def group_name(value):
	groups=items.find({'_id':{'$in':[ObjectId(x) for x in value]}},{'name':1, '_id':0})
	return groups
	
	
register.filter('group_name', group_name)