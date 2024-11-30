import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import json
import time
import warnings
from shapely.geometry import mapping
warnings.filterwarnings('ignore')

start = time.perf_counter()

data = gpd.read_file('./src/Geo-data/nc_to_json_2000_1.json')
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

def province_coord():
    province_NE = [
        "Nakhon Ratchasima", "Kalasin", "Khon Kaen", "Chaiyaphum", "Nakhon Phanom",
        "Bueng Kan", "Buri Ram", "Maha Sarakham", "Mukdahan", "Yasothon",
        "Roi Et", "Loei", "Si Sa Ket", "Sakon Nakhon", "Surin",
        "Nong Khai", "Nong Bua Lam Phu", "Udon Thani", "Ubon Ratchathani", "Amnat Charoen"
    ]
    
    province_North = [
        "Chiang Rai", "Chiang Mai", "Nan", "Phayao", "Phrae", "Mae Hong Son", "Lampang",
        "Lamphun", "Uttaradit"
    ]
    
    province_South = [
        "Krabi", "Chumphon", "Trang", "Nakhon Si Thammarat", "Narathiwat" , "Pattani", 
        "Phangnga", "Phatthalung", "Phuket", "Yala", "Ranong", "Songkhla", "Satun",
        "Surat Thani"
    ]
    
    province_Middle = [
        "Bangkok Metropolis", "Kamphaeng Phet", "Chai Nat", "Nakhon Nayok", "Nakhon Pathom", "Nakhon Sawan",
        "Nonthaburi", "Pathum Thani", "Phra Nakhon Si Ayutthaya", "Phichit", "Phitsanulok", "Phetchabun",
        "Lop Buri", "Samut Prakan", "Samut Songkhram", "Samut Sakhon", "Saraburi", "Sing Buri", "Sukhothai",
        "Suphan Buri", "Ang Thong", "Uthai Thani"
    ]
    
    #ภาคตะวันออก
    province_East = [
        "Chanthaburi", "Chachoengsao", "Chon Buri", "Trat", "Prachin Buri", "Rayong", "Sa Kaeo"
    ]
   
    #ภาคตะวันตก
    province_West = [
        "Kanchanaburi", "Tak", "Prachuap Khiri Khan", "Phetchaburi", "Ratchaburi"
    ] 
    
    # ดึงพิกัดของแต่ละจังหวัดในรูปแบบ geometry
    ne_list = [(name, shapefile[shapefile['NAME_1'] == name].geometry.unary_union, "North_East_region") for name in province_NE]
    north_list = [(name, shapefile[shapefile['NAME_1'] == name].geometry.unary_union, "North_region") for name in province_North]
    south_list = [(name, shapefile[shapefile['NAME_1'] == name].geometry.unary_union, "South_region") for name in province_South]
    middle_list = [(name, shapefile[shapefile['NAME_1'] == name].geometry.unary_union, "Middle_region") for name in province_Middle]
    east_list = [(name, shapefile[shapefile['NAME_1'] == name].geometry.unary_union, "East_region") for name in province_East]
    west_list = [(name, shapefile[shapefile['NAME_1'] == name].geometry.unary_union, "West_region") for name in province_West]


    # รวมข้อมูลของภาคเหนือและภาคอีสานในลิสต์
    region_coords = [
        north_list,
        ne_list,
        south_list,
        middle_list,
        east_list,
        west_list
    ]
    
    return region_coords

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


coord = shapefile[shapefile['NAME_1'] == np.array(shapefile['NAME_1'])[-1]]
count = 0
for region in province_coord():
    for province in region:
        name, geometry, region_name = province
        
        avg_temp, province_shape = calculate_weighted_temperature(name, shapefile, data)
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
        print(f"{count}: province name: {name}, average temp: {avg_temp:.3f}")

# บันทึกข้อมูล GeoJSON ลงไฟล์
output_geojson_path = "src/Geo-data/province_mean_temp_2001.json"
with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)


elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")