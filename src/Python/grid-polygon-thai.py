import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import time
import climate
import warnings
import json
warnings.filterwarnings('ignore')

fig, ax = plt.subplots(figsize=(10, 10))

test = gpd.read_file('./src/Geo-data/province_mean_temp_2001.json')
thai_grid = gpd.read_file('./src/shapefile/ThaiGrid.shp')
# test.plot(column='temperature', legend=True)
test.plot(ax=ax, column='temperature', legend=True, cmap='jet')
shp_int = climate.intersection_shp(test, thai_grid)
print(shp_int)
shp_int.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = 0.25)
plt.xlabel('Lon')
plt.ylabel('Lat')
plt.show()