'''
Number of tools which are required for tc_tracker.
Contents:
 - haversine_d(lat1,lat2,lon1,lon2):
       Calculates distnace between lat/lon coordinates.
- radians(x):
       Convers degrees to radians.
'''
import numpy as np

def haversine_d(lat1, lat2, lon1, lon2):
# Calculates the distances between two points given in lat and lon coords
    r = 6.37e6
    lat1 = radians(lat1); lat2 = radians(lat2)
    lon1 = radians(lon1); lon2 = radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    d = 2*r*np.arcsin(np.sqrt(np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2))
    return d

def radians(x):
    x = np.pi * x / 180
    return x
