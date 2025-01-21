# https://github.com/shiv3679/climate-indices
# https://github.com/monocongo/climate_indices
# https://github.com/KWRProjects/Meteorology-climate_indices
# https://github.com/KNMI/Indices_icclim_ClipC
# https://github.com/SantanderMetGroup/climate4R.indices
# https://github.com/XiaZhang1113/indices_python
# https://github.com/jeffjay88/Climate_Indices
# https://github.com/fmidev/resiclim-climateatlas
# https://github.com/monocongo/climate_indices/blob/master/docs/index.rst
# https://github.com/gabrielmpp/climate_indices
# https://github.com/topics/climate-indicators
# https://github.com/Climandes/ClimIndVis
# https://github.com/Ouranosinc/mat-clim-indices
# https://github.com/AgrDataSci/climatrends
# https://github.com/nicolasfauchereau/ACRE_workshop
# https://github.com/cerfacs-globc/icclim
# https://github.com/ARCCSS-extremes/climpact2/blob/master/ancillary/climate.indices.csv
# https://github.com/AusClimateService/indices
# https://github.com/ECA-D/gridclimind
# https://github.com/yyr/climate_indices
# https://github.com/drewpolasky/simple_pyclimdex
# https://climate-indices.readthedocs.io/en/latest/
# https://github.com/Ouranosinc/xclim
# https://scholar.google.com/citations?user=awGdXUsAAAAJ&hl=en

import climate_indices
import climate_library
from climate_library.climate_index import ClimateIndex

import xclim
import xclim.indices
# import xclim.core.units as xu
from xclim.testing import open_dataset
# from xclim.indices import standardized_precipitation_index
# from xclim.indices.stats import standardized_index_fit_params
from xclim.core.calendar import percentile_doy

import pandas as pd
import geopandas as gpd
# from netCDF4 import Dataset
import netCDF4 as nc

import xarray as xr
import numpy as np
import json
from tqdm import tqdm 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime
from scipy import stats as st
from tqdm import tqdm

from shapely.geometry import mapping

import climate_V2
from province import province_coord

# from distributed import Client
# from dask.distributed import Client
# client = Client(n_workers=4, threads_per_worker=1, memory_limit='1GB')
# client.close()
import warnings
warnings.filterwarnings('ignore')

# shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')

cld = 'C:/Netcdf/cru_ts4.08.1901.2023.cld.dat.nc'
dtr = 'C:/Netcdf/cru_ts4.08.1901.2023.dtr.dat.nc'
frs = 'C:/Netcdf/cru_ts4.08.1901.2023.frs.dat.nc'
pet = 'C:/Netcdf/cru_ts4.08.1901.2023.pet.dat.nc'
pre = 'C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc'
tmn = 'C:/Netcdf/cru_ts4.08.1901.2023.tmn.dat.nc'
tmp = 'C:/Netcdf/cru_ts4.08.1901.2023.tmp.dat.nc'
tmx = 'C:/Netcdf/cru_ts4.08.1901.2023.tmx.dat.nc'
vap = 'C:/Netcdf/cru_ts4.08.1901.2023.vap.dat.nc'
wet = 'C:/Netcdf/cru_ts4.08.1901.2023.wet.dat.nc'

# temperature = 'C:/Netcdf/ERA5-post-processed-daily-statistics-on-single-levels-from-1940-to-present-tmp.nc'
# precipitation = 'C:/Netcdf/ERA5-post-processed-daily-statistics-on-single-levels-from-1940-to-present.nc'
# precipitation = 'C:/Netcdf/TH_precipitation_day-1940.nc'
# precipitation = 'C:/Netcdf/convert_precipitation.nc'
# precipitation = 'C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc'
precipitation = 'C:/Netcdf/TH_precipitation_day_1960-2022.nc'
max_temperature = 'C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc'
min_temperature = 'C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc'
temperature = 'C:/Netcdf/TH_temperature_day_1940-2024.nc'

shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

# ds = xr.open_dataset(tmp)
# print(ds['tmp'].attrs)
# ds = xr.open_dataset(temperature)
# ds = ds.rename(t='t2m')
# ds = ds.rename(valid_time='time')
# ds['t2m'].attrs['units'] = 'C'
# ds['t2m'].values - 273.15
# ds.to_netcdf('TH_temperature_day_1940-2024.nc')

ds = xr.open_dataset(temperature)
# temp = ds.sel(time=slice('2000-01-01', '2000-12-31')).t2m
# ds = ds.sel(time=slice('2000-01-01', '2000-12-31'))
temp = ds.t2m
print(temp)
tasmax_per = percentile_doy(temp, per=10).sel(percentiles=10)
cold_days = xclim.indices.tx10p(temp, tasmax_per)
print(cold_days)
cold_days.plot()
plt.show()
# climate_index = ClimateIndex(tmp)
# climate_index = ClimateIndex(max_temperature)
# climate_index.pre_process(time_range=('1901-01-01', '1902-12-31'), resample_freq='M', fill_missing='interpolate')
# climate_index.pre_process(time_range=('2000-01-01', '2000-12-31'), resample_freq='D', fill_missing='interpolate')
# print(climate_index.data.indexes)
# tx10p_index = climate_index.calculate_tx10p(temp_var='mx2t')
# print(tx10p_index)


# temp = xr.open_dataset(temperature)
# max_temp = xr.open_dataset(max_temperature)
# min_temp = xr.open_dataset(min_temperature)

# print(temp['t'])
# xclim.indices.daily_temperature_range(min_temp, max_temp, freq="YS", op="mean")


