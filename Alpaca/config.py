# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 16:20:56 2020

@author: chris
"""

from easydict import EasyDict as edict


__C                           = edict()
# Consumers can get config by: from config import cfg

cfg                           = __C

# General options
__C.SEARCH                    = edict()

__C.SEARCH.location             = "REGION%5E219"
__C.SEARCH.radius               = 20.0 # miles
__C.SEARCH.minPrice             = 100000
__C.SEARCH.maxPrice             = 200000
__C.SEARCH.minBed               = 2
__C.SEARCH.maxBed               = 4
__C.SEARCH.propType             = "houses"
__C.SEARCH.maxDaysListed        = 14
__C.SEARCH.includeSSTC          = "on"

__C.SEARCH.URL                  = (f"https://www.rightmove.co.uk/property-for-sale/find.html?" + 
                                    "searchType=SALE&" + "locationIdentifier={location}&" + 
                                    "insId=1&" + 
                                    "radius={radius}&" + 
                                    "minPrice={minPrice}&maxPrice={maxPrice}&" + 
                                    "minBedrooms={minBed}&maxBedrooms={maxBed}&" + 
                                    "displayPropertyType={propType}&" + 
                                    "maxDaysSinceAdded={maxDaysListed}&" + 
                                    "_includeSSTC={includeSSTC}&sortByPriceDescending=&" + 
                                    "primaryDisplayPropertyType=&" + "secondaryDisplayPropertyType=&" + 
                                    "oldDisplayPropertyType=&" + 
                                    "oldPrimaryDisplayPropertyType=&" + 
                                    "newHome=&" + 
                                    "auction=false")