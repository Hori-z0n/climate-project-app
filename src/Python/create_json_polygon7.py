import pandas as pd
import geopandas as gpd
from scipy import stats as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import tqdm
import xarray as xr
import warnings
warnings.filterwarnings('ignore')

start_year = 1901
stop_year = 1901
start_month = 1
stop_month = 12

ds = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
print(len(ds['time'].values))

for i in range(0, 13):
    print(ds['time'][i].values)

# for year in range(start_year, stop_year+1):
#     print('\n')
#     value = []
#     path = f'C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/Year-Dataset/data_{year}.json'
#     data = gpd.read_file(path)
# print(pre['stn'][0]['time'])
# print(pre['stn'][0].values)
# for i in pre['stn'][0].values:
#     print(i)
# stations = 8

# data_var = ds.metpy.parse_cf('stn')
# x = data_var.lon
# y = data_var.lat
# im_data = data_var.isel(time=1)

# fig = plt.figure(figsize=(64, 64))
# ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
# mp = ax.imshow(im_data, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# plt.tight_layout()

# plt.show()