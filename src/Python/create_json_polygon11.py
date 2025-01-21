import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import json
import numpy as np
import xarray as xr
import pandas as pd
import json

# โหลดข้อมูลจาก NetCDF
tmp = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmp.dat.nc')
dtr = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.dtr.dat.nc')
pre = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
tmn = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmn.dat.nc')
tmx = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.tmx.dat.nc')

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

for i in range(0, 10):  # ตัวอย่างวนลูป 10 ปี
    year = 1901 + i
    temp = tmp.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    dtr_temp = dtr.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    pre_temp = pre.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    tmn_temp = tmn.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))
    tmx_temp = tmx.sel(lon=slice(96, 106), lat=slice(4, 21), time=str(year))

    time_values = temp['time'].values
    time_dates = pd.to_datetime(time_values)

    lon = temp['lon'].values
    lat = temp['lat'].values
    lon_step = float(lon[1] - lon[0])
    lat_step = float(lat[1] - lat[0])

    features = []
    for time_index, time in enumerate(time_dates):  
        month = time.month
        temp_in_month = temp.isel(time=time_index)
        dtr_in_month = dtr_temp.isel(time=time_index)
        pre_in_month = pre_temp.isel(time=time_index)
        tmn_in_month = tmn_temp.isel(time=time_index)
        tmx_in_month = tmx_temp.isel(time=time_index)
        
        temp_values = temp_in_month['tmp'].values
        dtr_values = dtr_in_month['dtr'].values
        pre_values = pre_in_month['pre'].values
        tmn_values = tmn_in_month['tmn'].values
        tmx_values = tmx_in_month['tmx'].values
        
        for i, lon_value in enumerate(lon):
            for j, lat_value in enumerate(lat):
                temperature = temp_values[j, i]
                diurnal_range = dtr_values[j, i]
                precipitation = pre_values[j, i]
                min_temp = tmn_values[j, i]
                max_temp = tmx_values[j, i]

                if not pd.isnull(temperature):
                    grid_polygon = create_grid_polygon(lon_value, lat_value, lon_step, lat_step)
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [grid_polygon]
                        },
                        "properties": {
                            "temperature": float(temperature),
                            "dtr": float(diurnal_range) if not pd.isnull(diurnal_range) else None,
                            "pre": float(precipitation) if not pd.isnull(precipitation) else None,
                            "tmin": float(min_temp) if not pd.isnull(min_temp) else None,
                            "tmax": float(max_temp) if not pd.isnull(max_temp) else None,
                            "month": month
                        }
                    })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    output_file = f"../Geo-data/Year-Dataset/data_grid_index_{year}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=4)

    print(f"Save to location : {output_file}")



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




