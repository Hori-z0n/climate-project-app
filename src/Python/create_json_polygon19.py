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


provinces=['Amnat Charoen', 'Ang Thong', 'Bangkok Metropolis', 'Bueng Kan', 'Buri Ram', 'Chachoengsao', 'Chai Nat',
        'Chaiyaphum', 'Chanthaburi', 'Chiang Mai', 'Chiang Rai', 'Chon Buri', 'Chumphon',
        'Kalasin', 'Kamphaeng Phet', 'Kanchanaburi', 'Khon Kaen', 'Krabi', 'Lampang',
        'Lamphun', 'Loei', 'Lop Buri', 'Mae Hong Son', 'Maha Sarakham', 'Mukdahan',
        'Nakhon Nayok', 'Nakhon Pathom', 'Nakhon Phanom', 'Nakhon Ratchasima', 'Nakhon Sawan', 'Nakhon Si Thammarat',
        'Nan', 'Narathiwat', 'Nong Bua Lam Phu', 'Nong Khai', 'Nonthaburi', 'Pathum Thani', 
        'Pattani', 'Phangnga', 'Phatthalung', 'Phayao', 'Phetchabun', 'Phetchaburi',
        'Phichit', 'Phitsanulok', 'Phra Nakhon Si Ayutthaya', 'Phrae', 'Phuket', 'Prachin Buri',
        'Prachuap Khiri Khan', 'Ranong', 'Ratchaburi', 'Rayong', 'Roi Et', 'Sa Kaeo',
        'Sakon Nakhon', 'Samut Prakan', 'Samut Sakhon', 'Samut Songkhram', 'Saraburi', 'Satun',
        'Si Sa Ket', 'Sing Buri', 'Songkhla', 'Sukhothai', 'Suphan Buri', 'Surat Thani',
        'Surin', 'Tak', 'Trang', 'Trat', 'Ubon Ratchathani', 'Udon Thani',
        'Uthai Thani', 'Uttaradit', 'Yala', 'Yasothon']

# for i in range(0, 77):
start_year = 1901
stop_year = 1902

fig, ax = plt.subplots(figsize=(16, 16))

pre = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')

pre = pre.sel(lon=slice(96, 106), lat=slice(4, 21))

lon = pre['lon'].values
lat = pre['lat'].values

lon_step = float(lon[1] - lon[0])
lat_step = float(lat[1] - lat[0])

features = []
for year in tqdm(range(start_year, stop_year), leave=False,unit=' year'):
    ds_pr_year = pre.sel(time=slice(f'{year}', f'{year}'))
    time_values = ds_pr_year['time'].values
    time_dates = pd.to_datetime(time_values)
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

#     seen = set()
#     _day = data['time'].values
#     _day = [x for x in _day if not (x in seen or seen.add(x))]

# features = []

# for province in tqdm(provinces, leave=False, unit=' province'):
#     coord = shapefile[shapefile['NAME_1'] == province]

#     grid_in_polygon = data[data.geometry.intersects(coord.geometry.union_all())]
#     grid_in_polygon = grid_in_polygon[grid_in_polygon['time'] == '1901-01-16']
#     grid_in_polygon.plot(ax=ax, column='pre')
#     coord.geometry.boundary.plot(ax=ax, color='black', linewidth=0.5)
#     plt.show()
    # print(grid_in_polygon['geometry'])
    # for time in _day:
    #     grid_in = grid_in_polygon[grid_in_polygon['time'] == time]
    #     grid_area = grid_in.geometry.area
    #     intersection_area = grid_in.geometry.intersection(coord.geometry.unary_union).area
    #     intersection_percentage = (intersection_area / grid_area) * 100
    #     total_percentage = sum(intersection_percentage)
    #     precipitation_grid = (grid_in['pre'] * intersection_percentage)/total_percentage
    #     # grid_in['percentage'] = intersection_percentage
    #     grid_in['pre_grid'] = precipitation_grid

    #     for pre in grid_in.values:
    #         features.append({
    #             "type": "Feature",
    #             "geometry": mapping(pre[0]),
    #             "properties": {
    #                 "pre": pre[3],
    #                 "time": str(pre[2])[0:10],
    #             }
    #         })
    # geojson_data = {
    #     "type": "FeatureCollection",
    #     "features": features
    # }

    # output_file = f"./src/Geo-data/Era-Dataset/cru_data_{province}.json"
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(geojson_data, f, ensure_ascii=False, indent=4)
    
# print(f"Data year {year} has been saved file in folder {output_file}")

# coord.plot(ax=ax, color='white', edgecolor='black', alpha=1, label='Amnat Charoen')
# grid_in_polygon.plot(ax=ax, color='red', edgecolor='black', alpha=0.1, label='Grid in Amnat Charoen')
# plt.title('Grid in Amnat Charoen', fontsize=16)
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.legend()
# plt.show()

# coord = shapefile[shapefile['NAME_1'] == 'Amnat Charoen']





    # for idx, grid in grid_in_polygon.iterrows():
    #     print(grid['geometry'])
    #     grid_area = grid.geometry.area
        
        

    #     print(time, " " ,grid_in_polygon)

#         




    # grid_in = data[data.geometry.intersects(coord.geometry.union_all())]

    #     # print(f"Grid {idx}: intersects {intersection_percentage:.2f}%, pre: {temperature_value:.2f}")
        
    # # grid_in = data[data.geometry.intersects(coord.geometry.unary_union())]
    
    
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

