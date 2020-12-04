class basinList():    
    def __init__(self):
        basins = {
            'NorthAtlantic' : [0,70,-100,30],
            'EasternPacific' : [0,70,-180,-100],
            'SouthIndian' : [-70,0,10,135],
            'SouthPacific' : [-70,0,135,290],
            'SouthAtlantic' : [-70,0,-70,10],
            'NorthIndian' : [0,70,30,100],
            'WesternPacific' : [0,70,100,180]
            }
        self.basins = basins
    
    def locateBasin(self,lat,lon):
        for basin,coord in self.basins.items():
            if (lat < coord[1]) and (lat > coord[0]) \
            and (lon < coord[3]) and (lon > coord[2]):
                return basin
    
    def getCoords(self,basin):
        if basin in self.basins:
            return self.basins[basin]


