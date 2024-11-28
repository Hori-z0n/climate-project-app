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
test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/candex_1901-01-16.json')
# test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/candex_1901-02-15.json')
# test = gpd.read_file("src/Geo-data/thailand-Geo.json")
# test = gpd.read_file('./src/Geo-data/province_mean_temp_2001.json')
# test = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/json_series/json_1901-01-16.json')
# thai_grid = gpd.read_file('./src/shapefile/gadm41_THA_1.shp')
# test.plot(column='temperature', legend=True)
test.plot(ax=ax, column='temperature', legend=True, cmap='jet')
# thai_grid.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = .5)
# shp_int = climate.intersection_shp(test, thai_grid)
# print(shp_int)
# shp_int.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = 0.25)
plt.xlabel('Lon')
plt.ylabel('Lat')
plt.show()