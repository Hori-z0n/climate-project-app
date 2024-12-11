import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping
from province import province_coord
from datetime import datetime, timedelta
import warnings
import json
import time

warnings.filterwarnings('ignore')
# import pandas as pd

cld = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.cld.dat.nc')
dtr = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.dtr.dat.nc')
# frs = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.frs.dat.nc')
# pet = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pet.dat.nc')
pre = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pre.dat.nc')
tmn = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmn.dat.nc')
tmp = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmp.dat.nc')
tmx = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmx.dat.nc')
# vap = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.vap.dat.nc')
# wet = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.wet.dat.nc')

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
        if(cru == 'dtr'):
            grid_value = grid['dtr']
        elif(cru == 'pre'):
            grid_value = grid['pre']
        elif(cru == 'tmn'):
            grid_value = grid['tmn']
        elif(cru == 'tmp'):
            grid_value = grid['tmp']
        elif(cru == 'tmx'):
            grid_value = grid['tmx']
        else:
            print("You select something wrong try again")
            break

        grid_value = np.nan_to_num(grid_value, nan=0.0)
        
        weighted_temp = grid_value * intersection_percentage_of_province
        total_weighted += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    average_value = total_weighted / total_percentage #if total_percentage != 0 else None
    return average_value, province_coord.geometry


start_year = 1901
stop_year = 1902
# stop_year = 2023
# year = 1901

for year in range(start_year, stop_year):
    data1 = dtr.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    time_values1 = data1['time'].values
    time_dates1 = pd.to_datetime(time_values1)
    data2 = pre.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    time_values2 = data2['time'].values
    time_dates2 = pd.to_datetime(time_values2)
    data3 = tmn.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    time_values3 = data3['time'].values
    time_dates3 = pd.to_datetime(time_values3)
    data4 = tmp.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    time_values4 = data4['time'].values
    time_dates4 = pd.to_datetime(time_values4)
    data5 = tmx.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    time_values5 = data5['time'].values
    time_dates5 = pd.to_datetime(time_values4)

    if len(time_dates1) == len(time_dates2) == len(time_dates3) == len(time_dates4) == len(time_dates5):
        print(f"Data for year {year} passed time consistency check.")
    else:
        print(f"Data for year {year} failed time consistency check.")
        # continue

    lon = cld['lon'].values
    lat = cld['lat'].values
    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])
    features = []
    for time_index, time in enumerate(time_dates1):
        month = time.month

        dtr_in_month = dtr.isel(time=time_index) 
        dtr_values = dtr_in_month['dtr'].values  
        
        pre_in_month = pre.isel(time=time_index) 
        pre_values = pre_in_month['pre'].values  
        
        tmn_in_month = tmn.isel(time=time_index) 
        tmn_values = tmn_in_month['tmn'].values  
        
        tmp_in_month = tmp.isel(time=time_index) 
        tmp_values = tmp_in_month['tmp'].values  
        
        tmx_in_month = tmx.isel(time=time_index) 
        tmx_values = tmx_in_month['tmx'].values  
        
        
        for i, lon_value in enumerate(lon):
            for j, lat_value in enumerate(lat):
                # cloud_cover = cld_values[j, i]  
                diural_temperature_range = dtr_values[j, i]
                precipitation = pre_values[j, i]
                minimum_temperature = tmn_values[j, i]
                mean_temperature = tmp_values[j, i]
                maximum_temperature = tmx_values[j, i]
                if not pd.isnull(diural_temperature_range) and not pd.isnull(precipitation) and not pd.isnull(minimum_temperature) and not pd.isnull(mean_temperature) and not pd.isnull(maximum_temperature):  
                    grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [grid_polygon]
                        },
                        "properties": {
                            "dtr": float(diural_temperature_range),
                            "pre": float(precipitation),
                            "tmn": float(minimum_temperature),
                            "tmp": float(mean_temperature),
                            "tmx": float(maximum_temperature),
                            "month": month 
                        }
                    })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    # print(geojson_data)
    # print(pd.DataFrame(geojson_data))
    # print(pd.Series(geojson_data))
    # print(gpd.GeoSeries(geojson_data))
    # print(gpd.GeoDataFrame(geojson_data))
    # print(gpd.GeoDataFrame(geojson_data['features']['properties'][:]))
    # data = pd.DataFrame.transpose(geojson_data['features'])
    # print(data.properties.values)

    # data = data.properties
    # gdf = gpd.GeoDataFrame(data.values, crs=4326)
    # gdf = gpd.GeoDataFrame(data.values, crs=3857)

    # print(gdf)
    output_file = f'./src/Geo-data/Year-Dataset/data_{year}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    print("GeoJSON data grid saved successfully.")

    data = gpd.read_file(f'./src/Geo-data/Year-Dataset/data_{year}.json')  
    shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    count = 0

    for month in range(1, 13):
        
        monthly_data = data[data['month'] == month]
        print(f"Processing data for Month {month}: {len(monthly_data)} entries")

        for region in province_coord(): 
            for province in region:
                name, geometry, region_name = province
                avg_dtr, province_shape1 = calculate_weighted_polygon(name, shapefile, monthly_data, cru='dtr')
                avg_pre, province_shape2 = calculate_weighted_polygon(name, shapefile, monthly_data, cru='pre')
                avg_tmn, province_shape3 = calculate_weighted_polygon(name, shapefile, monthly_data, cru='tmn')
                avg_tmp, province_shape4 = calculate_weighted_polygon(name, shapefile, monthly_data, cru='tmp')
                avg_tmx, province_shape5 = calculate_weighted_polygon(name, shapefile, monthly_data, cru='tmx')
                
                if (avg_dtr is not None and province_shape1 is not None) and (avg_pre is not None and province_shape2 is not None) and (avg_tmn is not None and province_shape3 is not None) and (avg_tmp is not None and province_shape4 is not None) and (avg_tmx is not None and province_shape5 is not None):
                    feature = {
                        "type": "Feature",
                        "geometry": mapping(geometry),  
                        "properties": {
                            "name": name,
                            "dtr": float(avg_dtr),
                            "pre": float(avg_pre),
                            "tmn": float(avg_tmn),
                            "tmp": float(avg_tmp),
                            "tmx": float(avg_tmx),
                            "region": region_name,  
                            "month": month
                        }
                    }
                    geojson_data["features"].append(feature)

                count += 1
                print(f"{count}: Month {month}, Province: {name}, Diural Temperature Range: {avg_dtr:.3f}")
                print(f"{count}: Month {month}, Province: {name}, Precipitation:            {avg_pre:.3f}")
                print(f"{count}: Month {month}, Province: {name}, Minimum Temperature:      {avg_tmn:.3f}")
                print(f"{count}: Month {month}, Province: {name}, Mean Temperature:         {avg_tmp:.3f}")
                print(f"{count}: Month {month}, Province: {name}, Maximum Temperature:      {avg_tmx:.3f}")

    output_geojson_path = f'./src/Geo-data/Year-Dataset/data_{year}.json'
    with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

    print("GeoJSON data polygon saved successfully.")
