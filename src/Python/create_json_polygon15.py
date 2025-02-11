import xarray as xr
import pandas as pd
import geojson as gpd
import json
from tqdm import tqdm
import xclim 
from xclim.core.calendar import percentile_doy

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return[
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]
    ]

tmx_temperature = xr.open_dataset("C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc")
tmp_temperature = xr.open_dataset('C:/Netcdf/TH_temperature_day_1940-2024.nc')
tmn_temperature = xr.open_dataset("C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc")
precipitation = xr.open_dataset("C:/Netcdf/TH_precipitation_day_1960-2022.nc")
shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

tmx_temperature['mx2t'] = tmx_temperature['mx2t'] - 273.15
tmx_temperature['mx2t'].attrs['units'] = 'degC'
tmx_temperature['mx2t'] = tmx_temperature['mx2t'].assign_coords(tmx_temperature.coords)

tmp_temperature['t2m'] = tmp_temperature['t2m'] - 273.15
tmp_temperature['t2m'].attrs['units'] = 'degC'
tmp_temperature['t2m'] = tmp_temperature['t2m'].assign_coords(tmp_temperature.coords)

tmn_temperature['mn2t'] = tmn_temperature['mn2t'] - 273.15
tmn_temperature['mn2t'].attrs['units'] = 'degC'
tmn_temperature['mn2t'] = tmn_temperature['mn2t'].assign_coords(tmn_temperature.coords)

precipitation['tp'] = precipitation['tp'] * 1000
precipitation['tp'].attrs['units'] = 'mm/days'
precipitation['tp'] = precipitation['tp'].assign_coords(precipitation.coords)

lon_step = float(tmx_temperature['longitude'][1] - tmx_temperature['longitude'][0])
lat_step = float(tmx_temperature['latitude'][1] - tmx_temperature['latitude'][0])


for year in range(1960, 1961):
    print(f"Processing data for the year {year}")
    features = []

    ds_tmin_year = tmn_temperature.sel(time=slice(f'{year}', f'{year}'))
    ds_tmax_year = tmx_temperature.sel(time=slice(f'{year}', f'{year}'))
    ds_pr_year = precipitation.sel(time=slice(f'{year}', f'{year}'))

    maxtemperature_values = ds_tmax_year['mx2t'].values
    mintemperature_values = ds_tmin_year['mn2t'].values
    precipitation_value = ds_pr_year['tp'].values

    total_grids = len(ds_tmin_year.latitude) * len(ds_tmin_year.longitude)
    with tqdm(total=total_grids, desc=f"Year {year}") as pbar:
        for lat in ds_tmin_year.latitude:
            for lon in ds_tmin_year.longitude:
                grid_data_tmin = ds_tmin_year['mn2t'].sel(latitude=lat, longitude=lon, method='nearest')
                grid_data_tmax = ds_tmax_year['mx2t'].sel(latitude=lat, longitude=lon, method='nearest')
                grid_data_pr = ds_pr_year['tp'].sel(latitude=lat, longitude=lon, method='nearest')
                for month in range(1, 13):
                    # เลือกข้อมูลรายเดือน
                    data_tmin_monthly = grid_data_tmin.sel(time=f'{year}-{month:02d}')
                    data_tmax_monthly = grid_data_tmax.sel(time=f'{year}-{month:02d}')
                    data_pr_monthly = grid_data_pr.sel(time=f'{year}-{month:02d}')

                    tmin_monthly = float(data_tmin_monthly.mean().values.item()) if len(data_tmin_monthly) > 0 else None
                    tmax_monthly = float(data_tmax_monthly.mean().values.item()) if len(data_tmax_monthly) > 0 else None
                    pr_monthly = float(data_pr_monthly.sum().values.item()) if len(data_pr_monthly) > 0 else None

                    grid_polygon = create_grid_polygon(lon.item(), lat.item(), lon_step, lat_step)

                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [grid_polygon]
                        },
                        "properties": {
                            "tmax": tmax_monthly,
                            "tmin": tmin_monthly,
                            "pre": pr_monthly,
                            "month": month
                        }
                    })
                pbar.update(1)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    output_file = f"./src/Geo-data/Era-Dataset/era_data_grid_{year}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    print(f"ข้อมูลสำหรับปี {year} ถูกบันทึกในไฟล์ {output_file}")

print("Processing complete!")