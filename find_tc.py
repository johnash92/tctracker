'''
Assuming that there is no analysis time for the TC (i.e. an initial observed
position is not already known), this script locates a storm given the 850hPa
relative vorticity field and the sea level pressure. For a storm to be tracked
it must follow the following criteria outlined in Heming (2017):
 (1) 850hPa relative vorticity > predetermined value
 (2) MSLP within local maximum of relative vorticity (where the max satisfies
     (1)) must be below a predetermined value.
 (3) Must pass a closed isobar check (i.e. it must have bigger values of slp
     in 8 each of the 8 points surrounding it).
 (4) It must be equatorwards of 37.5 deg (no mid latitude cyclones).
 (5) The TC must be very close to sea points in the model # Note this is not yet
     yet implemented).
 (6) The TC centre must be over the sea with analysed SST greater than a certain
     threshold. # Note this is not yet implemented.
Number (5) and (6) are not implemented at the moment, this may mean that some
developments over land are tracked, but this would be a rare occurance.
                                John Ashcroft, January 2019
'''

def find_tc(vrt,slp):
    # Check the units of relative vorticity - UM output is scaled by a factor of
    # 1e6.
    if np.amax(vrt.data) > 1.0e-1:
        vrt.data *= 1.0e-6

    TCboundary = 6e-6 # Tropical disturbance threshold
    TC_rad = 4. # In degrees size of box to mask. (Should be rough storm rad)

    # 1. Check the correct data has been given.
    if len(vrt.coord('pressure').points) > 1:
        p_constraint = iris.Constraint(pressure=850)
        vrt = vrt.extract(p_constraint)

    print('Searching for Tropical Cyclones using \n {0}'.format(vrt))
    tc_found = True
    while tc_found:
        max_vrt = np.amax(vrt.data)
        tc_found = check_vrt(vrt)


        if max_vrt > TCboundary:
            # i.e. storm found - record coordinates and mask for future
            # searches.
            lats = vrt.coord('latitude').points
            lons = vrt.coord('longitude').points
            LATS, LONS = np.meshgrid(lats,lons)
            idx = np.argmax(vrt.data)
            loc_lat = vrt.coord('latitude').points[idx[0]]
            loc_lon = vrt.coord('longitude').points[idx[1]]

            vrt.data = np.ma.masked_where((LATS > loc_lat-tc_rad))
            vrt.data = np.ma.masked_where((LATS > loc_lat+tc_rad))
            vrt.data = np.ma.masked_where((LONS > loc_lon-tc_rad))
            vrt.data = np.ma.masked_where((LONS > loc_lon+tc_rad))


def chack_vrt(max_vrt,threshold):
    '''
    Check vorticity is above the predetermined threshold.
    '''
    if max_vrt > threshold:
        return True
    else:
        print('Vorticity below limit, no disturbance found.')


def check_mslp():

def
