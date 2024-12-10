import netCDF4 
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
import pandas as pd
import time
import warnings
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')
from metpy.cbook import get_test_data
# import pandas as pd

cld = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.cld.dat.nc')
dtr = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.dtr.dat.nc')
# frs = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.frs.dat.nc')
# pet = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pet.dat.nc')
pre = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pre.dat.nc')
tmn = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmn.dat.nc')
tmp = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmp.dat.nc')
tmx = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmx.dat.nc')
vap = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.vap.dat.nc')
# wet = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.wet.dat.nc')

year = 1901
data1 = cld.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
time_values1 = data1['time'].values
time_dates1 = pd.to_datetime(time_values1)
data2 = dtr.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
time_values2 = data2['time'].values
time_dates2 = pd.to_datetime(time_values2)
# data3 = frs.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
# time_values3 = data2['time'].values
# time_dates3 = pd.to_datetime(time_values3)
print(time_dates1)
print(time_dates2)
# print(time_dates3)



# Cloud-Cover
# Diural-Temperature-Range
# Ground-Frost-Frequency
# Potential-Evapotranspiration
# Precipitation
# Minimum-Temperature
# Mean-Temperature
# Maximum-Temperature
# Vapour-Pressure
# Rain-Days