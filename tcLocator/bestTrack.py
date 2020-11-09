import requests
import re
from bs4 import BeautifulSoup
from netCDF4 import Dataset, num2date
import os.path
import numpy as np
import datetime as dt

URL = 'https://www.ncei.noaa.gov/data/' +\
        'international-best-track-archive-for-climate-stewardship-ibtracs/'
# 'v04r00/access/csv/'

class ibtracsNamedStorm:
    
    def __init__(self, stormName=None,stormYear=None):
        try:
            self.stormName = str(stormName)
        except:
            raise Exception("No storm name provided")
        self.stormYear = stormYear 
        self.getStormData()
        
    def getSerialNumber(self):
        r = requests.get(self.DATAURL)
        soup = BeautifulSoup(r.content,'lxml')
        for link in soup.find_all('a',href=True):
            if "SerialNumber" in link['href']:
                self.SERIALURL = self.DATAURL + link['href']
                break
        r = requests.get(self.SERIALURL)
        years = []; SIDs = []
        for line in r.text.splitlines():
            if self.stormName.upper() in line:
                yr = line[0:4]
                stormID = line[0:13]
                years.append(int(yr)); 
                SIDs.append(stormID)
        
        if self.stormYear==None and len(years) > 1:
            raise Exception ('Please provide a storm year, options: {0}'.format(years))
        elif len(years) == 0:
            raise Exception('Storm not found, check name ({0}).'.format(self.stormName))
        elif len(years) == 1:
            self.serialNo = SIDs[0];
        else:
            self.serialNo = SIDs[years.index(self.stormYear)]
        
    def getLatestVersion(self):
        r = requests.get(URL)
        versionStrings = re.findall('>v(\d+)r(\d+)',r.text)
        versions = []
        for ver in versionStrings:
            v = 100 * int(ver[0]) + int(ver[1])
            versions.append(v)
        max_v = max(versions)
        self.versStr = 'v{0:02d}r{1:02d}'.format(max_v//100,max_v%100)
        self.BASEURL = URL + self.versStr
        self.DATAURL = self.BASEURL + '/access/csv/'
        
    def downloadIBTrACS(self):
        besttrack_df = '../Data/IBTrACS_all_{0}.nc'.format(self.versStr)
        if os.path.exists(besttrack_df):
            return
        else:
            print('Downloading best track data...')
            NETCDFURL = self.BASEURL + '/access/netcdf/IBTrACS.ALL.' +\
                        self.versStr + '.nc'
            r = requests.get(NETCDFURL,allow_redirects=True)
            open(besttrack_df,"wb").write(r.content)
    
    def getStormData(self):
        self.getLatestVersion()
        self.getSerialNumber()
        self.downloadIBTrACS()
        besttrack_df = '../Data/IBTrACS_all_{0}.nc'.format(self.versStr)
        tc_data = Dataset(besttrack_df)
        
        storm_id_list = [bytes_to_str(i) for i in tc_data['sid'][:]]
        indices = [i for i,s in enumerate(storm_id_list) if self.serialNo in s]
        self.stormIndex = indices[0]
        time_unit = tc_data.variables['time'].units        
        mask = tc_data.variables['time'][self.stormIndex].mask
        indexs = np.argwhere(mask==False)
        time = tc_data.variables['time'][self.stormIndex].astype(object)
        calendar = tc_data.variables['time'].calendar
        for idx in indexs:
            hrs = int((time[idx][0]%1) * 3//0.125)
            t = num2date(time[idx],time_unit,calendar)#.replace(microsecond=0)
            t[0] += dt.timedelta(hours=hrs)
            time[idx] = t
        storm_data = {
                'lats' : tc_data.variables['lat'][self.stormIndex],
                'lons' : tc_data.variables['lon'][self.stormIndex],
                'mslp' : tc_data.variables['wmo_pres'][self.stormIndex],
                'maxws' : tc_data.variables['wmo_wind'][self.stormIndex],
                'time':time
                }
        self.stormData = storm_data
        
    def locateStorm(self,time):
        if time.hour % 6 == 0 :
            index = np.argwhere(self.stormData['time']==time)
            lat = self.stormData['lats'][index[0][0]]
            lon = self.stormData['lons'][index[0][0]]
            return [lat,lon]
        else:
            diff = time.hour % 6 # TODO: change to allow for different dts
            next_time = time + dt.timedelta(hours=diff)
            prev_time = time - dt.timedelta(hours=diff)
            prev_index = np.argwhere(self.stormData['time']==prev_time)
            next_index = np.argwhere(self.stormDeta['time']==next_time)
            prev_lat = self.stormData['lats'][prev_index[0][0]]
            next_lat = self.stormData['lats'][next_index[0][0]]
            prev_lon = self.stormData['lnos'][prev_index[0][0]]
            next_lon = self.stormData['lons'][next_index[0][0]]
            lat = ((6-diff) / 6.) * prev_lat + (diff / 6.) * next_lat
            lon = ((6-diff) / 6.) * prev_lon + (diff / 6.) * next_lon
            return [lat,lon]
        
def bytes_to_str(arr):
    string = ''
    for a in arr:
        string += a.decode('utf-8')
    return string

