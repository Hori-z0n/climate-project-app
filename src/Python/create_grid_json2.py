from tqdm import tqdm 
import json
import time
import xarray as xr
import pandas as pd
import numpy as np
from shapely.geometry import mapping
import warnings
warnings.filterwarnings('ignore')

netcdf_data = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   
    ]

year = '1960'
data = netcdf_data.sel(time=year)
lon = netcdf_data['longitude'].values
lat = netcdf_data['latitude'].values
lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])

for date in data['time'][0:34]:
    time_values1 = str(date.values)[0:10]
    time_dates1 = pd.to_datetime(time_values1)
    Precipitation = netcdf_data.sel(time=time_values1)
    pre_values = Precipitation['tp'].values
    time_dates = time_values1.split('-')
    _day = time_dates[2]
    _month = time_dates[1]
    _year = time_dates[0]
    count = 0
    # data_avg = Precipitation['tp'].mean(dim='time')
    # pre_value = data_avg.values
    # print(_day, _month, _year,pre_value)
    # data1 = pre_data.sel(time=str(year))
    # time_values1 = data1['time'].values
    # time_dates1 = pd.to_datetime(time_values1)
    
    count = 0
    features = []
    # for i, lon_value in tqdm(enumerate(lon), desc="Create grid...",unit=' grid', ascii='0123456789#', ncols=75):
    #     for j, lat_value in tqdm(enumerate(lat), leave=False, ncols=75):
    #         precipitation = pre_values[j, i]
    #         print(precipitation)
            # if not pd.isnull(precipitation):
                # grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
#                 features.append({
#                     "type": "Feature",
#                     "geometry": {
#                         "type": "Polygon",
#                         # "coordinates": [grid_polygon]
#                         "coordinates": [1, 2, 3, 4]
#                     },
#                     "properties": {
#                         "pre": float(precipitation),
#                         "year": _year,
#                         "month": _month ,
#                         "day": _day
#                     }
#                 })
#             print(_day, _month, _year)
#     count += 1

# geojson_data = {
#     "type": "FeatureCollection",
#     "features": features
# }
# output_file = f"C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/test_{year}.json"
# with open(output_file, 'w', encoding='utf-8') as f:
#     json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    # netcdf_data.time_bnds.attrs['units'] = netcdf_data.time.attrs['units']
    # lon = data_avg.longitude.values
    # lat = data_avg.latitude.values

# # pre_value = data_avg.values

# # def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
# #     return [
# #         [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
# #         [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
# #         [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
# #         [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
# #         [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
# #     ]

# # lon_step = float(lon[1] - lon[0])
# # lat_step = float(lat[1] - lat[0])

# # features = []
# # for i, lon_value in enumerate(lon):
# #     for j, lat_value in enumerate(lat):
# #         precipitation = pre_value[j, i]
# #         if not pd.isnull(precipitation):  # ตรวจสอบว่าไม่มี NaN
# #             grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
# #             features.append({
# #                 "type": "Feature",
# #                 "geometry": {
# #                     "type": "Polygon",
# #                     "coordinates": [grid_polygon]
# #                 },
# #                 "properties": {
# #                     "precipitation": float(precipitation)  # แปลง float32 เป็น float
# #                 }
# #             })
# #             # print(grid_polygon)

