import xarray as xr
import json
import pandas as pd
import time
import geopandas as gpd
from shapely.geometry import mapping
from province import province_coord  # ดึงข้อมูลพิกัดของจังหวัดในแต่ละภาคจาก province.py
import numpy as np

def calculate_weighted_temperature(province_name, shapefile, data):
    # เลือกจังหวัดที่ต้องการ
    province_coord = shapefile[shapefile['NAME_1'] == province_name]
    
    # ตรวจสอบว่ามีข้อมูลจังหวัดหรือไม่
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
        temperature_value = grid['temperature']
        temperature_value = np.nan_to_num(temperature_value, nan=0.0)
        
        # คำนวณค่าอุณหภูมิเฉลี่ยแบบถ่วงน้ำหนัก
        weighted_temp = temperature_value * intersection_percentage_of_province
        total_weighted_temp += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    # คำนวณค่าอุณหภูมิเฉลี่ยถ่วงน้ำหนักสำหรับจังหวัด
    average_temperature = total_weighted_temp / total_percentage #if total_percentage != 0 else None
    return average_temperature, province_coord.geometry


start = time.perf_counter()
# โหลดข้อมูล NetCDF
ds = xr.open_dataset('D:/Program/PROJECT/Python/cru_ts4.08.1901.2023.tmp.dat.nc')

for i in range(0, 10):
    year = 1901 + i
    temp = ds.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))

    # คำนวณค่าเฉลี่ยอุณหภูมิต่อกริด
    data_avg = temp['tmp'].mean(dim='time')

    # สร้าง DataFrame จากข้อมูล NetCDF
    lon, lat = data_avg.lon.values, data_avg.lat.values
    temp_values = data_avg.values
    #print(temp_values)

    # ฟังก์ชันสำหรับสร้าง Polygon จากพิกัดกลางของกริด
    def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
        return [
            [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
            [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
            [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
            [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
            [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
        ]

    # คำนวณระยะห่างระหว่างพิกัด (step)
    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])


    # เตรียมข้อมูลในรูปแบบ JSON
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

    # สร้างโครงสร้าง GeoJSON
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # บันทึกข้อมูลเป็นไฟล์ GeoJSON
    output_file = f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/nc_to_json_{year}.json"
    # output_file = f"../Geo-data/nc_to_json_{year}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    print(f"Data save to : {output_file}")
    
    data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/nc_to_json_{year}.json")  # ข้อมูลทั้งหมดรวมทุกเดือน
    shapefile = gpd.read_file('src/Geo-data/thailand-Geo.json')

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    count = 0

        # เรียกใช้ฟังก์ชัน calculate_weighted_temperature สำหรับทุกจังหวัด
    for region in province_coord():  # ดึงข้อมูลจังหวัดในแต่ละภาค
        for province in region:
            name, geometry, region_name = province
            avg_temp, province_shape = calculate_weighted_temperature(name, shapefile, data)

            if avg_temp is not None and province_shape is not None:
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geometry), 
                    "properties": {
                        "name": name,
                        "temperature": float(f"{avg_temp:.2f}"),  
                        "region": region_name,
                    }
                }
                geojson_data["features"].append(feature)

            count += 1
                # print(f"{count}: Month {month}, Province: {name}, Avg Temp: {avg_temp:.3f}")

    output_geojson_path = f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/nc_to_json_{year}.json"
    with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

    print(f"GeoJSON {year} data saved successfully.")


elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")