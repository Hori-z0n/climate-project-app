import json
import xclim
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import xarray as xr
import numpy as np
from shapely.geometry import mapping
from province import province_coord

precipitation = 'C:/Netcdf/TH_precipitation_day_1960-2022.nc'
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')
pre1 = xr.open_dataset(precipitation) 
print(pre1.sel(time='1960-01-01')['tp'].values)

pre = xr.open_dataset("C:/Netcdf/mm_TH_precipitation_day_1960-2022.nc")
# print(pre1)
# print(pre1['tp'].values)
# print("-"*100)
# pre = xr.open_dataset('C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc')
print(pre.sel(time='1960-01-01')['tp'].values)
def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # down left corner 
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # down right corner
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # up right corner
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # up left corner 
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # corner 1
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
        if(len(cru) != ''):
            grid_value = grid[cru]
        else:
            print("You not select something you need to try again")
            break

        grid_value = np.nan_to_num(grid_value, nan=0.0)
        
        weighted_temp = grid_value * intersection_percentage_of_province
        total_weighted += weighted_temp
        total_percentage += intersection_percentage_of_province
    
    average_value = total_weighted / total_percentage #if total_percentage != 0 else None
    return average_value, province_coord.geometry

pr = xr.open_dataset(precipitation)
pre = pr.tp

rx1day = xclim.indices.max_1day_precipitation_amount(pre, freq="M")


lon = rx1day['longitude']

lat =  rx1day['latitude']

lon_step = float(lon[1]-lon[0])

lat_step = float(lat[1]-lat[0])

features = []
# print(rx1day.sel(time='1960-01-01'))
for date in tqdm(rx1day['time'].values, leave=False, ascii=False, ncols=100):
# for date in rx1day['time'].values[0:12]:
    print(date)
    year = str(date)[0:4]
    
    _rx1day = rx1day.sel(time=year)
    print(_rx1day)

    thai_grid = _rx1day.clip(shapefile)
    thai_grid.plot(cmap='jet')
    _rx1day.plot(cmap='jet')

    lon = _rx1day['longitude']
    lat =  _rx1day['latitude']

    lon_step = float(lon[1]-lon[0])
    lat_step = float(lat[1]-lat[0])

    
    rx1day_value = _rx1day.values[0]
    
    for i, lon_value in tqdm(enumerate(lon), desc="Create longitude grid...",unit=' grid', leave=False, ncols=75):#i = 48
        for j, lat_value in tqdm(enumerate(lat), desc="Create latitude  grid...",unit=' grid', leave=False, ncols=75):# j = 72
            rx = rx1day_value[j, i]
            if not pd.isnull(rx):
                grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [grid_polygon]
                        },
                        "properties": {
                            "year": str(year),
                            "rx1day": float(rx) 
                        }
                    })
            
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

data = gpd.GeoDataFrame.from_features(geojson_data['features'])

geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for date in tqdm(rx1day['time'].values, leave=False, ascii=False, ncols=100):
    
    year = str(date)[0:4]

    data_year = data[data['year'] == year]
    

    for region in tqdm(province_coord(), desc=f"Loading region & province {date}...", ascii=False, ncols=150, colour='yellow'): 
        for province in region:
            name, geometry, region_name = province
            avg_rx, province_shape = calculate_weighted_polygon(name, shapefile, data_year, cru='rx1day')
            if avg_rx is not None:
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geometry),  
                    "properties": {
                        "name": name,
                        "region": region_name,
                        "year": year,
                        "rx1day":float(avg_rx)
                    }
                }
                geojson_data["features"].append(feature)

output_geojson_path = f'./src/Geo-data/Year-Dataset/rx1day.json'
with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)
print(output_geojson_path + " is saved.")

print("\nGeoJSON file polygon saved complete.")