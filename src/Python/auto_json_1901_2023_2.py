import xarray as xr
import pandas as pd
import json
import geopandas as gpd
import numpy as np
from shapely.geometry import mapping
from province import province_coord  # ดึงข้อมูลพิกัดของจังหวัดในแต่ละภาคจาก province.py
from gridcal import calculate_weighted_temperature

# ds = xr.open_dataset('./cru_ts4.08.1901.2023.tmp.dat.nc')
ds = xr.open_dataset('D:/Program/PROJECT/Python/cru_ts4.08.1901.2023.tmp.dat.nc')
year = 1901
temp = ds.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))

time_values = temp['time'].values
time_dates = pd.to_datetime(time_values)

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

lon = temp['lon'].values
lat = temp['lat'].values
lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])

features = []
for time_index, time in enumerate(time_dates):  
    month = time.month
    temp_in_month = temp.isel(time=time_index) 
    temp_values = temp_in_month['tmp'].values 
    
    for i, lon_value in enumerate(lon):
        for j, lat_value in enumerate(lat):
            temperature = temp_values[j, i]  
            if not pd.isnull(temperature):
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "temperature": float(temperature),  # แปลง float32 เป็น float
                        "month": month  # เพิ่มข้อมูลเดือน
                    }
                })

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}
# output_file = f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/json_{str(times)[0:10]}.json"
output_file = "C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/province_all_1901.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=4)

print(f"Save to location : {output_file}")

data = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/province_all_1901.json')  # ข้อมูลทั้งหมดรวมทุกเดือน
shapefile = gpd.read_file('src/Geo-data/thailand-Geo.json')


geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

count = 0

for month in range(1, 13):
    
    monthly_data = data[data['month'] == month]
    print(f"Processing data for Month {month}: {len(monthly_data)} entries")

    # เรียกใช้ฟังก์ชัน calculate_weighted_temperature สำหรับทุกจังหวัด
    for region in province_coord():  # ดึงข้อมูลจังหวัดในแต่ละภาค
        for province in region:
            name, geometry, region_name = province
            avg_temp, province_shape = calculate_weighted_temperature(name, shapefile, monthly_data)

            # ตรวจสอบว่าค่าคำนวณเสร็จสิ้นและไม่ใช่ค่า None
            if avg_temp is not None and province_shape is not None:
                # สร้างฟีเจอร์สำหรับจังหวัดและเดือนนี้
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geometry),  # ใช้ mapping ของรูปทรงจังหวัดโดยตรง
                    "properties": {
                        "name": name,
                        "temperature": float(f"{avg_temp:.2f}"),  # ค่าอุณหภูมิเฉลี่ยถ่วงน้ำหนัก
                        "region": region_name,  # เพิ่มข้อมูลภูมิภาค
                        "month": month  # เพิ่มข้อมูลเดือน
                    }
                }
                geojson_data["features"].append(feature)

            # แสดงสถานะการคำนวณ
            count += 1
            print(f"{count}: Month {month}, Province: {name}, Avg Temp: {avg_temp:.3f}")

# บันทึกข้อมูล GeoJSON ลงไฟล์
output_geojson_path = "C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/province_all_1901.json"
with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

print("GeoJSON data saved successfully.")