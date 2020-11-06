from bs4 import BeautifulSoup
import datetime as dt
import numpy as np
from netcdf4 import Dataset, num2date
import urllib2


class IbtracsNamedStorm:
    def __init__(self,name,year=0):
        self.serial, self.storm_index = self._find_serial_number(name,year)
        self.year = self.serial[0:4]
        self.name = name.upper()
        df = './ibtracs_all.nc'
        tc_data = Dataset(df)
        self.lats = tc_data.variables['lat'][self.storm_index]
        self.lons = tc_data.variables['lon'][self.storm_index]
        self.mslp = tc_data.variables['wmo_pres'][self.storm_index]
        self.wind = tc_data.variables['wmo_wind'][self.storm_index]
        time_unit = tc_data.variables['time'].units
        mask = tc_data.variables['time'][self.storm_index].mask
        indexs = np.argwhere(mask==False)
        time = tc_data.variables['time'][self.storm_index].astype(object)
        for idx in indexs:
            t = num2date(time[idx],time_unit)#.replace(microsecond=0)
            time[idx] = t
        self.time = time

    def _find_serial_number(self,name,year):
        url = 'https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/'
        resp = urllib2.urlopen(url)
        soup=BeautifulSoup(resp,from_encoding=resp.info().getparam('charset'))
        for link in soup.find_all('a',href=True):
            if "SerialNumber" in link['href']:
                new_url = url + link['href']
                break
        data = urllib2.urlopen(new_url)
        years = []; serial_nos = []; SIDs = []
        storm_id = 0
        for line in data:
            if name.upper() in line:
                yr = line[0:4]
                id = line[0:13]
                years.append(int(yr)); serial_nos.append(id);
                SIDs.append(storm_id)
            storm_id+=1
        if year==0 and len(years) > 1:
            print('Multiple storms found. Provide the year from the following:')
            for y in years:
                print(y)
            exit()
        elif len(years) == 0:
            print('Storm not found, check name ({0}).'.format(name))
            exit()
        elif len(years) == 1:
            return serial_nos[0], SIDs[0]
        else:
            return serial_nos[years.index(year)], SIDs[years.index(year)]

    def plot_track(self,ax):
        ax.plot(self.lons,self.lats,linewidth=2)
        day_index = np.argwhere(self.time.hours==0)
        ax.scatter(self.lons[day_index],self.lats[day_index],'ko',markersize=10)


storm = IbtracsNamedStorm('haiyan',year=2013)
print(storm)