import iris

def loadIrisCube(df, attributeConstraint=None, dataConstraints=None):
    if attributeConstraint is not None:
        if dataConstraints is not None:
            cube = iris.load_cube(df,attributeConstraint)\
                .extract(dataConstraints)
        else:
            cube = iris.load_cube(df,attributeConstraint)
    else:
        if dataConstraints is not None:
            cube = iris.load_cube(df).extract(dataConstraints)
        else:
            cube = iris.load_cube(df)
    return cube

def find_init_guess(df,yr,mth,day,time):
    '''
    Find the location of the storm according to ibtracs data at the time determined
    my monthday (mmdd) and time (hh).
    '''
    from netCDF4 import Dataset
    from netCDF4 import num2date
    import datetime as dt
    import numpy as np
    dataset = Dataset(df)
    lats =  dataset.variables['lat_wmo'][:]
    lons = dataset.variables['lon_wmo'][:]
    times = num2date(dataset.variables['time_wmo'][:],dataset.variables['time_wmo'].units)
    times[:] = [t.replace(microsecond=0) for t in times]
    tgt_dt = dt.datetime(yr,mth,day,time)
    idx = np.where(times==tgt_dt)
    lat = lats[idx]; lon = lons[idx]
    return [lat[0],lon[0]]
