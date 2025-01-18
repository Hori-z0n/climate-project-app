import geopandas as gpd
import climate
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
# gdf_tmp_clipped.plot(column='temperature', ax=ax, legend=True, cmap='jet', legend_kwds={'label': "Temperature (°C)", 'orientation': "horizontal"})

shp_target = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/gadm41_THA_1.shp')
shp_source = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/ThailandGrid2.shp')
shp_source = shp_source.set_crs("EPSG:4326")
shp_int = climate.intersection_shp(shp_target, shp_source)
shp_int = shp_int[['geometry']]
shp_int.geometry.boundary.plot(ax=ax, color='black', linewidth=0.5)
elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")
plt.show()