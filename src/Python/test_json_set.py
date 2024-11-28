import geopandas as gpd
import time
import xarray as xr
import pandas as pd
import json
import time
from shapely.geometry import mapping
import climate_V_thailand as climate
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

# netcdf_data = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Python/cru_ts4.08.1901.2023.tmp.dat.nc')
netcdf_data = xr.open_dataset('D:/Program/PROJECT/Python/cru_ts4.08.1901.2023.tmp.dat.nc')

thailand_json = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/thailand-Geo.json')
count = 1

# print(netcdf_data['time'].values[0:24])
# for times in netcdf_data['time'].values[0:24]:

#     data_filtered = netcdf_data.sel(lon=slice(96, 106), lat=slice(4, 21),time=[str(times)[0:10]])

#     netcdf_data['time'] = pd.to_datetime(netcdf_data['time'].values)
#     data_avg = data_filtered['tmp'].mean(dim='time')

#     lon, lat = data_avg.lon.values, data_avg.lat.values
#     temp_values = data_avg.values

#     lon_step = float(lon[1] - lon[0])
#     lat_step = float(lat[1] - lat[0])

#     features = []
#     for i, lon_value in enumerate(lon):
#         for j, lat_value in enumerate(lat):
#             temperature = temp_values[j, i]
#             if not pd.isnull(temperature):  # ตรวจสอบว่าไม่มี NaN
#                 grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
#                 features.append({
#                     "type": "Feature",
#                     "geometry": {
#                         "type": "Polygon",
#                         "coordinates": [grid_polygon]
#                     },
#                     "properties": {
#                         "temperature": float(temperature)  # แปลง float32 เป็น float
#                     }
#                 })
    
#     geojson_data = {
#     "type": "FeatureCollection",
#     "features": features
#     }
#     # output_file = f"./src/json_series/json_{str(times)[0:10]}.json"

#     output_file = f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/json_{str(times)[0:10]}.json"
    
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(geojson_data, f, ensure_ascii=False, indent=4)

#     print(f"save data to file : {output_file}")
#     count += 1


for times in netcdf_data['time'].values[0:24]:
    data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/json_{str(times)[0:10]}.json")
    gdf_shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')
    gdf_tmp_thailand = data.cx[97.5:105.5, 5:21]
    gdf_shapefile_thailand = gdf_shapefile.cx[97.5:105.5, 5:21]

    gdf_tmp_clipped = gdf_tmp_thailand.clip(gdf_shapefile_thailand)
    output_path = f'C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/candex_{str(times)[0:10]}.json'
    print(f"save data to file : {output_path}")
    gdf_tmp_clipped.to_file(output_path, driver='GeoJSON')
# for times in netcdf_data['time'].values[0:24]:
#     geojson_data = {
#     "type": "FeatureCollection",
#     "features": []
#     }
#     data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/json_{str(times)[0:10]}.json")

#     count = 0
#     for region in climate.province_coordinates('./src/Geo-data/thailand-Geo.json'):
#         for province in region:
#             #print(province)
#             name, geometry, region_name = province
#             avg_temp, province_shape = climate.calculate_weighted_temperature(name, thailand_json, data)
            
#             # ตรวจสอบว่าค่าคำนวณเสร็จสิ้นและไม่ใช่ค่า None
#             if avg_temp is not None and province_shape is not None:
#                 # สร้างฟีเจอร์สำหรับจังหวัดนี้ โดยใช้ MultiPolygon สำหรับรูปทรง
#                 feature = {
#                     "type": "Feature",
#                     "geometry": mapping(geometry),  # ใช้ mapping ของรูปทรงจังหวัดโดยตรง
#                     "properties": {
#                         "name": name,
#                         "temperature": float(f"{avg_temp:.2f}"),  # ค่าอุณหภูมิเฉลี่ยถ่วงน้ำหนัก
#                         "region": region_name  # เพิ่มข้อมูลภูมิภาค
#                     }
#                 }
#                 geojson_data["features"].append(feature)
            
#             # พิมพ์ชื่อจังหวัดและค่า avg_temp ที่คำนวณได้
#             count += 1
#             # print(f"{count}: province name: {name}, average temp: {avg_temp:.3f}")
#     output_geojson_path = f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/polygon_json_{str(times)[0:10]}.json"
#     # output_geojson_path = f"./src/json_series/province_mean_temp_{str(times)[0:10]}.json"
#     # output_geojson_path = f"C:/Users/konla/OneDrive/Desktop/Python/json_series/province_mean_temp_{str(times)[0:10]}.json"
#     with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
#         json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)
#     print(f"save data to file : {output_geojson_path}")

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")
