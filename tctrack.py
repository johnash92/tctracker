from loadData import loadInput, loadModelData
from tcLocator import findTC, bestTrack
import datetime as dt
import trackers 

INPUT_LOC = './input.txt'

class Input(object): 
    def __init__(self,inputs=None,initLon=None,initLat=None,dt=None):
        self.method = inputs.method
        self.dataloc = inputs.dataloc
        self.initLat = initLat
        self.initLon = initLon
        self.time0 = inputs.time0
        self.dt = dt
        

def main():
    # Load input from the input.txt file
    inputs = loadInput.inputParams(inputloc=INPUT_LOC)
    inputs.time0 = dt.datetime.strptime(inputs.inittime,'%Y%m%dT%H%MZ')
    if inputs.initLat == None or inputs.initLon == None:
        ibtracsTrack = bestTrack.ibtracsNamedStorm(stormName=inputs.stormName,
                                         stormYear=inputs.stormYear)
    # Find initial guess of storm location from ibtracs
    initlat, initlon = ibtracsTrack.locateStorm(inputs.time0)
    # TODO deal withg dt better
    trackerInput = Input(inputs=inputs,initLat=initlat,initLon=initlon,dt=3)
    
    
    if trackerInput.method == 'press_centroid':
        tcTrack = trackers.pressCentroid.tracker(trackerInput)
        tcTrack.loadData()
        
        
        
    
    
    
    
    



if __name__=='__main__':
    main()
