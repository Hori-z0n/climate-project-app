
import json
import time
import xarray as xr
import pandas as pd
from shapely.geometry import mapping
import warnings
warnings.filterwarnings('ignore')


start = time.perf_counter()

netcdf_data = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')

year = '1960-01-01'
Precipitation =  netcdf_data.sel(time=year)

data_avg = Precipitation['tp'].mean(dim='time')
# netcdf_data.time_bnds.attrs['units'] = netcdf_data.time.attrs['units']
lon = data_avg.longitude.values
lat = data_avg.latitude.values

pre_value = data_avg.values

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])

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
output_file = "C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/nc_to_json_1960.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=4)

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")
