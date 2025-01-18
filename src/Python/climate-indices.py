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

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime
from scipy import stats as st
from tqdm import tqdm

import climate_V2

# from distributed import Client
# from dask.distributed import Client
# client = Client(n_workers=4, threads_per_worker=1, memory_limit='1GB')
# client.close()
import warnings
warnings.filterwarnings('ignore')

# cld = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.cld.dat.nc')
# dtr = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.dtr.dat.nc')
# frs = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.frs.dat.nc')
# pet = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pet.dat.nc')
# pre = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
# tmn = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmn.dat.nc')
# tmp = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmp.dat.nc')
# tmx = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmx.dat.nc')
# vap = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.vap.dat.nc')
# wet = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.wet.dat.nc')

# temperature = 'C:/Netcdf/ERA5-post-processed-daily-statistics-on-single-levels-from-1940-to-present-tmp.nc'
# precipitation = 'C:/Netcdf/ERA5-post-processed-daily-statistics-on-single-levels-from-1940-to-present.nc'
# precipitation = 'C:/Netcdf/TH_precipitation_day-1940.nc'
# precipitation = 'C:/Netcdf/convert_precipitation.nc'
# precipitation = 'C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc'
precipitation = 'C:/Netcdf/TH_precipitation_day_1960-2022.nc'
max_temperature = 'C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc'
min_temperature = 'C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc'
temperature = 'C:/Netcdf/TH_temperature_day_1940-2024.nc'

# da_data = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
# ds_RR = da_data['pre']
# # ds_RR_Thailand= ds_RR.sel(lon=slice(96, 106), lat=slice(4, 21),time='1901')
# ds_RR_Thailand= ds_RR.sel(lon=slice(96, 106), lat=slice(4, 21),time=slice('2015', '2018'))

# i=3
# test = climate_V2.Climate(ds_RR_Thailand)
# ddata = test.calculate_spi(thresh=i,dimension='time',precip_var='pre')
# da_data['spi_3'] = ddata[9]
# # ddata[9].plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
# da_data['spi_3'].sel(lon=slice(96, 106), lat=slice(4, 21), time='2016').plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
# # plt.ylim(0,15)
# # plt.xlim(-20,15)
# plt.show()



# pr = xr.open_dataset(precipitation)
# pre = pr.tp
# rx1day = xclim.indices.max_1day_precipitation_amount(pre, freq="YS")
# # print(rx1day['time'])
# print(rx1day.sel(time='1960-01-01'))

temp = xr.open_dataset(temperature)
print(temp['t'])
xclim.indices.daily_temperature_range(temp.t, )