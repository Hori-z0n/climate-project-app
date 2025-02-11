import xarray as xr
import pandas as pd
import json
from shapely.geometry import mapping
import geopandas as gpd
import pandas as pd
import xclim
from province import province_coord 
from gridcal2 import calculate_weighted_temperature
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


ds_tmax = xr.open_dataset("C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc")
ds_tmin = xr.open_dataset("C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc")
ds_pr = xr.open_dataset("C:/Netcdf/TH_precipitation_day_1960-2022.nc")
# ds_pr = xr.open_dataset("C:/Netcdf/convert_precipitation.nc")
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

# คำนวณระยะห่างระหว่างพิกัด (step)
lon_step = float(ds_tmax['longitude'][1] - ds_tmax['longitude'][0])
lat_step = float(ds_tmax['latitude'][1] - ds_tmax['latitude'][0])

for year in tqdm(range(1960, 1966), leave=False, desc="Create by Year...", ascii=False, ncols=75,):

    data_tmax_year = ds_tmax.sel(time=str(year))
    data_tmin_year = ds_tmin.sel(time=str(year))
    data_pr_year = ds_pr.sel(time=str(year))
    tmax_monthly_mean = (data_tmax_year['mx2t'].resample(time='M').mean() - 273.15)

    tmin_monthly_mean = (data_tmin_year['mn2t'].resample(time='M').mean() - 273.15)
    pr_monthly_sum = data_pr_year['tp'].resample(time='M').sum() * 1000
    # print(data_pr_year['tp'].values)
    # data_pr_year['tp']*1000

    pre = data_pr_year.tp

    rx1day = xclim.indices.max_1day_precipitation_amount(pre, freq='ME')
    
    rx1day = rx1day*1000
    features = []
    lon, lat = tmax_monthly_mean['longitude'].values, tmax_monthly_mean['latitude'].values

    for month_idx, month in enumerate(tmax_monthly_mean['time'].values):
        tmax_values = tmax_monthly_mean.isel(time=month_idx).values
        tmin_values = tmin_monthly_mean.isel(time=month_idx).values
        pr_values = pr_monthly_sum.isel(time=month_idx).values
        rx1day_values = rx1day.isel(time=month_idx).values

        txx = tmax_values.max()
        tnn = tmin_values.min()

        for i, lon_value in enumerate(lon):
            for j, lat_value in enumerate(lat):
                tmax = tmax_values[j, i]
                tmin = tmin_values[j, i]
                pr = pr_values[j, i]
                rx = rx1day_values[j, i]
                if not pd.isnull(tmax) and not pd.isnull(tmin) and not pd.isnull(pr):
                    grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [grid_polygon]
                        },
                        "properties": {
                            "tmax": float(tmax),
                            "tmin": float(tmin),
                            "pre": float(pr),
                            "txx": float(txx),
                            "tnn": float(tnn),
                            "rx1day" :float(rx),
                            "month": pd.Timestamp(month).month
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
    features = []
    for month in range(1, 13):
        monthly_data = data[data['month'] == month]
        for region in province_coord():
            for province in region:
                name, geometry, region_name = province
                average_data, province_shape = calculate_weighted_temperature(name, shapefile, monthly_data)
                features.append({
                    "type": "Feature",
                        "geometry": mapping(geometry),
                        "properties": {
                            "name": name,
                            "region": region_name,
                            "month": month,
                            # "temperature": float(f"{average_data['temperature']:.2f}"),
                            # "dtr": float(f"{average_data['dtr']:.2f}"),
                            "pre": float(f"{average_data['pre']:.2f}"),
                            "tmin": float(f"{average_data['tmin']:.2f}"),
                            "tmax": float(f"{average_data['tmax']:.2f}"),
                            "rx1day": float(f"{average_data['rx1day']:.2f}"),
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