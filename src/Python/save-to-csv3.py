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

shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')

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

# prec = {}
grid_value = []
ddata = []
index = []
dates = []
times = '1960'
start_time = '1901'
stop_time = '2023'
# for date in tqdm(pre_data.sel(time = slice(start_time, stop_time))['time'], ascii=False, ncols=75, leave=False):
for date in tqdm(pre_data.sel(time = str(times))['time'], ascii=False, ncols=75, leave=False):
    ymd = str(date.values)[0:10]

    data_filtered = pre_data.sel(time=ymd)
    
    dates.append(ymd)

    # data_avg = data_filtered['pre'].mean(dim='time')
    data_avg = data_filtered['pre']

    lon = data_avg.lon.values
    lat = data_avg.lat.values

    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])
    
    pre_value = data_avg.values

    features = []
    for i, lon_value in enumerate(lon):
        for j, lat_value in enumerate(lat):
            precipitation = pre_value[j, i]
            if not pd.isnull(precipitation): 
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "precipitation": float(precipitation) 
                    }
                })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    data = gpd.GeoDataFrame.from_features(geojson_data['features'])
    gdf_tmp_clipped = data.clip(shapefile)

    # station_n = []
    # x_coordinates = []
    # y_coordinates = []
    
    pre = []
    li = {}
    ln = {}
    count = 1
    for idx, grid in gdf_tmp_clipped.iterrows():
        # x, y = grid.geometry.centroid.x, grid.geometry.centroid.y
        # x_coordinates.append(x)
        # y_coordinates.append(y)
        # station_n.append(f"station{loop}-{x}-{y}")
        pre.append(grid.precipitation)
        li.update({f"station{count}":grid.precipitation})
        # li.update({f"station{count}-{x}-{y}":grid.precipitation})

        # ddata.append([x, y])
        # index.append(f"station{count}")
        count += 1
    grid_value.append(li)
    
# idx = pd.DataFrame(data=ddata ,index=index, columns=["longitude", "latitude"])


climate_data = pd.DataFrame(grid_value, index=dates)

file_name1 = "precipitation.xlsx"
climate_data.to_excel(file_name1)
# file_name2 = "station_index.xlsx"
# idx.to_excel(file_name2)

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")