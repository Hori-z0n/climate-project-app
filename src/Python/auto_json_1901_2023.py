import geopandas as gpd
import time
import warnings
import xarray as xr
import pandas as pd
import json
import time
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

netcdf_data = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Python/cru_ts4.08.1901.2023.tmp.dat.nc')
thailand_json = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/thailand-Geo.json')
count = 1

for times in netcdf_data['time'].values:

    data_filtered = netcdf_data.sel(lon=slice(96, 106), lat=slice(4, 21),time=[str(times)[0:10]])

    netcdf_data['time'] = pd.to_datetime(netcdf_data['time'].values)
    data_avg = data_filtered['tmp'].mean(dim='time')

    lon, lat = data_avg.lon.values, data_avg.lat.values
    temp_values = data_avg.values

    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])

    features = []
    for i, lon_value in enumerate(lon):
        for j, lat_value in enumerate(lat):
            temperature = temp_values[j, i]
            if not pd.isnull(temperature):  # ตรวจสอบว่าไม่มี NaN
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "temperature": float(temperature)  # แปลง float32 เป็น float
                    }
                })
    
    geojson_data = {
    "type": "FeatureCollection",
    "features": features
    }
    output_file = f"./src/json_series/json_{str(times)[0:10]}.json"
    # output_file = f"C:/Users/konla/OneDrive/Desktop/Python/json_series/json_{str(times)[0:10]}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    print(f"save data to file : {output_file}")
    count += 1

# print(count)
elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")
