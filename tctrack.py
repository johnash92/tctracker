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
from loaddata import modeldata as md
from tracker import trackingdata
from tracker import initpos

def main():
    
    tracker_data = md.loadcubes()
    
    ## To do: find start points
    cenlats, cenlons = initpos.find_minslp(tracker_data['slp'])
    
    for cenlat, cenlon in zip(cenlats, cenlons):
        track = jdfk()
        track.dlkfjlk
    
    print(tracker_data)
    return


























    # Location of best track data. If inputting best track data change
    # 'best_track_data' to 1, otherwise keep at 0. Best track data should, as a
    # minimum include the location of the storm at timestep - 1.
    best_track_data = 0 # Change to 0 if no best track is available.
    best_track_loc = '/nfs/a37/scjea/plot_scripts/tc_analysis/intensity_track/ibtracs/'
    best_track_file = 'hagupit_ibtracs2.nc'

    # Output location
    outfile_loc = '/nfs/a319/scjea/new_trackdata/'
    outfile_name = 'bigens_pctrack_1203_12Z_em00.npy'
    outfile = outfile_loc + outfile_name
    # Tracker will automatically calculate the mslp and (if data is available)
    # the maximum windspeed. If you would not like this to be the case change
    # the following values to 0.
    calc_mslp = 1
    calc_maxswpeed = 1
    # Load the data that will be needed for the tracker.
    pp_df = pp_loc + pp_file
    cubes = load_model_data(pp_df,load_10mwspeed=calc_maxswpeed)
    slp = cubes['slp']
    u10 = cubes['u10m']
    v10 = cubes['v10m']

    dt = 3. # NEED TO CHANGE THIS - should be automatically found

    # First of all find the track of the storm. This can be done a number of
    # ways. For now we use the pressure centroid technique (see pc_track).

    # First step is to find an initial guess. This is done via the function,
    # however we first need to the date and time fo the forecast.
    fc_time = slp.coord('forecast_reference_time').points
    time_unit = slp.coord('forecast_reference_time').units
    fc_yr = time_unit.num2date(fc_time)[0].year
    fc_mth = time_unit.num2date(fc_time)[0].month
    fc_day = time_unit.num2date(fc_time)[0].day
    fc_hr = time_unit.num2date(fc_time)[0].hour

    best_track_df = best_track_loc + best_track_file
    [init_lat,init_lon] = find_init_guess(best_track_df,fc_yr,fc_mth,fc_day,fc_hr)
    print("Initial search position: ({0}, {1})".format(init_lat,init_lon))
    tcver_data = pc_tracker(slp,u10,v10,init_lat,init_lon,dt=dt)
    print("Saving track data...")
    np.save(outfile,tcver_data)
    print("It works!")
    



if __name__=='__main__':
    main()
