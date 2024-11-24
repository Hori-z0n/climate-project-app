import geopandas as gpd
import time
import warnings
import xarray as xr
from shapely.geometry import mapping
import json
import time
import climate_V_thailand as climate
import warnings
warnings.filterwarnings('ignore')

start = time.perf_counter()

netcdf_data = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Python/cru_ts4.08.1901.2023.tmp.dat.nc')
shapefile = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/thailand-Geo.json')

geojson_data = {
    "type": "FeatureCollection",
    "features": []
}
for times in netcdf_data['time'].values:
    data = gpd.read_file(f"./src/json_series/json_{str(times)[0:10]}.json")
    # data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/Python/json_series/json_{str(times)[0:10]}.json")

    count = 0
    # for region in climate.province_coordinates('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/thailand-Geo.json'):
    for region in climate.province_coordinates('./src/Geo-data/thailand-Geo.json'):
        for province in region:
            #print(province)
            name, geometry, region_name = province
            avg_temp, province_shape = climate.calculate_weighted_temperature(name, shapefile, data)
            
            # ตรวจสอบว่าค่าคำนวณเสร็จสิ้นและไม่ใช่ค่า None
            if avg_temp is not None and province_shape is not None:
                # สร้างฟีเจอร์สำหรับจังหวัดนี้ โดยใช้ MultiPolygon สำหรับรูปทรง
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geometry),  # ใช้ mapping ของรูปทรงจังหวัดโดยตรง
                    "properties": {
                        "name": name,
                        "temperature": float(f"{avg_temp:.2f}"),  # ค่าอุณหภูมิเฉลี่ยถ่วงน้ำหนัก
                        "region": region_name  # เพิ่มข้อมูลภูมิภาค
                    }
                }
                geojson_data["features"].append(feature)
            
            # พิมพ์ชื่อจังหวัดและค่า avg_temp ที่คำนวณได้
            count += 1
            # print(f"{count}: province name: {name}, average temp: {avg_temp:.3f}")

    output_geojson_path = f"./src/json_series/province_mean_temp_{str(times)[0:10]}.json"
    # output_geojson_path = f"C:/Users/konla/OneDrive/Desktop/Python/json_series/province_mean_temp_{str(times)[0:10]}.json"
    with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)
    print(f"save data to file : {output_geojson_path}")

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")