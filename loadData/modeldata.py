'''
Loads required iris cubes. Not the methods should be defined in intput file

Possible methods:
    press_centroid (pressure centroid)
    min_slp (minimum sea level pressure)
'''

import iris 

stash_codes = {
        'slp'   :'m01s16i222',
        'uplev' :'m01s15i201',
        'vplev' :'m01s15i202',
        'u10'   :'m01',
        'v10'   :'m01'
        }

standard_names = {
        'slp'   :'slp',}

methods = ['press_centroid','min_slp']

lat_constraint1 = iris.Constraint(latitude = lambda cell: cell > -40.)
lat_constraint2 = iris.Constraint(latitude = lambda cell: cell < 40.)

class inputpars(object):
    
    def __init__(self,df):
        self.get_fnames(df)
    
    def get_fnames(self,df):
        
        with open(df) as f:
            for line in f:
                fields = line.split('=')
                if fields[0].strip() == 'method':
                    self.method = fields[1].strip()
                elif fields[0].strip() == 'dataloc':
                    self.dlocs = fields[1].strip().split(',')
        self.num_dlocs = len(self.dlocs)
        
        if self.method not in methods:
            raise Exception("Incorrect method: ",self.method)
        
        if self.method == 'press_centroid':    
            self.pressurecentroid_inputs()
        
    def pressurecentroid_inputs(self):
        self.numcubes = 1
        self.stash_codes = [stash_codes['slp']]
        self.name = [standard_names['slp']]
        self.vars = ['slp']
        

def loadcubes(df='./input_files.txt'):
    
    input_params = inputpars(df)
    if input_params.num_dlocs == 1:
        input_params.dlocs = input_params.dlocs * input_params.num_dlocs
    elif input_params.num_dlocs != input_params.numcubes:
        raise Exception("Number of data fields and number of data locations "\
                        +"do not match")
        
    cube_dict = {}
    for dloc, stash, std_name in zip(input_params.dlocs,
                                     input_params.stash_codes,
                                     input_params.name):
        stash_constraint = iris.AttributeConstraint(STASH=stash)
        try:
            cube = iris.load_cube(dloc,stash_constraint).extract(lat_constraint1&lat_constraint2)
        except:
            try:
                cube = iris.load_cube(dloc,std_name).extract(lat_constraint1&lat_constraint2)
            except:
                raise Exception("Unable to load cube. Check filename: ", dloc)        
        cube_dict[std_name] = cube
    return cube_dict
    












        


def load_model_data(df,load_10mwspeed=1,load_850windspeed=1):
    '''
    Load data as cubes and return as dictionary of cubes. If load_10mwspeed
    or load_850windspeed = 0 then these will not be loaded.
    '''
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
