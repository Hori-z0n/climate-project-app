import cartopy.feature as cfeature
import cartopy.crs as ccrs
import geopandas as gpd
import time
import xarray as xr
import json
import matplotlib.pyplot as plt
import climate_V_thailand as climate
import warnings
import pandas as pd
import rioxarray
import numpy as np
warnings.filterwarnings('ignore')

start = time.perf_counter()
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(20, 20), subplot_kw={'projection': ccrs.PlateCarree()})
netcdf_data = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')

# shapefile = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/thailandGrid.shp')
shapefile = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/ThailandGrid2.shp')
thailand = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/gadm41_THA_1.shp')

# print(netcdf_data)
netcdf_data['time'] = pd.to_datetime(netcdf_data['time'].values)
# data_filtered = netcdf_data.sel(time=slice('2000-01-01', '2005-12-31'))
data_filtered = netcdf_data.sel(time='2000-02-01')
data_avg = data_filtered['tp'].mean(dim='time')

x = data_avg.longitude
y = data_avg.latitude
lon2d, lat2d = np.meshgrid(x, y)
coords = np.vstack([lon2d.ravel(), lat2d.ravel()]).T
points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(coords[:, 0], coords[:, 1]))

buffer_distance = 0.05
thailand_mask = thailand.geometry.unary_union.buffer(buffer_distance)
mask = points.within(thailand_mask).values.reshape(lon2d.shape)
data_avg = xr.where(mask, data_avg, np.nan)    
# print(data_filtered['time'])

# print(data_avg)
data_avg = np.flipud(data_avg)
# data_avg = np.fliplr(data_avg)
# mp = axs.imshow(data_avg,  cmap='jet', origin='lower')
mp = axs.imshow(data_avg, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')
thailand.boundary.plot(ax=axs, edgecolor='black', linewidth=2)
shp_int = climate.intersection_shp(thailand, shapefile)
shp_int.geometry.boundary.plot(ax=axs,color='gray',edgecolor='k',linewidth = 0.25)

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")
plt.show()