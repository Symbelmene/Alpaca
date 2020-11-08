# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 19:43:49 2020

@author: chris
"""

from bs4 import BeautifulSoup
import requests
import json

# Google API Key: AIzaSyD3oDTdVEv170DhkSEo2xDjE4VBm6FPSkA

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD3oDTdVEv170DhkSEo2xDjE4VBm6FPSkA')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)