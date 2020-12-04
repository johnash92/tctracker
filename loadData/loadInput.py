class inputParams:
    def __init__(self,inputloc='./input',dataloc=None,stormName=None,stormYear=None,
                 initLat=None,initLon=None,findAll=None): 
        
        f = open(inputloc,"r")        
        input_dict = {}
        for line in f:
            (key, value) = line.strip().split('=')
            input_dict[key] = value
        
        try:
            self.dataloc = input_dict['dataloc']
        except KeyError:
            raise ValueError('Data location not found.')

        try:
            self.method = input_dict['method']
        except KeyError:
            raise ValueError('Method not defined.')

        if 'stormname' in input_dict:
            self.stormName = input_dict['stormname']
        if 'stormyear' in input_dict:
            self.stormYear = int(input_dict['stormyear'])
        if 'initlat' in input_dict:
            self.initLat = input_dict['initlat']
        else:
            self.initLat = None
        if 'initlon' in input_dict:
            self.initLon = input_dict['initlon']
        else:
            self.initLat = None
        if 'findall' in input_dict:
            self.findAll = input_dict['findall']
        if 'inittime' in input_dict:
            self.inittime = input_dict['inittime']