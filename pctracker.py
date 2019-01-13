'''
Tracking method which uses a pressure centroid to find the location of the storm
at each timestep. The full method is described in Nguyen (2014). We use the same
metrics as Nguyen (2014), specifically the 2*R80 is used to define our centroid
size.

This method only calculates the central storm position. Ability to include max
windspeed and mslp may be added in future.

Only the sea level pressure is inputted (or pressure at any single level). SLP
should be an iris cube.

John Ashcroft, September 2018
'''
import iris
import numpy as np
from toolbox import *

def pc_tracker(slp,u,v,lat0,lon0,dt=3,max_disp=0.01,max_iter=50):
    # First make sure we only have the data we want according to the timestep
    # dt
    elaps_t = 0
    hour_dt = iris.Constraint(time= lambda cell: cell.point.hour % dt ==0 and cell.point.minute==0)
    with iris.FUTURE.context(cell_datetime_objects=True):
        slp = slp.extract(hour_dt)
        u = u.extract(hour_dt)
        v = v.extract(hour_dt)

    # Initialise the previous coordinates as our initial guess. According to the
    # specified condition if the new location does not move far enough than
    # function will end and new coords will be returned.
    prevlat = lat0; prevlon = lon0
    minlat = prevlat - 5; maxlat = prevlat + 5;
    minlon = prevlon - 5; maxlon = prevlon + 5
    b_constraint = box_constraint(minlat,maxlat,minlon,maxlon)

    lats = []; lons = []; mslp = []; maxws = []
    print("Starting PC Tracker")
    for slp_slc,u_slc,v_slc in zip(slp.slices(['latitude','longitude']),
                                    u.slices(['latitude','longitude']),
                                    v.slices(['latitude','longitude'])):
        ws = (u_slc**2 + v_slc**2)**0.5
        elaps_t += dt
        minlat = prevlat - 5; maxlat = prevlat + 5;
        minlon = prevlon - 5; maxlon = prevlon + 5
        b_constraint = box_constraint(minlat,maxlat,minlon,maxlon)
        slp_red = slp_slc.extract(b_constraint)
        prevlat,prevlon = find_min_coords(slp_red,rad=5)
        minslp = np.amin(slp_red.data)
        maxwinds = np.amax(ws.data)
        dlon = 1e7; dlat = 1e7;
        conditions = [dlon > 0.1, dlat > 0.1]
        num_iterations = 0
        while all(conditions):
            # Find R80 using previous guess of cenlat and cenlon
            rad = find_rad(u_slc,v_slc,prevlat,prevlon,perc=80)
            env_p = environmental_pressure(slp_slc,prevlat,prevlon)
            newlat,newlon = pressure_centroid(slp_slc,2*rad,prevlat,prevlon,env_p)
            dlon = abs(prevlon - newlon)
            dlat = abs(prevlat - newlat)
            prevlat = newlat; prevlon = newlon
            conditions = [(dlon**2 + dlat**2)**0.5 > max_disp, num_iterations < max_iter]
            num_iterations += 1
        print('T+{1}: Step complete, number of iterations = {0}'.format(num_iterations,elaps_t))
        lats.append(newlat); lons.append(newlon)
        mslp.append(minslp); maxws.append(maxwinds)
    tcver_data = dict()
    tcver_data['lats'] = lats
    tcver_data['lons'] = lons
    tcver_data['mslp'] = mslp
    tcver_data['maxws'] = maxws
    return tcver_data


def find_rad(u,v,cenlat,cenlon,perc=80):
    # Find the R80 radius (radius at which the winds are 80% of maximum)
    # Here this is done coarsely with the computation time in mind.
    # Azimuthal speed is currently used
    phis = np.arange(0,2*np.pi,np.pi / 4)
    radii = np.arange(0,200,10)
    wspeed = []
    for r in radii:
        r_speed = []
        for phi in phis:
            xpoi = cenlon + 0.009*r*np.cos(phi)
            ypoi = cenlat + 0.009*r*np.sin(phi)
            new_point = [('latitude',ypoi),('longitude',xpoi)]
            u_oi = u.interpolate(new_point,iris.analysis.Linear()).data
            v_oi = v.interpolate(new_point,iris.analysis.Linear()).data
            az_speed_oi = -u_oi * np.sin(phi) + v_oi * np.cos(phi)
            r_speed.append(az_speed_oi)
        mean_speed = np.mean(r_speed)
        wspeed.append(mean_speed)
    max_wspeed = np.amax(wspeed)
    target_speed = (max_wspeed * perc) / 100.
    tgt = [target_speed] * radii.size
    wspeed = np.asarray(wspeed)
    idx = np.argwhere(np.diff(np.sign(tgt - wspeed)) != 0).reshape(-1)
    radius = radii[idx[0]]
    return radius

def find_min_coords(cube,rad=1e10):
    # Find the latitude and longitude of the minimum value of data in a 2d cube.
    index = np.argmin(cube.data)
    indices= np.unravel_index(index,cube.data.shape)
    cenlat = cube.coord('latitude').points[indices[0]]
    cenlon = cube.coord('longitude').points[indices[1]]
    return cenlat, cenlon


def environmental_pressure(slp,y0,x0):
    # Find the average pressure 500km away from the centre of the centroid.
    phis = np.arange(0,2*np.pi + 0.1, np.pi / 16)
    slp500 = []
    for phi in phis:
        xpoi = x0 + 0.009*500*np.cos(phi)
        ypoi = y0 + 0.009*500*np.sin(phi)
        new_point = [('latitude',ypoi),('longitude',xpoi)]
        slp_oi = slp.interpolate(new_point,iris.analysis.Linear()).data
        slp500.append(slp_oi)
    mean_slp = np.mean(slp500)
    return mean_slp

def pressure_centroid(slp,rad,y0,x0,env_p):
    # Compute the new centre lat/lon according to a pressure centroid.
    dP = slp * -1.
    dP.data = dP.data + env_p # Deviation of SLP from the environment
    rad_in_deg = rad * 0.009
    minlat = y0 - rad_in_deg * 1.1; maxlat = y0 + rad_in_deg * 1.1
    minlon = x0 - rad_in_deg * 1.1; maxlon = x0 + rad_in_deg * 1.1
    b_constraint = box_constraint(minlat,maxlat,minlon,maxlon)
    red_dp = dP.extract(b_constraint)

    x_top = 0; y_top = 0
    x_bot = 0; y_bot = 0
    num_x = red_dp.coord('longitude').points.size
    num_y = red_dp.coord('latitude').points.size

    for i in np.arange(num_y):
        lat = red_dp.coord('latitude').points[i]
        for j in np.arange(num_x):
            lon = red_dp.coord('longitude').points[j]
            dist = haversine_d(lat,y0,lon,x0)
            if dist / 1000. > rad:
                continue
            press = red_dp.data[i,j]
            x_top = x_top + (lon * press); x_bot = x_bot + press
            y_top = y_top + (lat * press); y_bot = y_bot + press

    x = red_dp.coord('longitude').points
    y = red_dp.coord('latitude').points
    X,Y = np.meshgrid(x,y)
    YNEW = red_dp.copy()
    YNEW.data = red_dp.data * Y
    new_lon = x_top / x_bot
    new_lat = y_top / y_bot
    return new_lat, new_lon
