import geopandas as gpd
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings('ignore')
start = time.perf_counter()

fig, ax = plt.subplots(figsize=(10, 10))
thai_shape = gpd.read_file("./src/shapefile/gadm41_THA_1.shp")
thai_source = gpd.read_file("./src/Geo-data/nc_to_json_1960.json")
thailand = gpd.read_file("src/Geo-data/thailand-Geo.json")
shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')
gdf_tmp_thailand = thai_source.cx[96.5:106, 4:21]
gdf_shapefile_thailand = shapefile.cx[96:106, 4:21]

gdf_tmp_clipped = gdf_tmp_thailand.clip(gdf_shapefile_thailand)
gdf_tmp_clipped.plot(column='precipitation', ax=ax, legend=True, cmap='jet', legend_kwds={'label': "precipitation (mm)", 'orientation': "horizontal"})

output_path = 'src/Geo-data/candex_to_geo2.json'
gdf_tmp_clipped.to_file(output_path, driver='GeoJSON')

# open the json file
thailand = gpd.read_file("./src/Geo-data/candex_to_geo2.json")
fig, ax = plt.subplots(figsize=(10, 10))

# thai_source.plot(column='temperature', cmap='jet', linewidth=0.5, ax=ax, edgecolor='black', legend=True)

thailand.plot(column='precipitation', ax=ax, legend=True, cmap='jet', legend_kwds={'label': "precipitation (mm)", 'orientation': "horizontal"})

plt.xlabel('Lon')
plt.ylabel('Lat')

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")
plt.show()