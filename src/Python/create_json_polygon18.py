# import climate_indices
# import climate_indices.indices
# import climate_library
# from climate_library.climate_index import ClimateIndex
import cartopy.crs as ccrs
import xclim
import xclim.indices
# import xclim.core.units as xu
from xclim.testing import open_dataset
# from xclim.indices import standardized_precipitation_index
# from xclim.indices.stats import standardized_index_fit_params
# from xclim.core.calendar import percentile_doy

import pandas as pd
import geopandas as gpd
# from netCDF4 import Dataset
import netCDF4 as nc

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

from scipy import stats as st
import json
from shapely.geometry import mapping

import climate_V2
from province import province_coord

import warnings
warnings.filterwarnings('ignore')


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

def spi(ds, thresh):
    #ds - data ; thresh - time interval / scale
    
    #Rolling Mean / Moving Averages
    ds_ma = ds.rolling(thresh, center=False).mean()
    
    #Natural log of moving averages
    ds_In = np.log(ds_ma)
    ds_In[ np.isinf(ds_In) == True] = np.nan  #Change infinity to NaN
    
    #Overall Mean of Moving Averages
    ds_mu = np.nanmean(ds_ma)
    
    #Summation of Natural log of moving averages
    ds_sum = np.nansum(ds_In)
        
    #Computing essentials for gamma distribution
    n = len(ds_In[thresh-1:])                  #size of data
    A = np.log(ds_mu) - (ds_sum/n)             #Computing A
    alpha = (1/(4*A))*(1+(1+((4*A)/3))**0.5)   #Computing alpha  (a)
    beta = ds_mu/alpha                         #Computing beta (scale)
    
    #Gamma Distribution (CDF)
    gamma = st.gamma.cdf(ds_ma, a=alpha, scale=beta)  
    
    #Standardized Precipitation Index   (Inverse of CDF)
    norm_spi = st.norm.ppf(gamma, loc=0, scale=1)  #loc is mean and scale is standard dev.
    
    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi


# data1 = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/json/era_data_polygon_1960.json")
# data2 = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/json/era_data_polygon_1961.json")
# if data1.crs != data2.crs:
#     data2 = data2.to_crs(data1.crs)

shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')
fig, ax = plt.subplots(figsize=(10, 10))
data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/json/cru_data.json")
coord = shapefile[shapefile['NAME_1'] == 'Ang Thong']
grid_in_polygon = data[data.geometry.intersects(coord.geometry.union_all())]
# grid_in = grid_in_polygon[grid_in_polygon['time'] == time]
grid_area = grid_in_polygon.geometry.area
intersection_area = grid_in_polygon.geometry.intersection(coord.geometry.unary_union).area
intersection_percentage = (intersection_area / grid_area) * 100
total_percentage = sum(intersection_percentage)
precipitation_grid = (grid_in_polygon['pre'] * intersection_percentage)/total_percentage
# grid_in['percentage'] = intersection_percentage
grid_in_polygon['pre_grid'] = precipitation_grid
features = []
print(grid_in_polygon)
for pre in grid_in_polygon.values:
    features.append({
        "type": "Feature",
        "geometry": mapping(pre[2]),
        "properties": {
            "pre": pre[3],
            "time": str(pre[1])[0:10],
        }
    })
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}
output_file = f"./src/Geo-data/Era-Dataset/cru_data_Ang Thong.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=4)
    
# grid_in_polygon = grid_in_polygon[grid_in_polygon['time'] == '1901-01-16']
# grid_in_polygon.plot(ax=ax, column='pre_grid')
# coord.geometry.boundary.plot(ax=ax, color='black', linewidth=0.5)
# plt.show()
# print(data1)
# print(data2)
# spatial_joined_gdf = gpd.sjoin(data1, data2, how='inner')
# print(spatial_joined_gdf)
start_year = 1901
stop_year = 2024
# for province in provinces:
# spi_data = gpd.GeoDataFrame()
spi_data = []
# data = pd.DataFrame()
# data = data.set_index(pd.date_range('1960', '2022', freq='M'))
print(data)
for year in range(start_year, stop_year):
    data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/json/era_data_polygon_{year}.json")
    # data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/json/cru_data_{year}.json")
    print(data)
    one = data[data['name'] == provinces[0]]
    for ds in one['pre'].values:
        spi_data.append(ds)
# time = np.arange('1960-01', '2023-01', dtype='datetime64[M]')
# ds = xr.Dataset({'pre':(['time'],spi_data)},coords={'time':time})
# data = climate_indices.indices.spi(values=ds['pre'].values, scale=3,distribution='gamma', data_start_year=1960, calibration_year_initial=1960, calibration_year_final=2022, periodicity='monthly')
# print(data)

# dict = {"pre":spi_data}
spi_data = pd.DataFrame(dict)
data = spi_data.set_index(pd.date_range(str(start_year), str(stop_year), freq='M'))
x = spi(data, 12)
data['spi'] = x[9]
print(data)

# fig, axes = plt.subplots(nrows=1, figsize=(15, 10))
# col_scheme=np.where(data['spi']>0, 'b','r')
# axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# axes.bar(data.index, data['spi'], width=25, align='center', color=col_scheme)
# axes.axhline(y=0, color='k')
# axes.legend(loc='upper right')
# axes.set_ylabel('SPI', fontsize=12)
# plt.show()

#     temp = gpd.GeoDataFrame()
#     temp.sjoin(spi_data, one)
# # x = spi(one['pre'], 3)
# print(temp)


# print(spi_data)
# x = spi(spi_data, 3)

    # spi_data.append(one)
#     for i in one['pre']:
#         print(i)
# print(spi_data['name'])