'''
Tropical cyclone tracking program V 1.0.0

This program tracks a tropical cyclone using data in a .pp file. The data
produced is the following:
 - Track
 - Maximum 10m windspeed
 - Minimum sea level pressure

Default is to use 3 hourly timesteps. Each of the metrics is treated separately
using their relevant scripts. They all use techniques which have been tested and
found to be the most accurate.

Optionally can input best track data. All data produced is saved, can also be
optionally plotted.

                                    John Ashcroft, Uni. of Leeds, September 2018
'''
import iris
import numpy as np
from load_data import * 

def main():
    # Location and name of input data (.pp files).
    pp_loc = '/nfs/a319/scjea/large_ensemble/tracking_data/'
    pp_file = 'tcver3hr_bigensemble_1203_12Z_em00.pp'

    # Location of best track data. If inputting best track data change
    # 'best_track_data' to 1, otherwise keep at 0. Best track data should, as a
    # minimum include the location of the storm at timestep - 1.
    best_track_data = 0 # Change to 0 if no best track is available.
    best_track_loc = ''
    best_track_file = ''

    # Output location
    outfile_loc = ''

    # Tracker will automatically calculate the mslp and (if data is available)
    # the maximum windspeed. If you would not like this to be the case change
    # the following values to 0.
    calc_mslp = 1
    calc_maxswpeed = 1
    # Load the data that will be needed for the tracker.
    pp_df = pp_loc + pp_file
    cubes = load_data(pp_df,load_10mwspeed=calc_maxswpeed)

    # 

    # First of all find the track of the storm. This can be done a number of
    # ways. For now we use the pressure centroid technique (see pc_track)

    slp = cubes['slp']
    print slp

    coords = pc_track(slp)




if __name__=='__main__':
    main()
