import xarray as xr
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

ds = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmp.dat.nc')

year = 1901

tmp = ds.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
time_values = tmp['time'].values
time_dates = pd.to_datetime(time_values)

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

lon = tmp['lon'].values
lat = tmp['lat'].values
lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])
features = []
for time_index, time in enumerate(time_dates):  # วนลูปสำหรับแต่ละเดือน
    month = time.month
    tmp_in_month = tmp.isel(time=time_index)  # เลือกข้อมูลของเดือนนั้น
    tmp_values = tmp_in_month['tmp'].values  # ค่าอุณหภูมิในเดือนนั้น [lat, lon]
    
    for i, lon_value in enumerate(lon):
        for j, lat_value in enumerate(lat):
            cloud = tmp_values[j, i]  # ใช้ดัชนี [lat, lon]
            if not pd.isnull(cloud):  # ตรวจสอบว่าไม่มี NaN
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "TMP": float(cloud),  # แปลง float32 เป็น float
                        "month": month  # เพิ่มข้อมูลเดือน
                    }
                })


geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

output_file = "./src/Geo-data/Year-Dataset/data_tmp_1901.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=4)

print(f"ข้อมูลถูกบันทึกในไฟล์ {output_file}")


import geopandas as gpd
from shapely.geometry import mapping
from province import province_coord
import numpy as np

def calculate_weighted_cloud(province_name, shapefile, data):
    # เลือกจังหวัดที่ต้องการ
    province_coord = shapefile[shapefile['NAME_1'] == province_name]
    
    if province_coord.empty:
        print(f"No data in province: {province_name}")
        return None, None  # Return None if no data
    
    # กรองเฉพาะกริดที่ตัดกับเขตของจังหวัด
    grid_in_province = data[data.geometry.intersects(province_coord.geometry.union_all())]
    
    # พื้นที่ของจังหวัด
    province_area = province_coord.geometry.union_all().area
    
    total_weighted_temp = 0
    total_percentage = 0
    
    for idx, grid in grid_in_province.iterrows():
        # พื้นที่ที่ตัดกันกับเขตจังหวัด
        intersection_area = grid.geometry.intersection(province_coord.geometry.union_all()).area
        
        # คำนวณสัดส่วนการตัดกันของกริดที่เทียบกับพื้นที่จังหวัด
        intersection_percentage_of_province = (intersection_area / province_area) * 100
        
        # ค่า temperature ในกริด
        temperature_value = grid['TMP']
        temperature_value = np.nan_to_num(temperature_value, nan=0.0)
        
        # คำนวณค่าอุณหภูมิเฉลี่ยแบบถ่วงน้ำหนัก
        weighted_temp = temperature_value * intersection_percentage_of_province
        total_weighted_temp += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    # คำนวณค่าอุณหภูมิเฉลี่ยถ่วงน้ำหนักสำหรับจังหวัด
    average_temperature = total_weighted_temp / total_percentage #if total_percentage != 0 else None
    return average_temperature, province_coord.geometry

data = gpd.read_file('./src/Geo-data/Year-Dataset/data_tmp_1901.json')  
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')


geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

count = 0
year = 1901


for month in range(1, 13):
    
    monthly_data = data[data['month'] == month]
    print(f"Processing data for Month {month}: {len(monthly_data)} entries")

    for region in province_coord(): 
        for province in region:
            name, geometry, region_name = province
            avg_tmp, province_shape = calculate_weighted_cloud(name, shapefile, monthly_data)

            
            if avg_tmp is not None and province_shape is not None:
                
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geometry),  
                    "properties": {
                        "name": name,
                        "TMP": float(f"{avg_tmp:.2f}"),
                        "region": region_name,  
                        "month": month
                    }
                }
                geojson_data["features"].append(feature)

            count += 1
            print(f"{count}: Month {month}, Province: {name}, Avg Temp: {avg_tmp:.3f}")

output_geojson_path = "./src/Geo-data/Year-Dataset/province_tmp_1901.json"
with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

print("GeoJSON data saved successfully.")

import matplotlib.pyplot as plt

thailand = gpd.read_file("./src/Geo-data/Year-Dataset/province_tmp_1901.json")
fig, ax = plt.subplots(figsize=(10, 10))

# thai_source.plot(column='temperature', cmap='jet', linewidth=0.5, ax=ax, edgecolor='black', legend=True)

thailand.plot(column='TMP', ax=ax, legend=True, cmap='jet', legend_kwds={'label': "Temperature (°C)", 'orientation': "horizontal"})

plt.xlabel('Lon')
plt.ylabel('Lat')
plt.show()