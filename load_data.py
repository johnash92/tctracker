'''
This script loads data for the tctracker using the input datafile. Data is
stored in iris cubes. It is assumed that the following is required:
 - Sea level pressure
 - 10m (u,v)
 - 850hPa (u,v)
It is used with the tctracker code.
'''

def load_data(df,load_10mwspeed=1,load_850windspeed=1):
    '''
    Load data as cubes and return as dictionary of cubes. If load_10mwspeed
    or load_850windspeed = 0 then these will not be loaded.
    '''
    import iris
    cubes = dict() # Dictionary to add loaded data to.
    slp_stash = 'm01s16i222' # unique code for sea level pressure
    slp_constraint = iris.AttributeConstraint(STASH=slp_stash)
    slp = iris.load_cube(df,slp_constraint)
    cubes['slp'] = slp
    if load_10mwspeed:
        u_stash = 'm01s03i225' # unique code for 10m u (and below for 10m v)
        v_stash = 'm01s03i226'
        u_constraint = iris.AttributeConstraint(STASH=u_stash)
        v_constraint = iris.AttributeConstraint(STASH=v_stash)
        u10m = iris.load_cube(df,u_constraint)
        v10m = iris.load_cube(df,v_constraint)
        cubes['u10m'] = u10m; cubes['v10m'] = v10m

    if load_850windspeed:
        u_stash = 'm01s15i201' # Stash codes for (u,v) on pressure levels
        v_stash = 'm01s15i202'
        p_constraint = iris.Constraint(pressure=850) # Limit (u,v) to 850hPa
        u_constraint = iris.AttributeConstraint(STASH=u_stash)
        v_constraint = iris.AttributeConstraint(STASH=v_stash)
        u850 = iris.load_cube(df,u_constraint).extract(p_constraint)
        v850 = iris.load_cube(df,v_constraint).extract(p_constraint)
        cubes['u850'] = u850; cubes['v850'] = v850

    return cubes 
