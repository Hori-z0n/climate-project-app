import pandas as pd
import geopandas as gpd
import xarray as xr
import numpy as np
import json
from province import province_coord
from shapely.geometry import mapping
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return[
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]
    ]

def calculate_weighted_polygon(province_name, shapefile, data, cru):
    province_coord = shapefile[shapefile['NAME_1'] == province_name]
    
    if province_coord.empty:
        print(f"No data in province : {province_name}")
        return None, None
    
    grid_in_province = data[data.geometry.intersects(province_coord.geometry.union_all())]

    province_area = province_coord.geometry.union_all().area

    total_weighted = 0
    total_percentage = 0
    for idx, grid in grid_in_province.iterrows():

        intersection_area = grid.geometry.intersection(province_coord.geometry.union_all()).area

        intersection_percentage_of_province = (intersection_area / province_area) * 100

        if (cru == 'pre'):
            grid_value = grid['pre']
        elif(cru == 'tmx'):
            grid_value = grid['tmx']
        elif(cru == 'tmn'):
            grid_value = grid['tmn']
        else:
            print("You select somthing wrong try again")
            break
    
        grid_value = np.nan_to_num(grid_value, nan=0.0)

        weighted_temp = grid_value * intersection_percentage_of_province
        total_weighted += weighted_temp
        total_percentage += intersection_percentage_of_province

    average_value = total_weighted / total_percentage 
    return average_value, province_coord.geometry

pre_data = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')
tmx_data = xr.open_dataset('C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc')
tmn_data = xr.open_dataset('C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc')
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

prec = {}
grid_value = []
dates = []
features = []
start_year = 1960
stop_year = 1961
ary_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
for year in range(start_year, stop_year):
    count = 1
    for date in tqdm(pre_data.sel(time=str(year))['time'], ascii=False, ncols=75, leave=False):
        ymd = str(date.values)[0:10]
        data_filtered1 = pre_data.sel(time=ymd)
        data_filtered2 = tmn_data.sel(time=ymd)
        data_filtered3 = tmx_data.sel(time=ymd)

        dates.append(ymd)

        data_avg1 = data_filtered1['tp'].mean(dim='time')
        data_avg2 = data_filtered2['mn2t'].mean(dim='time')
        data_avg3 = data_filtered3['mx2t'].mean(dim='time')
        time_dates1 = ymd.split('-')
        _day = time_dates1[2]
        _month = time_dates1[1]
        _year = time_dates1[0]

        pre_value = data_avg1.values
        tmn_value = data_avg2.values
        tmx_value = data_avg3.values

        lon = data_avg1.longitude.values
        lat = data_avg2.latitude.values

        lon_step = float(lon[1] - lon[0])
        lat_step = float(lat[1] - lat[0])

        for i, lon_value in tqdm(enumerate(lon), leave=False, desc="Create grid... ", unit=' grid', ncols=75):
            for j, lat_value in tqdm(enumerate(lat), leave=False, ncols=75):
                precipitation = pre_value[j, i]
                min_temperature = tmn_value[j, i]
                max_temperature = tmx_value[j, i]

                if not pd.isnull(precipitation):
                    grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                    features.append({
                        "type":"Feature",
                        "geometry":{
                            "type":"Polygon",
                            "coordinates":[grid_polygon]
                        },
                        "properties":{
                            "pre":float(precipitation),
                            "tmn":float(min_temperature),
                            "tmx":float(max_temperature),
                            "year":_year,
                            "month":_month,
                            "day":_day
                        }
                    })
        count += 1

    geojson_data = {
        "type":"FeatureCollection",
        "features":features
    }

    data = gpd.GeoDataFrame.from_features(geojson_data['features'])

    print(f"\nGeoJson {count} grid is create complete.")
    avg_pre = []
    avg_tmn = []
    avg_tmx = []
    for month in tqdm(ary_month[0:1], desc="Create polygon...", leave=False, ncols=75):
        monthly_data = data[data['month'] == month]
        seen = set()
        _day = []
        for day in monthly_data['day'].values:
            _day.append(day)
        _day = [x for x in _day if not (x in seen or seen.add(x))]
        day_length = len(_day)
        if monthly_data.empty == False:
            for day in tqdm(_day, desc="  ",ncols=100, leave=False):
                day_data = monthly_data[monthly_data['day'] == day]
                temporary = []
                for region in tqdm(province_coord(), desc="Loading region & province...", ascii=False, ncols=75, colour='yellow', leave=False):
                    for province in region:
                        Precipitation = 0
                        name, geometry, region_name = province
                        pre, province_shape1 = calculate_weighted_polygon(name, shapefile, day_data, cru='pre')
                        tmn, province_shape1 = calculate_weighted_polygon(name, shapefile, day_data, cru='tmn')
                        tmx, province_shape1 = calculate_weighted_polygon(name, shapefile, day_data, cru='tmx')
                        temporary.append(pre)
                print(len(temporary))
                avg_pre.append(temporary)
        print(len(avg_pre))

        #         print(len(avg_pre))

    #                     if(avg_pre is not None and province_shape1 is not None):
    #                         features = {
    #                             "type": "Feature",
    #                             "geometry":mapping(geometry),
    #                             "properties":{
    #                                 "name":name,
    #                                 "region":region_name,
    #                                 "month":month,
    #                                 "day":day,
    #                                 "pre":float(avg_pre),
    #                                 "tmn":float(avg_tmn),
    #                                 "tmx":float(avg_tmx)
    #                             }
    #                         }
    #                         geojson_data['features'].append(features)
    #     else:
    #         print("Error data is empty!")
        

    # output_geojson_path = f'G:/dayjson/data_{year}.json'
    # with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    #     json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

    # print(f"\nGeoJson file {year} polygon is create complete.")
    # print("\nNow saved")
