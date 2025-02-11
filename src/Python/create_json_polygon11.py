import pandas as pd
import geopandas as gpd
# import netCDF4 as nc

import xarray as xr
import numpy as np
import json

from shapely.geometry import mapping
from tqdm import tqdm
from province import province_coord
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

def calculate_weighted_polygon(province_name, shapefile, data, cru):
    province_coord = shapefile[shapefile['NAME_1'] == province_name]
    
    if province_coord.empty:
        print(f"No data in province: {province_name}")
        return None, None  # Return None if no data
    
    grid_in_province = data[data.geometry.intersects(province_coord.geometry.union_all())]
    # grid_in_province = data[data.geometry.intersects(province_coord.geometry.unary_union())]
    
    province_area = province_coord.geometry.union_all().area
    
    total_weighted = 0
    total_percentage = 0
    
    for idx, grid in grid_in_province.iterrows():

        grid_area = grid.geometry.area

        intersection_area = grid.geometry.intersection(province_coord.geometry.union_all()).area
        # intersection_area = grid.geometry.intersection(province_coord.geometry.unary_union).area
        
        intersection_percentage_of_province = (intersection_area / province_area) * 100
        # intersection_percentage_of_province = (intersection_area / grid_area) * 100
        # weight = intersection_percentage_of_province / 100

        grid_value = grid[cru]
        if(cru == ''):
            print("You not select something try again")
            break

        grid_value = np.nan_to_num(grid_value, nan=0.0)
        
        # weighted_temp = grid_value * intersection_percentage_of_province
        weighted_temp = grid_value * intersection_percentage_of_province
        total_weighted += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    average_value = total_weighted / total_percentage #if total_percentage != 0 else None
    return average_value, province_coord.geometry


# thailand = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/gadm41_THA_1.shp')
# shapefile = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/ThailandGrid.shp')
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')


# provinces=['Amnat Charoen', 'Ang Thong', 'Bangkok Metropolis', 'Bueng Kan', 'Buri Ram', 'Chachoengsao', 'Chai Nat',
#         'Chaiyaphum', 'Chanthaburi', 'Chiang Mai', 'Chiang Rai', 'Chon Buri', 'Chumphon',
#         'Kalasin', 'Kamphaeng Phet', 'Kanchanaburi', 'Khon Kaen', 'Krabi', 'Lampang',
#         'Lamphun', 'Loei', 'Lop Buri', 'Mae Hong Son', 'Maha Sarakham', 'Mukdahan',
#         'Nakhon Nayok', 'Nakhon Pathom', 'Nakhon Phanom', 'Nakhon Ratchasima', 'Nakhon Sawan', 'Nakhon Si Thammarat',
#         'Nan', 'Narathiwat', 'Nong Bua Lam Phu', 'Nong Khai', 'Nonthaburi', 'Pathum Thani', 
#         'Pattani', 'Phangnga', 'Phatthalung', 'Phayao', 'Phetchabun', 'Phetchaburi',
#         'Phichit', 'Phitsanulok', 'Phra Nakhon Si Ayutthaya', 'Phrae', 'Phuket', 'Prachin Buri',
#         'Prachuap Khiri Khan', 'Ranong', 'Ratchaburi', 'Rayong', 'Roi Et', 'Sa Kaeo',
#         'Sakon Nakhon', 'Samut Prakan', 'Samut Sakhon', 'Samut Songkhram', 'Saraburi', 'Satun',
#         'Si Sa Ket', 'Sing Buri', 'Songkhla', 'Sukhothai', 'Suphan Buri', 'Surat Thani',
#         'Surin', 'Tak', 'Trang', 'Trat', 'Ubon Ratchathani', 'Udon Thani',
#         'Uthai Thani', 'Uttaradit', 'Yala', 'Yasothon']

# for i in range(0, 77):
start_year = 1901
stop_year = 1903


pre = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')

pre = pre.sel(lon=slice(96, 106), lat=slice(4, 21))

lon = pre['lon'].values
lat = pre['lat'].values

lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])

for year in tqdm(range(start_year, stop_year), leave=False,unit=' year'):
    ds_pr_year = pre.sel(time=slice(f'{year}', f'{year}'))
    time_values = ds_pr_year['time'].values
    time_dates = pd.to_datetime(time_values)
    features = []
    for time_idx, time in enumerate(time_dates):
        month = time.month
        precipitation_in_month = ds_pr_year.isel(time=time_idx)
        precipitation_value = precipitation_in_month['pre'].values
        for i, lon_value in enumerate(lon):
            for j, lat_value in enumerate(lat):
                pr = precipitation_value[j, i]
                # if not pd.isnull(pr):
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "pre": float(pr),
                        "time":time,
                    }
                })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    data = gpd.GeoDataFrame.from_features(geojson_data['features'])

    # geojson_data = {
    #     "type": "FeatureCollection",
    #     "features": []
    # }
    # seen = set()
    # _day = data['time'].values
    # _day = [x for x in _day if not (x in seen or seen.add(x))]

    # features = []
    # # for month in range(1, 13):
    # for time in np.array(_day):
    #     monthly_data = data[data['time'] == time]
    #     for region in province_coord():
    #         for province in region:
    #             name, geometry, region_name = province
    #             average_data, province_shape = calculate_weighted_polygon(name, shapefile, monthly_data, cru='pre')
    #             features.append({
    #                 "type": "Feature",
    #                     "geometry": mapping(geometry),
    #                     "properties": {
    #                         "name": name,
    #                         "region": region_name,
    #                         "time": str(time)[0:10],
    #                         "pre": float(average_data),
    #                     }
    #             })

    #     geojson_data = {
    #         "type": "FeatureCollection",
    #         "features": features
    #     }
    # data = gpd.GeoDataFrame.from_features(geojson_data['features'])
    # print(data)
    # output_file = f"./src/Geo-data/Era-Dataset/cru_data_polygon_{year}.json"
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(geojson_data, f, ensure_ascii=False, indent=4)
        
    # print(f"Data year {year} has been saved file in folder {output_file}")








# import geopandas as gpd
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import json
# import numpy as np
# import xarray as xr
# import pandas as pd
# import json

# # โหลดข้อมูลจาก NetCDF
# tmp = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmp.dat.nc')
# dtr = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.dtr.dat.nc')
# pre = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
# tmn = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmn.dat.nc')
# tmx = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmx.dat.nc')

# def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
#     return [
#         [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
#         [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
#         [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
#         [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
#         [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
#     ]

# for i in range(0, 10):  # ตัวอย่างวนลูป 10 ปี
#     year = 1901 + i
#     temp = tmp.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
#     dtr_temp = dtr.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
#     pre_temp = pre.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
#     tmn_temp = tmn.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
#     tmx_temp = tmx.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))

#     time_values = temp['time'].values
#     time_dates = pd.to_datetime(time_values)

#     lon = temp['lon'].values
#     lat = temp['lat'].values
#     lon_step = float(lon[1] - lon[0])
#     lat_step = float(lat[1] - lat[0])

#     features = []
#     for time_index, time in enumerate(time_dates):  
#         month = time.month
#         temp_in_month = temp.isel(time=time_index)
#         dtr_in_month = dtr_temp.isel(time=time_index)
#         pre_in_month = pre_temp.isel(time=time_index)
#         tmn_in_month = tmn_temp.isel(time=time_index)
#         tmx_in_month = tmx_temp.isel(time=time_index)
        
#         temp_values = temp_in_month['tmp'].values
#         dtr_values = dtr_in_month['dtr'].values
#         pre_values = pre_in_month['pre'].values
#         tmn_values = tmn_in_month['tmn'].values
#         tmx_values = tmx_in_month['tmx'].values
        
#         for i, lon_value in enumerate(lon):
#             for j, lat_value in enumerate(lat):
#                 temperature = temp_values[j, i]
#                 diurnal_range = dtr_values[j, i]
#                 precipitation = pre_values[j, i]
#                 min_temp = tmn_values[j, i]
#                 max_temp = tmx_values[j, i]

#                 if not pd.isnull(temperature):
#                     grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
#                     features.append({
#                         "type": "Feature",
#                         "geometry": {
#                             "type": "Polygon",
#                             "coordinates": [grid_polygon]
#                         },
#                         "properties": {
#                             "temperature": float(temperature),
#                             "dtr": float(diurnal_range) if not pd.isnull(diurnal_range) else None,
#                             "pre": float(precipitation) if not pd.isnull(precipitation) else None,
#                             "tmin": float(min_temp) if not pd.isnull(min_temp) else None,
#                             "tmax": float(max_temp) if not pd.isnull(max_temp) else None,
#                             "month": month
#                         }
#                     })

#     geojson_data = {
#         "type": "FeatureCollection",
#         "features": features
#     }
#     output_file = f"./src/Geo-data/Year-Dataset/data_grid_index_{year}.json"
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(geojson_data, f, ensure_ascii=False, indent=4)

#     print(f"Save to location : {output_file}")



# # กำหนดปีที่ต้องการพล็อต
# years = range(1901, 1911)  # ช่วงปี 1901-1910

# # ขอบเขตแผนที่
# lon_min, lon_max = 96, 106
# lat_min, lat_max = 4, 21

# # Color map
# cmap = 'turbo'

# # สร้าง subplot สำหรับ 10 ปี
# fig, axes = plt.subplots(2, 5, figsize=(20, 10), subplot_kw={'projection': ccrs.PlateCarree()})
# fig.suptitle("Average Temperature by Year (1901-1910)", fontsize=16)

# for i, year in enumerate(years):
#     # โหลดข้อมูล GeoJSON ของแต่ละปี
#     geojson_file = f"../Geo-data/Year-Dataset/data_grid_{year}.json"
#     with open(geojson_file, 'r', encoding='utf-8') as f:
#         geojson_data = json.load(f)

#     # แปลงข้อมูล GeoJSON เป็น GeoDataFrame
#     gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

#     # ตรวจสอบว่าข้อมูลมีคอลัมน์ temperature
#     if 'temperature' not in gdf.columns:
#         raise ValueError("GeoJSON data must contain 'temperature' property.")

#     # คำนวณค่าเฉลี่ยรายปี
#     annual_avg_temp = gdf['temperature'].mean()
#     print(f"Year {year}: Average Temperature = {annual_avg_temp:.2f}°C")

#     # แสดง grid cells เฉลี่ยของปีนั้น
#     ax = axes[i // 5, i % 5]
#     gdf.plot(column='temperature', ax=ax, cmap=cmap, edgecolor='k', legend=False)

#     # ตั้งค่าแผนที่
#     ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
#     ax.set_title(f"{year} Avg Temp: {annual_avg_temp:.2f}°C", fontsize=10)

# # ปรับระยะห่างของ subplot
# plt.tight_layout(rect=[0, 0, 1, 0.95])
# plt.show()
