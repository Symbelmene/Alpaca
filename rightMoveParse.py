# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 21:34:58 2020

@author: chris
"""

from bs4 import BeautifulSoup
import requests
import time
import json
import pandas as pd
from multiprocessing import Pool

dfKey = ['address', 'bathrooms', 'bedrooms', 'hasFloorPlan', 
         'lat', 'lng', 'propertyType', 'displayPrice', 
         'dateSold', 'tenure']

def getPageData(url):
    reqGet = requests.get(url)
    
    soup = BeautifulSoup(reqGet.text, 'lxml')
    #siteData = soup.prettify()
    scriptData = str(soup.findAll('script')[0])
    
    rawData = scriptData.replace('<script>window.__PRELOADED_STATE__ = ', '')
    rawData = rawData.replace('</script>', '')

    data = json.loads(rawData)
    return data

def getHouseInfo(d):
    l = []
    for e in range(len(d['transactions'])):
        houseList = []
        houseList.append(d['address'])
        houseList.append(d['bathrooms'])
        houseList.append(d['bedrooms'])
        houseList.append(d['hasFloorPlan'])
        houseList.append(d['location']['lat'])
        houseList.append(d['location']['lng'])
        houseList.append(d['propertyType'])
        houseList.append(d['transactions'][e]['displayPrice'][1:])
        houseList.append(d['transactions'][e]['dateSold'])
        houseList.append(d['transactions'][e]['tenure'])
        l.append(houseList)
    return l

def getPropertyData(postCode):
    propertyList = []
    # Get first page for initial data
    target = f'https://www.rightmove.co.uk/house-prices/{postCode}.html?page=1'
    data = getPageData(target)
    numPages = data['pagination']['last']
    propertyData = data['results']['properties']
    for prop in propertyData:
        ret = getHouseInfo(prop)
        propertyList += ret
    print('Got data from {}'.format(target))
    # Scrape additional pages
    for p in range(2,numPages+1):
        time.sleep(1)
        target = f'https://www.rightmove.co.uk/house-prices/{postCode}.html?page={p}'
        data = getPageData(target)
        propertyData = data['results']['properties']
        for prop in propertyData:
            ret = getHouseInfo(prop)
            propertyList += ret
        print('Got data from {}'.format(target))
    return propertyList

# MAIN PROGRAM START
if __name__ == '__main__':
    pool = Pool(processes=4)
    # Post codes to gather data on
    postCodeList = ['bs1', 'bs2', 'bs3', 'bs4', 'bs5', 'bs6']
    propertyDetailsList = pool.map(getPropertyData, postCodeList)
    #propertyDetailsList = []
    #for e in postCodeList:
    #    propertyDetailsList.append(getPropertyData(e))
    
    results = [entry for subList in propertyDetailsList for entry in subList]
    df = pd.DataFrame(results, columns=dfKey)
    df.to_csv('test_out.csv')