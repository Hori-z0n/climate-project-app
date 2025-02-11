
import climate_indices
import climate_library
from climate_library.climate_index import ClimateIndex

import xclim
import xclim.indices
# import xclim.core.units as xu
from xclim.testing import open_dataset
# from xclim.indices import standardized_precipitation_index
# from xclim.indices.stats import standardized_index_fit_params
from xclim.core.calendar import percentile_doy

import pandas as pd
import geopandas as gpd
# from netCDF4 import Dataset
import netCDF4 as nc

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scipy import stats as st

from shapely.geometry import mapping

import climate_V2
from province import province_coord

# from distributed import Client
# from dask.distributed import Client
# client = Client(n_workers=4, threads_per_worker=1, memory_limit='1GB')
# client.close()
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

# da_data = xr.open_dataset('C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc')
# ds_RR = da_data['pre']
# # ds_RR_Thailand= ds_RR.sel(lon=slice(96, 106), lat=slice(4, 21),time='1901')
# ds_RR_Thailand= ds_RR.sel(lon=slice(96, 106), lat=slice(4, 21),time=slice('2015', '2018'))

# i=3
# test = climate_V2.Climate(ds_RR_Thailand)
# ddata = test.calculate_spi(thresh=i,dimension='time',precip_var='pre')
# da_data['spi_3'] = ddata[9]
# # ddata[9].plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
# da_data['spi_3'].sel(lon=slice(96, 106), lat=slice(4, 21), time='2015').plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
# # plt.ylim(0,15)
# # plt.xlim(-20,15)
# plt.show()


#Standardized Precipitation Index Function
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
# gdf = gpd.read_file("./src/Geo-data/Year-Dataset/spi.json")
# gdf = gpd.read_file("./src/Geo-data/Year-Dataset/station.json")
# data = pd.read_csv('precipitation.csv')
# dates = data['time'].values
# data.drop('time', inplace=True, axis=1)

# index = pd.DataFrame()
# data = data.set_index(pd.date_range('1901', '2024', freq='M'))
# times = [3, 6, 9, 12, 24]
# for i in times:
#     x = spi(data['station1'], i)
#     data['spi_'+str(i)] = x[9]

# --------------------------------------------------------------------------------------

# features = []
# count = 0
# for d, s in tqdm(enumerate(data.columns), ascii=False, ncols=75, leave=False):
#     # print(data.columns[count], " ", gdf['station'][d])
#     for i in tqdm(times, leave=False):
#         x = spi(data[s], i)
#         index['spi_'+str(i)] = x[9]
#     # print(mapping(gdf['geometry'][d]))
#     # spi_6 = index['spi_6'].values
#     # spi_9 = index['spi_9'].values
#     # spi_12 = index['spi_12'].values
#     # spi_24 = index['spi_24'].values
#     features.append({
#             "type":"Feature",
#             "geometry":mapping(gdf['geometry'][d]),
#             "properties":{
#                 "station": gdf['station'][d],
#                 "spi_3":tuple(index['spi_3'].values),
#                 # "spi_6":index['spi_6'].values,
#                 # "spi_9":index['spi_9'].values,
#                 # "spi_12":index['spi_12'].values,
#                 # "spi_24":index['spi_24'].values
#             }
#         })
#     if data.columns[count] != gdf['station'][d]:
#         print("It have error")
    
#     count += 1

# geojson_data = {
#     "type": "FeatureCollection",
#     "features": features
# }

# data = gpd.GeoDataFrame.from_features(geojson_data['features'])
# print(data)
# print(data[0])

# output_geojson_path = "./src/Geo-data/Year-Dataset/spi.json"

# with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
#     json.dump(geojson_data, geojson_file, indent=236, ensure_ascii=False)

# --------------------------------------------------------------------------------------

# fig, axes = plt.subplots(nrows=5, figsize=(15, 10))
# plt.subplots_adjust(hspace=0.15)
# for i, ax in enumerate(axes):
#     col_scheme=np.where(data['spi_'+str(times[i])]>0, 'b','r')

#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#     ax.bar(data.index, data['spi_'+str(times[i])], width=25, align='center', color=col_scheme, label='SPI '+str(times[i]))
#     ax.axhline(y=0, color='k')
#     ax.xaxis.set_major_locator(mdates.YearLocator(2))
#     ax.legend(loc='upper right')
#     ax.set_yticks(range(-3,4), range(-3,4))
#     ax.set_ylabel('SPI', fontsize=12)
#     ax.tick_params(axis='x', labelrotation = 100)
#     if i<len(times)-1:
#         ax.set_xticks([],[])

# plt.show()

# --------------------------------------------------------------------------------------

start_year = 1965
stop_year = 1990
spi_data = []
# data = pd.DataFrame()

for year in range(start_year, stop_year):
    data = gpd.read_file(f"C:/Users/konla/OneDrive/Desktop/json/era_data_polygon_{year}.json")
    one = data[data['name'] == provinces[0]]
    for ds in one['pre'].values:
        spi_data.append(ds)

dict = {"pre":spi_data}
spi_data = pd.DataFrame(dict)
data = spi_data.set_index(pd.date_range(str(start_year), str(stop_year), freq='M'))
x = spi(data, 1)
data['spi'] = x[9]
print(data)
# times = [3, 6, 9, 12, 24]
# for i in times:
#     x = spi(data['pre'], i)
#     data['spi_'+str(i)] = x[9]

# fig, axes = plt.subplots(nrows=5, figsize=(15, 10))
# plt.subplots_adjust(hspace=0.15)
# for i, ax in enumerate(axes):
#     col_scheme=np.where(data['spi_'+str(times[i])]>0, 'b','r')

#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#     ax.bar(data.index, data['spi_'+str(times[i])], width=25, align='center', color=col_scheme, label='SPI '+str(times[i]))
#     ax.axhline(y=0, color='k')
#     ax.xaxis.set_major_locator(mdates.YearLocator(2))
#     ax.legend(loc='upper right')
#     ax.set_yticks(range(-3,4), range(-3,4))
#     ax.set_ylabel('SPI', fontsize=12)
    
#     if i<len(times)-1:
#         ax.set_xticks([],[])

# plt.show()
fig, axes = plt.subplots(nrows=1, figsize=(15, 10))
col_scheme=np.where(data['spi']>0, 'b','r')
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.bar(data.index, data['spi'], width=25, align='center', color=col_scheme)
axes.axhline(y=0, color='k')
axes.legend(loc='upper right')
axes.set_ylabel('SPI', fontsize=12)
plt.show()

