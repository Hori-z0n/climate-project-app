import netCDF4 
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
import pandas as pd
import time
import geopandas as gpd
import warnings
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')
from metpy.cbook import get_test_data
# import pandas as pd

cld = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.cld.dat.nc')
dtr = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.dtr.dat.nc')
frs = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.frs.dat.nc')
pet = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pet.dat.nc')
pre = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pre.dat.nc')
tmn = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmn.dat.nc')
tmp = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmp.dat.nc')
tmx = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmx.dat.nc')
vap = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.vap.dat.nc')
wet = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.wet.dat.nc')

data = gpd.read_file('./src/Geo-data/Year-Dataset/data_cld_1901.json') 
print(data)
# print('cld---------------------------------------------------------------------')
# print(cld['cld'].attrs['units'])
print('dtr---------------------------------------------------------------------')
print(dtr['dtr'].attrs['units'])
# print('frs---------------------------------------------------------------------')
# print(frs['frs'])
# print('pet---------------------------------------------------------------------')
# print(pet['pet'].attrs['units'])
print('pre---------------------------------------------------------------------')
print(pre['pre'].attrs['units'])
print('tmn---------------------------------------------------------------------')
print(tmn['tmn'].attrs['units'])
print('tmp---------------------------------------------------------------------')
print(tmp['tmp'].attrs['units'])
print('tmx---------------------------------------------------------------------')
print(tmx['tmx'].attrs['units'])
# print('vap---------------------------------------------------------------------')
# print(vap['vap'].attrs['units'])
# print('wet---------------------------------------------------------------------')
# print(wet['wet'])
# print('------------------------------------------------------------------------')

# # fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})
# llon = 94
# hlon = 110
# llat = 2
# hlat = 30

# fig = plt.figure(figsize=(64, 64))
# year = 2023

# start = time.perf_counter()

# # Cloud Cover
# data_var1 = cld.metpy.parse_cf('cld')

# cld['time'] = pd.to_datetime(cld['time'].values)
# data_filtered1 = cld.sel(time=slice('2022-01-01', '2023-12-31'))

# var1 = data_filtered1.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg1 = var1['cld'].mean(dim='time')
# x = var1.lon
# y = var1.lat
# ax = fig.add_subplot(2, 5, 1, projection=ccrs.PlateCarree())
# mp1 = ax.imshow(data_avg1, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp1, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Cloud Cover')



# # Diural Temperature Range
# data_var2 = dtr.metpy.parse_cf('dtr')

# dtr['time'] = pd.to_datetime(dtr['time'].values)
# data_filtered2 = dtr.sel(time=slice('2022-01-01', '2023-12-31'))


# var2 = data_filtered2.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg2 = var2['dtr'].mean(dim='time')
# x = var2.lon
# y = var2.lat
# ax = fig.add_subplot(2, 5, 2, projection=ccrs.PlateCarree())
# mp2 = ax.imshow(data_avg2, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp2, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Diural Temperature Range')



# # Ground Frost Frequency
# data_var3 = frs.metpy.parse_cf('frs')

# # frs['time'] = pd.to_datetime(frs['time'].values)
# data_filtered3 = frs.sel(time=slice('2022-01-01', '2023-12-31'))
# var3 = data_filtered3.sel(lon=slice(llon, hlon), lat=slice(llat, hlat))
# data_avg3 = var3['frs'].mean(dim='time').dt.days
# # data_avg3 = data_filtered3['frs'].mean(dim='time').dt.days
# # x = var3.lon
# # y = var3.lat
# # ax = axs

# ax = fig.add_subplot(2, 5, 3, projection=ccrs.PlateCarree())

# # mp = ax.imshow(data_avg3, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')
# # mp = ax.imshow(data_avg3, cmap='jet', origin='lower')
# mp = ax.pcolormesh(data_avg3['lon'], data_avg3['lat'], data_avg3, cmap='viridis', transform=ccrs.PlateCarree())
# # gl = ax.gridlines(draw_labels=True, alpha=0.1)
# # gl.top_labels = False
# # gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Ground Frost Frequency')


# # Potential Evapotranspiration
# data_var4 = pet.metpy.parse_cf('pet')

# pet['time'] = pd.to_datetime(pet['time'].values)
# data_filtered4 = pet.sel(time=slice('2022-01-01', '2023-12-31'))

# year = 2023
# var4 = data_filtered4.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg4 = var4['pet'].mean(dim='time')
# x = var4.lon
# y = var4.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 4, projection=ccrs.PlateCarree())
# mp = ax.imshow(data_avg4, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Potential Evapotranspiration')


# # Precipitation
# data_var5 = pre.metpy.parse_cf('pre')

# pre['time'] = pd.to_datetime(pre['time'].values)
# data_filtered5 = pre.sel(time=slice('2022-01-01', '2023-12-31'))

# year = 2023
# var5 = data_filtered5.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg5 = var5['pre'].mean(dim='time')
# x = var5.lon
# y = var5.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 5, projection=ccrs.PlateCarree())
# mp = ax.imshow(data_avg5, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Potential Evapotranspiration')


# # Minimum Temperature
# data_var6 = tmn.metpy.parse_cf('tmn')

# tmn['time'] = pd.to_datetime(tmn['time'].values)
# data_filtered6 = tmn.sel(time=slice('2022-01-01', '2023-12-31'))

# year = 2023
# var6 = data_filtered6.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg6 = var6['tmn'].mean(dim='time')
# x = var6.lon
# y = var6.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 6, projection=ccrs.PlateCarree())
# mp = ax.imshow(data_avg6, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Minimum Temperature')


# # Mean Temperature
# data_var7 = tmp.metpy.parse_cf('tmp')

# tmp['time'] = pd.to_datetime(tmp['time'].values)
# data_filtered7 = tmp.sel(time=slice('2022-01-01', '2023-12-31'))


# var7 = data_filtered7.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg7 = var7['tmp'].mean(dim='time')
# x = var7.lon
# y = var7.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 7, projection=ccrs.PlateCarree())
# mp = ax.imshow(data_avg7, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Mean Temperature')


# # Maximum Temperature
# data_var8 = tmx.metpy.parse_cf('tmx')

# tmx['time'] = pd.to_datetime(tmx['time'].values)
# data_filtered8 = tmx.sel(time=slice('2022-01-01', '2023-12-31'))


# var8 = data_filtered8.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg8 = var8['tmx'].mean(dim='time')
# x = var8.lon
# y = var8.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 8, projection=ccrs.PlateCarree())
# mp = ax.imshow(data_avg8, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Maximum Temperature')


# # Vapour Pressure
# data_var9 = vap.metpy.parse_cf('vap')

# vap['time'] = pd.to_datetime(vap['time'].values)
# data_filtered9 = vap.sel(time=slice('2022-01-01', '2023-12-31'))


# var9 = data_filtered9.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# data_avg9 = var9['vap'].mean(dim='time')
# x = var9.lon
# y = var9.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 9, projection=ccrs.PlateCarree())
# mp = ax.imshow(data_avg9, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')

# gl = ax.gridlines(draw_labels=True, alpha=0.1)
# gl.top_labels = False
# gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Maximum Temperature')


# # Rain Days
# data_var10 = wet.metpy.parse_cf('wet')

# # wet['time'] = pd.to_datetime(wet['time'].values)
# data_filtered10 = wet.sel(time=slice('2022-01-01', '2023-12-31'))

# # var10 = data_filtered10.sel(lon=slice(llon, hlon), lat=slice(llat, hlat), time=str(year))
# var10 = data_filtered10.sel(lon=slice(llon, hlon), lat=slice(llat, hlat))
# data_avg10 = var10['wet'].mean(dim='time').dt.days
# # x = var10.lon
# # y = var10.lat
# # ax = axs
# ax = fig.add_subplot(2, 5, 10, projection=ccrs.PlateCarree())
# # mp = ax.imshow(data_avg10, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')
# mp = ax.pcolormesh(data_avg10['lon'], data_avg10['lat'], data_avg10, cmap='viridis', transform=ccrs.PlateCarree())

# # gl = ax.gridlines(draw_labels=True, alpha=0.1)
# # gl.top_labels = False
# # gl.right_labels = False
# cbar = fig.colorbar(mp, ax=ax, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
# cbar.set_label('Maximum Temperature')


# elapsed = time.perf_counter() - start
# print(f"{__file__} executed in {elapsed} seconds.")
# plt.show()