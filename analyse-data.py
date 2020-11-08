# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 21:47:06 2020

@author: chris
"""

from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests


def parseCSV(csvFile):
    """

    Parameters
    ----------
    csvFile : String
        Location of CSV file conaining scraped data

    Returns
    -------
    df : Dataframe
        Parsed dataframe with formatted dates, numbers etc...

    """
    
    # Read csv and parse numerical values
    df = pd.read_csv(dataFile, thousands=',')
    
    # Parse dates
    df['dateSold'] = pd.to_datetime(df['dateSold'])
    
    # Generate post code column
    df['postCode'] = 'None'
    for idx, row in df.iterrows():
        df.at[idx, 'postCode'] = '{} {}'.format(row['address'].split(' ')[-2], row['address'].split(' ')[-1])
    
    return df

def getMap():
    apiKey = 'AIzaSyD3oDTdVEv170DhkSEo2xDjE4VBm6FPSkA'
    lat = 51.4545
    long = -2.5879
    zoom = 11
    size = (500, 500)
    url = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom={}&size={}x{}&key={}'.format(
        lat, long, zoom, size[0], size[1], apiKey)
    
    reqGet = requests.get(url)
    
    image = reqGet.content
    file = open("sample_image.png", "wb")
    file.write(image)
    file.close()

# Main Program Start
getMap()

#dataFile = './test_out.csv'
#df = parseCSV(dataFile)
#df.to_csv('./test_out_parse.csv')