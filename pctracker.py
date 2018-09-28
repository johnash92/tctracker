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

def pc_tracker(slp):
