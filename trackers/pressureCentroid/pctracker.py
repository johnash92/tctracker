import iris
from loadData.loadModelData import loadIrisCube
from toolbox.basins import basinList
from toolbox.cubeTools import boxConstraint

class tracker():
    def __init__(self,trackInput):
        self.dloc = trackInput.dataloc
        self.dataloc = trackInput.dataloc
        self.initLat = trackInput.initLat
        self.initLon = trackInput.initLon
        self.initTime = trackInput.time0
        self.slpStash = 'm01s16i222'
        self.uStash = 'm01s15i201'
        self.vStash = 'm01s15i202'
        self.dt = trackInput.dt
    
    def loadData(self):
        slpConstraint = iris.AttributeConstraint(STASH=self.slpStash)
        uConstraint = iris.AttributeConstraint(STASH=self.uStash)
        vConstraint = iris.AttributeConstraint(STASH=self.vStash)
        hrdtConstraint = iris.Constraint(forecast_period = lambda cell: cell % 3 == 0)
        self._getBasinConstraint(self.initLat,self.initLon)
        attrConstraint = self.basinConstraint&hrdtConstraint
        self.slpCube = loadIrisCube(self.dataloc,
                                    attributeConstraint=slpConstraint,
                                    dataConstraints = attrConstraint)
    
    def _getBasinConstraint(self,lat,lon):
        self._findBasin(lat,lon)
        self.basinConstraint = boxConstraint(self.basinCoords)
        
    def _findBasin(self,lat,lon):
        self.basin = basinList().locateBasin(lat,lon)
        self.basinCoords = basinList().getCoords(self.basin)
        
    def _set_dt(self):
        if not self.dt == None:
            print('TODO - set dt')
   
    def trackStorm(self):
        self.currTime = self.initTime
        self._setFinalTime()
        self.latList = []
        self.lonList = []
        self.initLonGuess = self.initLon
        self.initLatGuess = self.initLat
        self.changingR = False #TODO change this, should be using R80
        
        for slp_slc in self.slpCube.slices(['latitude','longitude']):
            
        
        
        
        
        
        
        
        
        
        
