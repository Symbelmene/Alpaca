# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:02:15 2020

@author: chris
"""

#from scrape import getPageData

import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Google API Key: AIzaSyD3oDTdVEv170DhkSEo2xDjE4VBm6FPSkA

import googlemaps
from datetime import datetime

def getSearchURL(page=0):
    # Input search criteria
    outcode = "GU4"
    radius = 5.0 # miles
    minPrice = 500000
    maxPrice = 600000
    minBed = 3
    maxBed = 4
    propType = "houses"
    maxDaysListed = 14
    includeSSTC = "on"
    
    # Translate postcode to RM Outcode format
    with open('./Data/outcodes_parse.json', 'r') as rf:
        codes = json.load(rf)
    location = f"OUTCODE%5E{codes[outcode]}"
    
    # Final search URL
    searchURL = ("https://www.rightmove.co.uk/property-for-sale/find.html?" + 
        f"searchType=SALE&locationIdentifier={location}&" + 
        "insId=1&" + 
        f"radius={radius}&" + f"index={page*25}&" + 
        f"minPrice={minPrice}&maxPrice={maxPrice}&" + 
        f"minBedrooms={minBed}&maxBedrooms={maxBed}&" + 
        f"displayPropertyType={propType}&" + 
        f"maxDaysSinceAdded={maxDaysListed}&" + 
        f"_includeSSTC={includeSSTC}&sortByPriceDescending=&" + 
        "primaryDisplayPropertyType=&" + "secondaryDisplayPropertyType=&" + 
        "oldDisplayPropertyType=&" + 
        "oldPrimaryDisplayPropertyType=&" + 
        "newHome=&" + 
        "auction=false")
    return searchURL

def getSearchData(url):
    reqGet = requests.get(url)
    soup = BeautifulSoup(reqGet.text, 'lxml')
    
    # Parse first page
    print("Scraping page 0")
    searchResults = soup.findAll('a', {"class":"propertyCard-anchor"})
    propIDList = [s["id"].replace('prop','') for s in searchResults]
    
    # Get number of pages
    numResults = soup.find("span", {"class":"searchHeader-resultCount"})
    numResultsInt = int(numResults.text.replace(',',''))
    pages = numResultsInt // 25
    if numResultsInt > 1000:
        print("Over 1000 results found. Not all results will be displayed...")
        pages = 40
    for i in range(1, pages):
        print("Scraping page {}".format(i))
        reqGet = requests.get(getSearchURL(i))
        soup = BeautifulSoup(reqGet.text, 'lxml')        
        searchResults = soup.findAll('a', {"class":"propertyCard-anchor"})
        propertyResults = soup.findAll('address', {"class":"propertyCard-address"})
        addressResults = propertyResults.text.replace("\n", "")
        propIDList += [s["id"].replace('prop','') for s in searchResults]
    return propIDList

def getPropertyData(propertyID):
    error = True
    i = 0
    while error and i < 5:
        # Get property URL
        url = "http://www.rightmove.com/property-for-sale/property-{}.html".format(propertyID)
        reqGet = requests.get(url)
        soup = BeautifulSoup(reqGet.text, 'lxml')
        print(propertyID)
        # Get property data
        scriptData = soup.find('script', {"type":"text/javascript"})
        if "RIGHTMOVE_JS_ERROR" in str(scriptData):
            print("Got bad request on property {}. Retrying...".format(propertyID))
            i += 1
        else:
            error = False
    if i >= 5:
        return 0
    rawData = str(scriptData).split('L = ')[1].replace("</script>","")
    data = json.loads(rawData)
    return data



url = getSearchURL()
propIDs = getSearchData(url)
#propertyData = [getPropertyData(p) for p in propIDs]
