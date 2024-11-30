import xarray as xr
import json
import pandas as pd
import time
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


elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")