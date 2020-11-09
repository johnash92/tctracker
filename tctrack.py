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
from loadData import loadInput, loadModelData
from tcLocator import findTC
import bestTrack

INPUT_LOC = './input'

def main():
    inputs = loadInput.inputParams(inputloc=INPUT_LOC)
    if inputs.initLat == None or inputs.initLon == None:
        ibtracsTrack = bestTrack.ibtracs(name=inputs.StormName,
                                         year=inputs.StormYear)
        
    
    
    
    print(inputs.method)
    
    
    
    
    



if __name__=='__main__':
    main()
