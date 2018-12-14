'''
Given a wind field script will find the initial position(s)
of a tropical cyclone using a predefined relative vorticity
boudnary.
                                John Ashcroft, January 2019
'''

def find_tc(vrt):
    TCboundary = 6e-6 # Limit for which we look for TCs
    TC_rad = 4. # In degrees size of box to mask. (Should be rough storm rad)
    # 1. Check the correct data has been given.
    if len(vrt.coord('pressure').points) > 1:
        p_constraint = iris.Constraint(pressure=850)
        vrt = vrt.extract(p_constraint)
    print('Searching for Tropical Cyclones using \n {0}'.format(vrt))
    tc_found = True
    while tc_found:
        max_vrt = np.amax(vrt.data)
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
            
