# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 17:50:43 2020

@author: chris
"""

import json

with open('./Data/outcodes.json', 'r') as rf:
    d = json.load(rf)
    
new_dict = {}
for item in d:
   name = item['code']
   new_dict[item['outcode']] = item['code']
   
with open('./Data/outcodes_parse.json', 'w+') as wf:
    json.dump(new_dict, wf)