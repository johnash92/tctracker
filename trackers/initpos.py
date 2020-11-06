import numpy as np

def find_minslp(slp,onestorm=True):

    if onestorm:    
        indexs = np.where(slp.data == np.min(slp.data))
        cenlat = slp.coord('latitude').points[indexs[0]]
        cenlon = slp.coord('longitude').points[indexs[1]]
        return cenlat, cenlon
    else:
        cenlats = []; cenlons = []
        min_slp = np.min(slp.data)
        while min_slp < 95000:
            indexs = np.where(slp.data == np.min(slp.data))
            cenlat = slp.coord('latitude').points[indexs[0]]
            cenlon = slp.coord('longitude').points[indexs[1]]    
            slp.data[indexs[0]-10:indexs[0]+10,indexs[1]-10:indexs[1]+10]=100000
            cenlats.append(cenlat); cenlons.append(cenlon)
        return cenlats, cenlons

            
    

