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

pre_data = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')
# tmx_data = xr.open_dataset('C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc')
# tmn_data = xr.open_dataset('C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc')
shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

prec = {}
grid_value = []
dates = []

times = '1960'
# year = str(times)[0:10]
for date in tqdm(pre_data['time'][0:10], ascii=False, ncols=75, leave=False):
    ymd = str(date.values)[0:10]
    
    data_filtered = pre_data.sel(time=ymd)
    
    dates.append(ymd)
    
    data_avg = data_filtered['tp'].mean(dim='time')

    lon = data_avg.longitude.values
    lat = data_avg.latitude.values

    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])

    pre_value = data_avg.values

    features = []
    for i, lon_value in enumerate(lon):
        for j, lat_value in enumerate(lat):
            precipitation = pre_value[j, i]
            if not pd.isnull(precipitation):  # ตรวจสอบว่าไม่มี NaN
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "precipitation": float(precipitation)  # แปลง float32 เป็น float
                    }
                })
                # print(grid_polygon)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    data = gpd.GeoDataFrame.from_features(geojson_data['features'])

    gdf_tmp_clipped = data.clip(shapefile)

    station_n = []
    x_coordinates = []
    y_coordinates = []
    
    pre = []
    li = {}
    count = 1
    for idx, grid in gdf_tmp_clipped.iterrows():
        x, y = grid.geometry.centroid.x, grid.geometry.centroid.y
        # x_coordinates.append(x)
        # y_coordinates.append(y)
        # station_n.append(f"station{loop}-{x}-{y}")
        pre.append(grid.precipitation)
        li.update({f"station{count}-{x}-{y}":grid.precipitation})
        # print(f"station{count}")
        # print(count)
        count += 1
    grid_value.append(li)
    # prec.update(li)
    # prec.append([prec])
    # pre = None
# print(grid_value)
# print(pd.DataFrame(grid_value, index=dates, columns=station_n))
# print(pd.DataFrame(grid_value, index=dates))
# climate_data = pd.DataFrame(prec, index=dates)
climate_data = pd.DataFrame(grid_value, index=dates)
# print(climate_data)
file_name = "test.xlsx"
climate_data.to_excel(file_name)
# # print(type(prec))
# # print(prec)
# # print('-'*100)
# # print(len(prec))
# # print(prec)
elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")