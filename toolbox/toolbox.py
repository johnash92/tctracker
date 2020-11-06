'''
Number of tools which are required for tc_tracker.
Contents:
 - box_constraint(minlat,minlon,maxlat,maxlon):
       Creates iris constraint on latitude and longitude. Four coordinates required.
 - haversine_d(lat1,lat2,lon1,lon2):
       Calculates distnace between lat/lon coordinates.
- radians(x):
       Convers degrees to radians.
'''
import numpy as np

def box_constraint(minlat,maxlat,minlon,maxlon):
    import iris
    # Create constraint to extract data from cube over a certain region
    longitude_constraint1=iris.Constraint(longitude = lambda cell:cell>minlon)
    longitude_constraint2=iris.Constraint(longitude = lambda cell:cell<maxlon)
    latitude_constraint1=iris.Constraint(latitude = lambda cell:cell>minlat)
    latitude_constraint2=iris.Constraint(latitude = lambda cell:cell<maxlat)
    box_constraint=longitude_constraint1&longitude_constraint2&latitude_constraint1&latitude_constraint2
    return box_constraint


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
