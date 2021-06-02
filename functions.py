import streamlit as st
import pandas as pd
import numpy as np
import heapq
from geopy.geocoders import Nominatim
import geopy.distance
import re
import csv
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

def convert_address(address):
	geolocator = Nominatim(user_agent="my_app")
	Geo_Coordinate = geolocator.geocode(address)
	lat = Geo_Coordinate.latitude
	lon = Geo_Coordinate.longitude
	point = (lat, lon)
	return point


def route_finder(loc, hills, loop, least, most, df):

    loop_dict = {'Yes':1, 'No':0}

    hill_dict = {'Little to none':('min','50%'),\
                 'Moderate': ('25%', '75%'),\
                 'Intense': ('75%', 'max'),\
                 'No preference': ('min', 'max')}
    
    X = df[(df['miles'] >= least) & (df['miles'] <= most)]
    if X.empty:
        return 'No routes with those mile specifications.'

    if loop!='Either':
        loop_val = loop_dict[loop]
        X = X[X['is_loop'] == loop_val]
        if X.empty:
            return 'No routes with those mile and round trip specifications.'

    hill_min, hill_max = hill_dict[hills]
    hill_stats = X['num_hills'].describe()
    hill_min_val = hill_stats[hill_min]
    hill_max_val = hill_stats[hill_max]

    X = X[(X['num_hills'] >= hill_min_val) & (X['num_hills'] <= hill_max_val)]

    return best_routes(loc, X)

def best_routes(loc, df):
    n = min(5, df.shape[0])
    points = df[['ID','l1','l2','l3','l4','l5','l6','l7','l8','l9','l10']]
    

    closest_routes = heapq.nlargest(n, points.values, key=lambda x: -(point_min(x, loc)[1]))

    route_info = list(map(lambda x: [x[0], point_min(x,loc)[0], point_min(x,loc)[1]], closest_routes))

    return route_info
    
    
    
def point_min(arr, loc):
    arr = arr[1:]
    close_point = min(arr, key=lambda x: geopy.distance.distance(eval(x),loc).miles)
    return close_point, geopy.distance.distance(eval(close_point),loc).miles
    

def route_display(info, df):
    choices=[]
    urls = []
    i=1
    for rec in info:
        dist_from = round(rec[-1],2)
        path = df[df['ID']==rec[0]]
        dist = path['miles'].values[0]
        hills = path['num_hills'].values[0]
        gain = round(path['gain'].values[0])
        s = f'{i}. Mileage: {dist} | Elevation gain: {gain} | Hill rating: {hills} | Proximity(miles): {dist_from}'
        choices.append(s)
        urls.append(path['url'].values[0])
        i+=1
    return choices, urls

def get_lats_longs(url):    
    locPage = urlopen(url)
    soup = BS(locPage, "lxml").findAll('script',{"src":False})
    points = []
    for s in soup:
        if 'routePoints' in s.string:
            value = "[{" + s.string.split("}];")[0].split("[{")[1] + "}]"
            jsonObj = json.loads(value)
            for x in jsonObj:
                points.append((x["latitude"],x["longitude"]))
    return points
