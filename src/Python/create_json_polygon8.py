import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
import json
from province import province_coord
from shapely.geometry import mapping
from scipy import stats as st
from tqdm import tqdm
import warnings
# warnings.filterwarnings('ignore')

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   
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
        if(cru == 'pre'):
            grid_value = grid['pre']
        elif(cru == 'tmx'):
            grid_value = grid['tmx']
        elif(cru == 'tmn'):
            grid_value = grid['tmn']
        else:
            print("You select something wrong try again")
            break

        grid_value = np.nan_to_num(grid_value, nan=0.0)
        
        weighted_temp = grid_value * intersection_percentage_of_province
        total_weighted += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    average_value = total_weighted / total_percentage #if total_percentage != 0 else None
    return average_value, province_coord.geometry

pre_data = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')
tmx_data = xr.open_dataset('C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc')
tmn_data = xr.open_dataset('C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc')
# start_year = 1960
# stop_year = 1961

prec = {}
grid_value = []
dates = []
features = []
year = 1960

for date in tqdm(pre_data.sel(time=str(year))['time'], ascii=False, ncols=75, leave=False):
    ymd = str(date.values)[0:10]
    data_filtered = pre_data.sel(time=ymd)
    dates.append(ymd)

    data_avg = data_filtered['tp'].mean(dim='time')
    time_dates1 = ymd.split('-')
    _day = time_dates1[2]
    _month = time_dates1[1]
    _year = time_dates1[0]
    pre_value = data_avg.values

    lon = data_avg.longitude.values
    lat = data_avg.latitude.values

    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])
    
    count = 0
    
    for i, lon_value in tqdm(enumerate(lon), desc="Create grid...",unit=' grid', ascii='0123456789#', ncols=75):
        for j, lat_value in tqdm(enumerate(lat), leave=False, ncols=75):
            precipitation = pre_value[j, i]
            if not pd.isnull(precipitation):
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "pre": float(precipitation),
                        "year": _year,
                        "month": _month ,
                        "day": _day
                    }
                })
            # print(_day, _month, _year)
    count += 1


geojson_data = {
    "type": "FeatureCollection",
    "features": features
}
data = gpd.GeoDataFrame.from_features(geojson_data['features'])

# output_file = f'./src/Geo-data/Year-Dataset/test_{year}.json'
# with open(output_file, 'w', encoding='utf-8') as f:
#     json.dump(geojson_data, f, ensure_ascii=False, indent=4)
print("\nGeoJSON data grid create successfully.")

shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

# start_month = 1
# stop_month = 2
# for info in data:
# print(data)

# for month in range()
_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', ]
count = 0
for month in _month:
    monthly_data = data[data['month'] == month]
    seen = set()
    _day = []
    for day in monthly_data['day'].values:
        _day.append(day)
    _day = [x for x in _day if not (x in seen or seen.add(x))]
    if monthly_data.empty == False:
        for day in _day:
            # print(str(day))
            day_data = monthly_data[monthly_data['day'] == day]
            for region in tqdm(province_coord(), desc="Loading region & province...", ascii=False, ncols=75, colour='yellow'): 
                for province in region:
                    name, geometry, region_name = province
                    avg_pre, province_shape1 = calculate_weighted_polygon(name, shapefile, day_data, cru='pre')
                    if (avg_pre is not None and province_shape1 is not None):
                        feature = {
                            "type": "Feature",
                            "geometry": mapping(geometry),  
                            "properties": {
                                "name": name,
                                "region": region_name,
                                "year": year,
                                "month": month,
                                "day": day,
                                "pre": float(avg_pre),
                            }
                        }
                        geojson_data["features"].append(feature)

                    count += 1
    else:
        print('Nothave')

output_geojson_path = f'./src/Geo-data/Year-Dataset/test_{year}.json'
with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

print("\nGeoJSON file polygon saved complete.")

    # if monthly_data:
    #     print(month, monthly_data)
    # else:
    #     print("Nonw")
# for info in data:
#             avg_dtr, province_shape1 = calculate_weighted_polygon(name, shapefile, info[0], cru='tp')

# print(data)

#     print(info)

# for region in tqdm(province_coord(), desc="Loading region & province...", ascii=False, ncols=75, colour='yellow'): 
#     for province in region:
#         name, geometry, region_name = province
# for year in tqdm(range(start_year, stop_year), desc="Create GeoJson...", ascii=False, ncols=75, leave=False):
#     data1 = pre_data.sel(time=str(year))
#     time_values1 = data1['time'].values
#     time_dates1 = pd.to_datetime(time_values1)
#     lon = pre_data['longitude'].values
#     lat = pre_data['latitude'].values
#     lon_step = float(lon[1] - lon[0])
#     lat_step = float(lat[1] - lat[0])
#     # print(data1['tp'].values)
#     # for data in data1.values:
#     #     print(data)
#     # for time_index, data in enumerate(time_dates1):
#     #     print(data)
#     # count = 0
#     for data in tqdm(data1['time'][0:62], ascii=False, ncols=75, leave=False):
#         time_values1 = str(data.values)[0:10]
#         # print(time_values1)
#         time_dates1 = time_values1.split('-')
#         pre_time = pre_data.isel(time=time_values1)
        
        # pre_values = pre_in_month['tp'].values
    #     time_dates1 = pd.to_datetime(time_values1)
        
    #     _day = time_dates1[2]
    #     _month = time_dates1[1]
    #     _year = time_dates1[0]
    #     # print(_day, _month, _year)

    #     print(_day, _month, _year, pre_in_month['tp'].mean().values)

    #     features = []
        
        

    #     # for time_index, time in tqdm(enumerate(time_dates1), desc="Create time Series...", ascii='0123456789#', ncols=75):
    #     # _day = time.day
    #     # _month = time.month
    #     # _year = time.year
    #     # print("day ", _day, "month ", _month, "year", _year)
    # #     pre_in_month = pre_data.isel(time=time_index) 
    # #     pre_values = pre_in_month['tp'].values
