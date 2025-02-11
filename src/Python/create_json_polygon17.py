import pandas as pd
import geopandas as gpd
# import netCDF4 as nc

import xarray as xr
import numpy as np
import json

from shapely.geometry import mapping
from tqdm import tqdm
from province import province_coord

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
    
    province_area = province_coord.geometry.union_all().area
    
    total_weighted = 0
    total_percentage = 0
    
    for idx, grid in grid_in_province.iterrows():

        intersection_area = grid.geometry.intersection(province_coord.geometry.union_all()).area
        
        intersection_percentage_of_province = (intersection_area / province_area) * 100
        grid_value = grid[cru]
        if(cru == ''):
            print("You not select something try again")
            break

        grid_value = np.nan_to_num(grid_value, nan=0.0)
        
        weighted_temp = grid_value * intersection_percentage_of_province
        total_weighted += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    average_value = total_weighted / total_percentage #if total_percentage != 0 else None
    return average_value, province_coord.geometry

precipitation = 'C:/Netcdf/TH_precipitation_day_1960-2022.nc'

precipitation = xr.open_dataset(precipitation)

precipitation['tp'] = precipitation['tp'] * 1000
precipitation['tp'].attrs['units'] = 'mm/day'
precipitation['tp'] = precipitation['tp'].assign_coords(precipitation.coords)

lon_step = float(precipitation['longitude'][1] - precipitation['longitude'][0])
lat_step = float(precipitation['latitude'][1] - precipitation['latitude'][0])
 
start_year = 1960
# stop_year = 1961
stop_year = 2023

thailand = gpd.read_file('C:/Users/konla/OneDrive/Desktop/climate-project-app/src/shapefile/gadm41_THA_1.shp')
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

x = precipitation['longitude'].values
y = precipitation['latitude'].values
for year in tqdm(range(start_year, stop_year), leave=False,unit=' year'):
    ds_pr_year = precipitation.sel(time=slice(f'{year}', f'{year}'))
    precipitation_monthly = ds_pr_year['tp'].resample(time='M').mean(dim='time')
    features = []
    for month_idx, month in enumerate(precipitation_monthly['time'].values):
        precipitation_value = precipitation_monthly.isel(time=month_idx).values
        for i, lon_value in enumerate(x):
            for j, lat_value in enumerate(y):
                pr = precipitation_value[j, i]
                if not pd.isnull(pr):
                    grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [grid_polygon]
                        },
                        "properties": {
                            "pre": float(pr),
                            "time": month
                            # "month": pd.Timestamp(month).month
                        }
                    })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    data = gpd.GeoDataFrame.from_features(geojson_data['features'])
    # print(data['time'])
    seen = set()
    _day = data['time'].values
    _day = [x for x in _day if not (x in seen or seen.add(x))]

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    features = []
    for time in np.array(_day):
        monthly_data = data[data['time'] == time]
        for region in province_coord():
            for province in region:
                name, geometry, region_name = province
                average_data, province_shape = calculate_weighted_polygon(name, shapefile, monthly_data, cru='pre')
                features.append({
                    "type": "Feature",
                        "geometry": mapping(geometry),
                        "properties": {
                            "name": name,
                            "region": region_name,
                            "time": str(time)[0:10],
                            "pre": float(average_data),
                        }
                })

        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

    output_file = f"./src/Geo-data/Era-Dataset/era_data_polygon_{year}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)
        
    print(f"Data year {year} has been saved file in folder {output_file}")