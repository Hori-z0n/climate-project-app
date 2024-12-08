import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import xarray as xr
import pandas as pd
import geopandas as gpd
import warnings
import climate_V_thailand
# from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

year = 2023
ds = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.frs.dat.nc')

data_var = ds.metpy.parse_cf('frs')

ds['time'] = pd.to_datetime(ds['time'].values)
data_filtered = ds.sel(time=slice('2022-01-01', '2023-12-31'))

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})

frs = data_filtered.sel(lon=slice(50, 120), lat=slice(0, 30), time=str(year))
data_avg = frs['frs'].mean(dim='time').dt.days

x = frs.lon
y = frs.lat

ax = axs
mp = ax.imshow(data_avg, extent=(x.min(), x.max(), y.min(), y.max()), cmap='jet', origin='lower')
# mp = ax.pcolormesh(data_avg['lon'], data_avg['lat'], data_avg, extent=(x.min(), x.max(), y.min(), y.max()), cmap='viridis', transform=ccrs.PlateCarree())
# mp = ax.pcolormesh(data_avg['lon'], data_avg['lat'], data_avg, cmap='viridis', transform=ccrs.PlateCarree())

ax.set_extent([50, 120, 0, 30], crs=ccrs.PlateCarree())
plt.title('Cloud Cover for Thailand in ' + str(year), fontsize=12)

shp_target = gpd.read_file('./src/shapefile/gadm41_THA_1.shp')
shp_source = gpd.read_file('./src/shapefile/ThailandGrid.shp')
shp_source = shp_source.set_crs("EPSG:4326")

shp_int = climate_V_thailand.intersection_shp(shp_target, shp_source)
shp_int = shp_int[['geometry']]

shp_int.geometry.boundary.plot(ax=ax, color='black', linewidth=0.5)

gl = ax.gridlines(draw_labels=True, alpha=0.1)
gl.top_labels = False
gl.right_labels = False
cbar = fig.colorbar(mp, ax=axs, orientation='horizontal', fraction=0.05, pad=0.1, shrink=0.3)
cbar.set_label('Ground Frost Frequency')
plt.show()
