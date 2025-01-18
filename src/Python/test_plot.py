import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import time
import climate
import warnings
import json
warnings.filterwarnings('ignore')

fig, ax = plt.subplots(figsize=(10, 10))
# test = gpd.read_file('./src/Geo-data/nc_to_json_2001.json')
# test = gpd.read_file('./src/Geo-data/province_mean_temp_1901-01-16.json')
# test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/polygon_json_1901-01-16.json')
# test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/candex_1901-01-16.json')
# test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/candex_1901-02-15.json')
# test = gpd.read_file("src/Geo-data/thailand-Geo.json")
# test = gpd.read_file('./src/Geo-data/province_mean_temp_2001.json')
# test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/json_series/json_1901-01-16.json')
# thai_grid = gpd.read_file('./src/shapefile/gadm41_THA_1.shp')
# test.plot(column='temperature', legend=True)
# test.plot(ax=ax, column='temperature', legend=True, cmap='jet')
# thai_grid.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = .5)
# shp_int = climate.intersection_shp(test, thai_grid)
# print(shp_int)
# shp_int.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = 0.25)
# plt.xlabel('Lon')
# plt.ylabel('Lat')
thai_shape = gpd.read_file("src/shapefile/gadm41_THA_1.shp")
thai_source = gpd.read_file("src/Geo-data/nc_to_json_1960.json")
thailand = gpd.read_file("src/Geo-data/thailand-Geo.json")
# thai_grid = gpd.read_file('src/shapefile/ThaiGrid.shp')
gdf_shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')

gdf_tmp_thailand = thai_source.cx[97.5:105.5, 5:21]
gdf_shapefile_thailand = gdf_shapefile.cx[97.5:105.5, 5:21]

gdf_tmp_clipped = gdf_tmp_thailand.clip(gdf_shapefile_thailand)
gdf_tmp_clipped.plot(column='temperature', ax=ax, legend=True, cmap='jet', legend_kwds={'label': "Temperature (°C)", 'orientation': "horizontal"})

shp_target = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/gadm41_THA_1.shp')
shp_source = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/ThailandGrid2.shp')
shp_source = shp_source.set_crs("EPSG:4326")
shp_int = climate.intersection_shp(shp_target, shp_source)
shp_int = shp_int[['geometry']]
shp_int.geometry.boundary.plot(ax=ax, color='black', linewidth=0.5)

plt.show()