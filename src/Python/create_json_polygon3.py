import cartopy.feature as cfeature
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping
import json
from tqdm import tqdm, trange
import warnings
warnings.filterwarnings('ignore')

# cld = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.cld.dat.nc')
dtr = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.dtr.dat.nc')
pre = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pre.dat.nc')
tmn = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmn.dat.nc')
tmp = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmp.dat.nc')
tmx = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmx.dat.nc')

start_year = 1901
stop_year = 1902
start_month = 1
stop_month = 13

features = []

txx_year_value = []
tnn_year_value = []
for year in tqdm(range(start_year, stop_year)):
    path = f'C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/Year-Dataset/data_{year}.json'
    data = gpd.read_file(path)
    for i in tqdm(range(start_month, stop_month), desc="Start Create Value Climate Extreme Index...", ascii=False, ncols=75, colour='orange'):
        # max_value = {'month':int(), 'name':str(), 'temperature':0.0}
        # min_value = {'month':int(), 'name':str(), 'temperature':100.0}
        max_value = {'name':str(), 'temperature':0.0}
        min_value = {'name':str(), 'temperature':100.0}
        for ds in data[data['month'] == i].values:
            province = ds[0]
            month = ds[2]
            _tmn = ds[5]
            _tmx = ds[7]
            if max_value['temperature'] < _tmx:
                max_value['temperature'] = _tmx
                max_value['name'] = province
                # max_value['month'] = month
            elif max_value['temperature'] > _tmx:
                continue
            else:
                print('something is wrong')

            if min_value['temperature'] > _tmn:
                min_value['temperature'] = _tmn
                min_value['name'] = province
                # min_value['month'] = month
            elif min_value['temperature'] < _tmn:
                continue
            else:
                print('something is wrong')
        txx_year_value.append(max_value)
        tnn_year_value.append(min_value)

    print("\nGeoJSON data Climate Extreme Index create successfully.")

    with open(path) as f:
        data = json.load(f)

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for month in tqdm(range(start_month, stop_month), desc="Start Create Value Climate Extreme Index...", ascii=False, ncols=75, colour='orange'):
        for i in range(0, 924):
            features = {
                "type": "Feature",
                "geometry": {
                    "type":data['features'][i]['geometry']['type'],
                    "coordinates": data['features'][i]['geometry']['coordinates']
                },  
                "properties": {
                'name': data['features'][i]['properties']['name'],
                'region': data['features'][i]['properties']['region'],
                'month': data['features'][i]['properties']['month'],
                'pre': data['features'][i]['properties']['pre'],
                'dtr': data['features'][i]['properties']['dtr'], 
                'tmn': data['features'][i]['properties']['tmn'], 
                'tmp': data['features'][i]['properties']['tmp'], 
                'tmx': data['features'][i]['properties']['tmx'],
                'txx': txx_year_value[month-1],
                'tnn': tnn_year_value[month-1]
                }
            }
            geojson_data['features'].append(features)

    output_geojson_path = f'./src/Geo-data/Year-Dataset/data_{year}_V2.json'
    with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

print("\nGeoJSON file polygon saved complete.")
