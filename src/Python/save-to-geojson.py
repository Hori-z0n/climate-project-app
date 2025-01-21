import csv
import json
import numpy as np
import time
import xarray as xr
import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

start = time.perf_counter()

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

pre_data = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
gdf = gpd.read_file('./src/shapefile/gadm41_THA_1.shp')
shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')

# prec = {}
grid_value = []
ddata = []
index = []
dates = []
times = '1902'
test_start = '1901-01-16'
test_stop = '1901-02-15'
start_time = '1901'
stop_time = '2023'
# for date in tqdm(pre_data.sel(time = slice(start_time, stop_time))['time'], ascii=False, ncols=75, leave=False):
# for date in tqdm(pre_data.sel(time = str(times))['time'], ascii=False, ncols=75, leave=False):

#     ymd = str(date.values)[0:10]

#     data_filtered = pre_data.sel(time=ymd)
    
#     dates.append(ymd)

#     # data_avg = data_filtered['pre'].mean(dim='time')
#     data_avg = data_filtered['pre']

#     lon = data_avg.lon.values
#     lat = data_avg.lat.values

#     lon_step = float(lon[1] - lon[0])
#     lat_step = float(lat[1] - lat[0])

#     pre_value = data_avg.values

#     features = []
#     for i, lon_value in enumerate(lon):
#         for j, lat_value in enumerate(lat):
#             precipitation = pre_value[j, i]
#             if not pd.isnull(precipitation): 
#                 grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
#                 features.append({
#                     "type": "Feature",
#                     "geometry": {
#                         "type": "Polygon",
#                         "coordinates": [grid_polygon]
#                     },
#                     "properties": {
#                         "precipitation": float(precipitation) 
#                     }
#                 })

#     geojson_data = {
#         "type": "FeatureCollection",
#         "features": features
#     }
#     data = gpd.GeoDataFrame.from_features(geojson_data['features'])
#     gdf_tmp_clipped = data.clip(shapefile)

#     station_n = []
#     x_coordinates = []
#     y_coordinates = []
#     pre = []
#     li = {}
#     ln = {}
#     count = 1
#     for idx, grid in gdf_tmp_clipped.iterrows():
#         print(grid)
#         x, y = grid.geometry.centroid.x, grid.geometry.centroid.y
#         # x_coordinates.append(x)
#         # y_coordinates.append(y)
#         # station_n.append(f"station{loop}-{x}-{y}")
#         pre.append(grid.precipitation)
#         li.update({f"station{count}":grid.precipitation})
#         # li.update({f"station{count}-{x}-{y}":grid.precipitation})

#         ddata.append([x, y])
#         index.append(f"station{count}")
#         count += 1
#     grid_value.append(li)
    
# idx = pd.DataFrame(data=ddata ,index=index, columns=["longitude", "latitude"])
# print(idx)

# # climate_data = pd.DataFrame(grid_value, index=dates)

# # file_name1 = "precipitation.xlsx"
# # climate_data.to_excel(file_name1)
# file_name2 = "station_index.xlsx"
# idx.to_excel(file_name2)

fig, ax = plt.subplots(figsize=(10, 10))

# for date in tqdm(pre_data.sel(time = slice(test_start, test_stop))['time'], ascii=False, ncols=75, leave=False):

    # ymd = str(date.values)[0:10]

    # data_filtered = pre_data.sel(lon=slice(96, 106), lat=slice(4, 21), time=ymd)

    # dates.append(ymd)
    # # data_avg = data_filtered['pre'].mean(dim='time')

data_filtered = pre_data.sel(lon=slice(96, 106), lat=slice(4, 21),time='1960-01-16')

data_avg = data_filtered['pre']

lon = data_avg.lon.values
lat = data_avg.lat.values

lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])

pre_value = data_avg.values

buffer_distance = 0.3

thailand_mask = gdf.geometry.unary_union.buffer(buffer_distance)

lon2d, lat2d = np.meshgrid(lon, lat)

coord = np.vstack([lon2d.ravel(), lat2d.ravel()]).T

points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(coord[:,0], coord[:, 1]))

mask = points.within(thailand_mask).values.reshape(lon2d.shape)

data_avg = xr.where(mask, data_avg, np.nan)

# for i in mask:
#     print(i)
# print(len(data_avg['lat']))
# print(len(data_avg['lon']))
count = 1
features = []
for i, lat_value in enumerate(data_avg['lat']):
    for j, lon_value in enumerate(data_avg['lon']):
        precipitation = pre_value[i, j]
        if not pd.isnull(precipitation) and mask[i, j] == True:
            grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
            features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "station": f"station{count}"
                        # "precipitation": float(precipitation) 
                    }
                })
            count += 1
        else:
            continue

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}
output_geojson_path = "./src/Geo-data/Year-Dataset/station.json"

with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

# data = gpd.GeoDataFrame.from_features(geojson_data['features'])
# print(data)

# for idx, grid in data.iterrows():
#     print(grid.geometry)
# data.plot(ax=ax, column='precipitation', cmap='jet')
# plt.show()
# print(mask[0][0])
# shapefile.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = .5)

# mp = ax.imshow(data_avg, extent=(lon.min(), lon.max(), lat.min(), lat.max()), cmap='jet', origin='lower')

# data = gpd.GeoDataFrame(data_avg)


# data.plot(ax=ax, column='precipitation', cmap='jet')

# gdf_tmp_clipped.plot(ax=ax, column='precipitation', cmap='jet')
#     features = []
    
#     for i, lon_value in enumerate(lon):
#         for j, lat_value in enumerate(lat):
#             precipitation = pre_value[j, i]
#             if not pd.isnull(precipitation): 
#                 grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
#                 features.append({
#                     "type": "Feature",
#                     "geometry": {
#                         "type": "Polygon",
#                         "coordinates": [grid_polygon]
#                     },
#                     "properties": {
#                         "precipitation": float(precipitation) 
#                     }
#                 })

#     geojson_data = {
#         "type": "FeatureCollection",
#         "features": features
#     }
#     data = gpd.GeoDataFrame.from_features(geojson_data['features'])

#     gdf_tmp_clipped = data.clip(shapefile)

#     # print(gdf_tmp_clipped['features']['geometry'].type)
    
#     geojson_data = {
#         "type": "FeatureCollection",
#         "features": []
#     }

#     count = 1
#     for m in gdf_tmp_clipped.values:
#         features = {
#             'feature':"Feature",
#             'geometry':mapping(m[0]),
#             'properties':{
#                 'station':count,
#                 'pre':float(m[1])
#             }
#         }
#         geojson_data["features"].append(features)
#     count += 1

# output_geojson_path = f'./src/Geo-data/Year-Dataset/test_1_19_2025.json'
# with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
#     json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

# print("\nGeoJSON file polygon saved complete.")

# print(gdf_tmp_clipped)


# shapefile.geometry.boundary.plot(ax=ax, color=None,edgecolor='k',linewidth = .5)

# data.plot(ax=ax, column='precipitation', cmap='jet')
# gdf_tmp_clipped.plot(ax=ax, column='precipitation', cmap='jet')


# plt.show()

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")