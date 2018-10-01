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

def pc_tracker(slp,lat0,lon0,dt=3):
    # First make sure we only have the data we want according to the timestep
    # dt
    hour_dt = iris.Constraint(time= lambda cell: cell.point.hour % 3 ==0 and cell.point.minute==0)
    with iris.FUTURE.context(cell_datetime_objects=True):
        slp = slp.extract(hour_dt)

    # Initialise the previous coordinates as our initial guess. According to the
    # specified condition if the new lcoation does not move far enough than
    # function will end and new coords will be returned.
    prevlat = lat0; prevlon = lon0
    minlat = prevlat - 5; maxlat = prevlat + 5;
    minlon = prevlon - 5; maxlon = prevlon + 5
    b_constraint = box_constraint()
