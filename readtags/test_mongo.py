## -*- coding: utf-8 -*- 
from config_project import *

all_items=items.find({})
for item in all_items:
	for key, value in item.items():
		print key, value