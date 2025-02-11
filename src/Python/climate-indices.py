# https://github.com/shiv3679/climate-indices
# https://github.com/monocongo/climate_indices
# https://github.com/KWRProjects/Meteorology-climate_indices
# https://github.com/KNMI/Indices_icclim_ClipC
# https://github.com/SantanderMetGroup/climate4R.indices
# https://github.com/XiaZhang1113/indices_python
# https://github.com/jeffjay88/Climate_Indices
# https://github.com/fmidev/resiclim-climateatlas
# https://github.com/monocongo/climate_indices/blob/master/docs/index.rst
# https://github.com/gabrielmpp/climate_indices
# https://github.com/topics/climate-indicators
# https://github.com/Climandes/ClimIndVis
# https://github.com/Ouranosinc/mat-clim-indices
# https://github.com/AgrDataSci/climatrends
# https://github.com/nicolasfauchereau/ACRE_workshop
# https://github.com/cerfacs-globc/icclim
# https://github.com/ARCCSS-extremes/climpact2/blob/master/ancillary/climate.indices.csv
# https://github.com/AusClimateService/indices
# https://github.com/ECA-D/gridclimind
# https://github.com/yyr/climate_indices
# https://github.com/drewpolasky/simple_pyclimdex
# https://climate-indices.readthedocs.io/en/latest/
# https://github.com/Ouranosinc/xclim
# https://github.com/royalosyin/Python-Practical-Application-on-Climate-Variability-Studies
# https://scholar.google.com/citations?user=awGdXUsAAAAJ&hl=en
# https://github.com/ECCC-CDAS/RClimDex/tree/master
# import climate_indices
# import climate_indices.compute
# import climate_indices.indices
# import climate_library
# from climate_library.climate_index import ClimateIndex

import xclim
# import xclim.indices
# import xclim.core.units as xu
# from xclim.testing import open_dataset
# from xclim.indices import standardized_precipitation_index
# from xclim.indices.stats import standardized_index_fit_params
# from xclim.core.calendar import percentile_doy

import pandas as pd
import geopandas as gpd
# from netCDF4 import Dataset
import netCDF4 as nc

import xarray as xr
import numpy as np
import json
from tqdm import tqdm 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime
from scipy import stats as st
# from metpy.units import units
from shapely.geometry import mapping
# import pint

# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

# import climate_V2
# from province import province_coord

# from distributed import Client
# from dask.distributed import Client
# client = Client(n_workers=4, threads_per_worker=1, memory_limit='1GB')
# client.close()
import warnings
warnings.filterwarnings('ignore')

# shapefile = gpd.read_file('src/Geo-data/shapefile-lv1-thailand.json')

# cld = 'C:/Netcdf/cru_ts4.08.1901.2023.cld.dat.nc'
# dtr = 'C:/Netcdf/cru_ts4.08.1901.2023.dtr.dat.nc'
# frs = 'C:/Netcdf/cru_ts4.08.1901.2023.frs.dat.nc'
# pet = 'C:/Netcdf/cru_ts4.08.1901.2023.pet.dat.nc'
# pre = 'C:/Netcdf/cru_ts4.08.1901.2023.pre.dat.nc'
# tmn = 'C:/Netcdf/cru_ts4.08.1901.2023.tmn.dat.nc'
# tmp = 'C:/Netcdf/cru_ts4.08.1901.2023.tmp.dat.nc'
# tmx = 'C:/Netcdf/cru_ts4.08.1901.2023.tmx.dat.nc'
# vap = 'C:/Netcdf/cru_ts4.08.1901.2023.vap.dat.nc'
# wet = 'C:/Netcdf/cru_ts4.08.1901.2023.wet.dat.nc'

# temperature = 'C:/Netcdf/ERA5-post-processed-daily-statistics-on-single-levels-from-1940-to-present-tmp.nc'
# precipitation = 'C:/Netcdf/ERA5-post-processed-daily-statistics-on-single-levels-from-1940-to-present.nc'
# precipitation = 'C:/Netcdf/TH_precipitation_day-1940.nc'
# precipitation = 'C:/Netcdf/convert_precipitation.nc'
# precipitation = 'C:/Netcdf/TH_precipitation_day_1960-2022.nc'
# max_temperature = 'C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc'
# min_temperature = 'C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc'
# temperature = 'C:/Netcdf/TH_temperature_day_1940-2024.nc'

# shapefile = gpd.read_file('./src/Geo-data/thailand-Geo.json')

# ds = xr.open_dataset(pre)

# filename = 'cru_time.txt'
# try:
#     file = open(filename, 'w')
#     for time in ds['time'].values:
#         file.write(str(time)[0:10] + '\n')
#     file.close()
# except IOError as e:
#     print(e)

# try:
#     with open(filename, 'r') as file:
#         readmsg = file.readline()
#         result = []
#         for data in readmsg:
#             result.append(data.strip('\n'))
#     for msg in result:
#         print(msg)
#     file.close()
# except IOError as e:
#     print(e)

# try:
#     with open(filename, 'r') as file:
#         readmsg = file.readlines()
#         result = []
#         for data in readmsg:
#             result.append(data.strip('\n'))
    # for msg in result:
    #     print(msg)

#     file.close()
# except IOError as e:
#     print(e)
# year = [ "1901-01-16", "1901-02-15", "1901-03-16", "1901-04-16", "1901-05-16", "1901-06-16", "1901-07-16", "1901-08-16", "1901-09-16", "1901-10-16", "1901-11-16", "1901-12-16", "1902-01-16", "1902-02-15", "1902-03-16", "1902-04-16", "1902-05-16", "1902-06-16", "1902-07-16", "1902-08-16",
#          "1902-09-16", "1902-10-16", "1902-11-16", "1902-12-16", "1903-01-16", "1903-02-15", "1903-03-16", "1903-04-16", "1903-05-16", "1903-06-16", "1903-07-16", "1903-08-16", "1903-09-16", "1903-10-16", "1903-11-16", "1903-12-16", "1904-01-16", "1904-02-15", "1904-03-16", "1904-04-16",
#          "1904-05-16", "1904-06-16", "1904-07-16", "1904-08-16", "1904-09-16", "1904-10-16", "1904-11-16", "1904-12-16", "1905-01-16", "1905-02-15", "1905-03-16", "1905-04-16", "1905-05-16", "1905-06-16", "1905-07-16", "1905-08-16", "1905-09-16", "1905-10-16", "1905-11-16", "1905-12-16",
#          "1906-01-16", "1906-02-15", "1906-03-16", "1906-04-16", "1906-05-16", "1906-06-16", "1906-07-16", "1906-08-16", "1906-09-16", "1906-10-16", "1906-11-16", "1906-12-16", "1907-01-16", "1907-02-15", "1907-03-16", "1907-04-16", "1907-05-16", "1907-06-16", "1907-07-16", "1907-08-16",
#          "1907-09-16", "1907-10-16", "1907-11-16", "1907-12-16", "1908-01-16", "1908-02-15", "1908-03-16", "1908-04-16", "1908-05-16", "1908-06-16", "1908-07-16", "1908-08-16", "1908-09-16", "1908-10-16", "1908-11-16", "1908-12-16", "1909-01-16", "1909-02-15", "1909-03-16", "1909-04-16",
#          "1909-05-16", "1909-06-16", "1909-07-16", "1909-08-16", "1909-09-16", "1909-10-16", "1909-11-16", "1909-12-16", "1910-01-16", "1910-02-15", "1910-03-16", "1910-04-16", "1910-05-16", "1910-06-16", "1910-07-16", "1910-08-16", "1910-09-16", "1910-10-16", "1910-11-16", "1910-12-16",
#          "1911-01-16", "1911-02-15", "1911-03-16", "1911-04-16", "1911-05-16", "1911-06-16", "1911-07-16", "1911-08-16", "1911-09-16", "1911-10-16", "1911-11-16", "1911-12-16", "1912-01-16", "1912-02-15", "1912-03-16", "1912-04-16", "1912-05-16", "1912-06-16", "1912-07-16", "1912-08-16",
#          "1912-09-16", "1912-10-16", "1912-11-16", "1912-12-16", "1913-01-16", "1913-02-15", "1913-03-16", "1913-04-16", "1913-05-16", "1913-06-16", "1913-07-16", "1913-08-16", "1913-09-16", "1913-10-16", "1913-11-16", "1913-12-16", "1914-01-16", "1914-02-15", "1914-03-16", "1914-04-16",
#          "1914-05-16", "1914-06-16", "1914-07-16", "1914-08-16", "1914-09-16", "1914-10-16", "1914-11-16", "1914-12-16", "1915-01-16", "1915-02-15", "1915-03-16", "1915-04-16", "1915-05-16", "1915-06-16", "1915-07-16", "1915-08-16", "1915-09-16", "1915-10-16", "1915-11-16", "1915-12-16", 
#          "1916-01-16", "1916-02-15", "1916-03-16", "1916-04-16", "1916-05-16", "1916-06-16", "1916-07-16", "1916-08-16", "1916-09-16", "1916-10-16", "1916-11-16", "1916-12-16", "1917-01-16", "1917-02-15", "1917-03-16", "1917-04-16", "1917-05-16", "1917-06-16", "1917-07-16", "1917-08-16",
#          "1917-09-16", "1917-10-16", "1917-11-16", "1917-12-16", "1918-01-16", "1918-02-15", "1918-03-16", "1918-04-16", "1918-05-16", "1918-06-16", "1918-07-16", "1918-08-16", "1918-09-16", "1918-10-16", "1918-11-16", "1918-12-16", "1919-01-16", "1919-02-15", "1919-03-16", "1919-04-16",
#          "1919-05-16", "1919-06-16", "1919-07-16", "1919-08-16", "1919-09-16", "1919-10-16", "1919-11-16", "1919-12-16", "1920-01-16", "1920-02-15", "1920-03-16", "1920-04-16", "1920-05-16", "1920-06-16", "1920-07-16", "1920-08-16", "1920-09-16", "1920-10-16", "1920-11-16", "1920-12-16",
#          "1921-01-16", "1921-02-15", "1921-03-16", "1921-04-16", "1921-05-16", "1921-06-16", "1921-07-16", "1921-08-16", "1921-09-16", "1921-10-16", "1921-11-16", "1921-12-16", "1922-01-16", "1922-02-15", "1922-03-16", "1922-04-16", "1922-05-16", "1922-06-16", "1922-07-16", "1922-08-16",
#          "1922-09-16", "1922-10-16", "1922-11-16", "1922-12-16", "1923-01-16", "1923-02-15", "1923-03-16", "1923-04-16", "1923-05-16", "1923-06-16", "1923-07-16", "1923-08-16", "1923-09-16", "1923-10-16", "1923-11-16", "1923-12-16", "1924-01-16", "1924-02-15", "1924-03-16", "1924-04-16",
#          "1924-05-16", "1924-06-16", "1924-07-16", "1924-08-16", "1924-09-16", "1924-10-16", "1924-11-16", "1924-12-16", "1925-01-16", "1925-02-15", "1925-03-16", "1925-04-16", "1925-05-16", "1925-06-16", "1925-07-16", "1925-08-16", "1925-09-16", "1925-10-16", "1925-11-16", "1925-12-16", 
#          "1926-01-16", "1926-02-15", "1926-03-16", "1926-04-16", "1926-05-16", "1926-06-16", "1926-07-16", "1926-08-16", "1926-09-16", "1926-10-16", "1926-11-16", "1926-12-16", "1927-01-16", "1927-02-15", "1927-03-16", "1927-04-16", "1927-05-16", "1927-06-16", "1927-07-16", "1927-08-16", 
#          "1927-09-16", "1927-10-16", "1927-11-16", "1927-12-16", "1928-01-16", "1928-02-15", "1928-03-16", "1928-04-16", "1928-05-16", "1928-06-16", "1928-07-16", "1928-08-16", "1928-09-16", "1928-10-16", "1928-11-16", "1928-12-16", "1929-01-16", "1929-02-15", "1929-03-16", "1929-04-16", 
#          "1929-05-16", "1929-06-16", "1929-07-16", "1929-08-16", "1929-09-16", "1929-10-16", "1929-11-16", "1929-12-16", "1930-01-16", "1930-02-15", "1930-03-16", "1930-04-16", "1930-05-16", "1930-06-16", "1930-07-16", "1930-08-16", "1930-09-16", "1930-10-16", "1930-11-16", "1930-12-16", 
#          "1931-01-16", "1931-02-15", "1931-03-16", "1931-04-16", "1931-05-16", "1931-06-16", "1931-07-16", "1931-08-16", "1931-09-16", "1931-10-16", "1931-11-16", "1931-12-16", "1932-01-16", "1932-02-15", "1932-03-16", "1932-04-16", "1932-05-16", "1932-06-16", "1932-07-16", "1932-08-16", 
#          "1932-09-16", "1932-10-16", "1932-11-16", "1932-12-16", "1933-01-16", "1933-02-15", "1933-03-16", "1933-04-16", "1933-05-16", "1933-06-16", "1933-07-16", "1933-08-16", "1933-09-16", "1933-10-16", "1933-11-16", "1933-12-16", "1934-01-16", "1934-02-15", "1934-03-16", "1934-04-16", 
#          "1934-05-16", "1934-06-16", "1934-07-16", "1934-08-16", "1934-09-16", "1934-10-16", "1934-11-16", "1934-12-16", "1935-01-16", "1935-02-15", "1935-03-16", "1935-04-16", "1935-05-16", "1935-06-16", "1935-07-16", "1935-08-16", "1935-09-16", "1935-10-16", "1935-11-16", "1935-12-16", 
#          "1936-01-16", "1936-02-15", "1936-03-16", "1936-04-16", "1936-05-16", "1936-06-16", "1936-07-16", "1936-08-16", "1936-09-16", "1936-10-16", "1936-11-16", "1936-12-16", "1937-01-16", "1937-02-15", "1937-03-16", "1937-04-16", "1937-05-16", "1937-06-16", "1937-07-16", "1937-08-16", 
#          "1937-09-16", "1937-10-16", "1937-11-16", "1937-12-16", "1938-01-16", "1938-02-15", "1938-03-16", "1938-04-16", "1938-05-16", "1938-06-16", "1938-07-16", "1938-08-16", "1938-09-16", "1938-10-16", "1938-11-16", "1938-12-16", "1939-01-16", "1939-02-15", "1939-03-16", "1939-04-16", 
#          "1939-05-16", "1939-06-16", "1939-07-16", "1939-08-16", "1939-09-16", "1939-10-16", "1939-11-16", "1939-12-16", "1940-01-16", "1940-02-15", "1940-03-16", "1940-04-16", "1940-05-16", "1940-06-16", "1940-07-16", "1940-08-16", "1940-09-16", "1940-10-16", "1940-11-16", "1940-12-16", 
#          "1941-01-16", "1941-02-15", "1941-03-16", "1941-04-16", "1941-05-16", "1941-06-16", "1941-07-16", "1941-08-16", "1941-09-16", "1941-10-16", "1941-11-16", "1941-12-16", "1942-01-16", "1942-02-15", "1942-03-16", "1942-04-16", "1942-05-16", "1942-06-16", "1942-07-16", "1942-08-16", 
#          "1942-09-16", "1942-10-16", "1942-11-16", "1942-12-16", "1943-01-16", "1943-02-15", "1943-03-16", "1943-04-16", "1943-05-16", "1943-06-16", "1943-07-16", "1943-08-16", "1943-09-16", "1943-10-16", "1943-11-16", "1943-12-16", "1944-01-16", "1944-02-15", "1944-03-16", "1944-04-16", 
#          "1944-05-16", "1944-06-16", "1944-07-16", "1944-08-16", "1944-09-16", "1944-10-16", "1944-11-16", "1944-12-16", "1945-01-16", "1945-02-15", "1945-03-16", "1945-04-16", "1945-05-16", "1945-06-16", "1945-07-16", "1945-08-16", "1945-09-16", "1945-10-16", "1945-11-16", "1945-12-16", 
#          "1946-01-16", "1946-02-15", "1946-03-16", "1946-04-16", "1946-05-16", "1946-06-16", "1946-07-16", "1946-08-16", "1946-09-16", "1946-10-16", "1946-11-16", "1946-12-16", "1947-01-16", "1947-02-15", "1947-03-16", "1947-04-16", "1947-05-16", "1947-06-16", "1947-07-16", "1947-08-16", 
#          "1947-09-16", "1947-10-16", "1947-11-16", "1947-12-16", "1948-01-16", "1948-02-15", "1948-03-16", "1948-04-16", "1948-05-16", "1948-06-16", "1948-07-16", "1948-08-16", "1948-09-16", "1948-10-16", "1948-11-16", "1948-12-16", "1949-01-16", "1949-02-15", "1949-03-16", "1949-04-16", 
#          "1949-05-16", "1949-06-16", "1949-07-16", "1949-08-16", "1949-09-16", "1949-10-16", "1949-11-16", "1949-12-16", "1950-01-16", "1950-02-15", "1950-03-16", "1950-04-16", "1950-05-16", "1950-06-16", "1950-07-16", "1950-08-16", "1950-09-16", "1950-10-16", "1950-11-16", "1950-12-16", 
#          "1951-01-16", "1951-02-15", "1951-03-16", "1951-04-16", "1951-05-16", "1951-06-16", "1951-07-16", "1951-08-16", "1951-09-16", "1951-10-16", "1951-11-16", "1951-12-16", "1952-01-16", "1952-02-15", "1952-03-16", "1952-04-16", "1952-05-16", "1952-06-16", "1952-07-16", "1952-08-16", 
#          "1952-09-16", "1952-10-16", "1952-11-16", "1952-12-16", "1953-01-16", "1953-02-15", "1953-03-16", "1953-04-16", "1953-05-16", "1953-06-16", "1953-07-16", "1953-08-16", "1953-09-16", "1953-10-16", "1953-11-16", "1953-12-16", "1954-01-16", "1954-02-15", "1954-03-16", "1954-04-16", 
#          "1954-05-16", "1954-06-16", "1954-07-16", "1954-08-16", "1954-09-16", "1954-10-16", "1954-11-16", "1954-12-16", "1955-01-16", "1955-02-15", "1955-03-16", "1955-04-16", "1955-05-16", "1955-06-16", "1955-07-16", "1955-08-16", "1955-09-16", "1955-10-16", "1955-11-16", "1955-12-16", 
#          "1956-01-16", "1956-02-15", "1956-03-16", "1956-04-16", "1956-05-16", "1956-06-16", "1956-07-16", "1956-08-16", "1956-09-16", "1956-10-16", "1956-11-16", "1956-12-16", "1957-01-16", "1957-02-15", "1957-03-16", "1957-04-16", "1957-05-16", "1957-06-16", "1957-07-16", "1957-08-16", 
#          "1957-09-16", "1957-10-16", "1957-11-16", "1957-12-16", "1958-01-16", "1958-02-15", "1958-03-16", "1958-04-16", "1958-05-16", "1958-06-16", "1958-07-16", "1958-08-16", "1958-09-16", "1958-10-16", "1958-11-16", "1958-12-16", "1959-01-16", "1959-02-15", "1959-03-16", "1959-04-16", 
#          "1959-05-16", "1959-06-16", "1959-07-16", "1959-08-16", "1959-09-16", "1959-10-16", "1959-11-16", "1959-12-16", "1960-01-16", "1960-02-15", "1960-03-16", "1960-04-16", "1960-05-16", "1960-06-16", "1960-07-16", "1960-08-16", "1960-09-16", "1960-10-16", "1960-11-16", "1960-12-16", 
#          "1961-01-16", "1961-02-15", "1961-03-16", "1961-04-16", "1961-05-16", "1961-06-16", "1961-07-16", "1961-08-16", "1961-09-16", "1961-10-16", "1961-11-16", "1961-12-16", "1962-01-16", "1962-02-15", "1962-03-16", "1962-04-16", "1962-05-16", "1962-06-16", "1962-07-16", "1962-08-16", 
#          "1962-09-16", "1962-10-16", "1962-11-16", "1962-12-16", "1963-01-16", "1963-02-15", "1963-03-16", "1963-04-16", "1963-05-16", "1963-06-16", "1963-07-16", "1963-08-16", "1963-09-16", "1963-10-16", "1963-11-16", "1963-12-16", "1964-01-16", "1964-02-15", "1964-03-16", "1964-04-16", 
#          "1964-05-16", "1964-06-16", "1964-07-16", "1964-08-16", "1964-09-16", "1964-10-16", "1964-11-16", "1964-12-16", "1965-01-16", "1965-02-15", "1965-03-16", "1965-04-16", "1965-05-16", "1965-06-16", "1965-07-16", "1965-08-16", "1965-09-16", "1965-10-16", "1965-11-16", "1965-12-16", 
#          "1966-01-16", "1966-02-15", "1966-03-16", "1966-04-16", "1966-05-16", "1966-06-16", "1966-07-16", "1966-08-16", "1966-09-16", "1966-10-16", "1966-11-16", "1966-12-16", "1967-01-16", "1967-02-15", "1967-03-16", "1967-04-16", "1967-05-16", "1967-06-16", "1967-07-16", "1967-08-16", 
#          "1967-09-16", "1967-10-16", "1967-11-16", "1967-12-16", "1968-01-16", "1968-02-15", "1968-03-16", "1968-04-16", "1968-05-16", "1968-06-16", "1968-07-16", "1968-08-16", "1968-09-16", "1968-10-16", "1968-11-16", "1968-12-16", "1969-01-16", "1969-02-15", "1969-03-16", "1969-04-16", 
#          "1969-05-16", "1969-06-16", "1969-07-16", "1969-08-16", "1969-09-16", "1969-10-16", "1969-11-16", "1969-12-16", "1970-01-16", "1970-02-15", "1970-03-16", "1970-04-16", "1970-05-16", "1970-06-16", "1970-07-16", "1970-08-16", "1970-09-16", "1970-10-16", "1970-11-16", "1970-12-16", 
#          "1971-01-16", "1971-02-15", "1971-03-16", "1971-04-16", "1971-05-16", "1971-06-16", "1971-07-16", "1971-08-16", "1971-09-16", "1971-10-16", "1971-11-16", "1971-12-16", "1972-01-16", "1972-02-15", "1972-03-16", "1972-04-16", "1972-05-16", "1972-06-16", "1972-07-16", "1972-08-16", 
#          "1972-09-16", "1972-10-16", "1972-11-16", "1972-12-16", "1973-01-16", "1973-02-15", "1973-03-16", "1973-04-16", "1973-05-16", "1973-06-16", "1973-07-16", "1973-08-16", "1973-09-16", "1973-10-16", "1973-11-16", "1973-12-16", "1974-01-16", "1974-02-15", "1974-03-16", "1974-04-16", 
#          "1974-05-16", "1974-06-16", "1974-07-16", "1974-08-16", "1974-09-16", "1974-10-16", "1974-11-16", "1974-12-16", "1975-01-16", "1975-02-15", "1975-03-16", "1975-04-16", "1975-05-16", "1975-06-16", "1975-07-16", "1975-08-16", "1975-09-16", "1975-10-16", "1975-11-16", "1975-12-16", 
#          "1976-01-16", "1976-02-15", "1976-03-16", "1976-04-16", "1976-05-16", "1976-06-16", "1976-07-16", "1976-08-16", "1976-09-16", "1976-10-16", "1976-11-16", "1976-12-16", "1977-01-16", "1977-02-15", "1977-03-16", "1977-04-16", "1977-05-16", "1977-06-16", "1977-07-16", "1977-08-16", 
#          "1977-09-16", "1977-10-16", "1977-11-16", "1977-12-16", "1978-01-16", "1978-02-15", "1978-03-16", "1978-04-16", "1978-05-16", "1978-06-16", "1978-07-16", "1978-08-16", "1978-09-16", "1978-10-16", "1978-11-16", "1978-12-16", "1979-01-16", "1979-02-15", "1979-03-16", "1979-04-16", 
#          "1979-05-16", "1979-06-16", "1979-07-16", "1979-08-16", "1979-09-16", "1979-10-16", "1979-11-16", "1979-12-16", "1980-01-16", "1980-02-15", "1980-03-16", "1980-04-16", "1980-05-16", "1980-06-16", "1980-07-16", "1980-08-16", "1980-09-16", "1980-10-16", "1980-11-16", "1980-12-16", 
#          "1981-01-16", "1981-02-15", "1981-03-16", "1981-04-16", "1981-05-16", "1981-06-16", "1981-07-16", "1981-08-16", "1981-09-16", "1981-10-16", "1981-11-16", "1981-12-16", "1982-01-16", "1982-02-15", "1982-03-16", "1982-04-16", "1982-05-16", "1982-06-16", "1982-07-16", "1982-08-16", 
#          "1982-09-16", "1982-10-16", "1982-11-16", "1982-12-16", "1983-01-16", "1983-02-15", "1983-03-16", "1983-04-16", "1983-05-16", "1983-06-16", "1983-07-16", "1983-08-16", "1983-09-16", "1983-10-16", "1983-11-16", "1983-12-16", "1984-01-16", "1984-02-15", "1984-03-16", "1984-04-16", 
#          "1984-05-16", "1984-06-16", "1984-07-16", "1984-08-16", "1984-09-16", "1984-10-16", "1984-11-16", "1984-12-16", "1985-01-16", "1985-02-15", "1985-03-16", "1985-04-16", "1985-05-16", "1985-06-16", "1985-07-16", "1985-08-16", "1985-09-16", "1985-10-16", "1985-11-16", "1985-12-16", 
#          "1986-01-16", "1986-02-15", "1986-03-16", "1986-04-16", "1986-05-16", "1986-06-16", "1986-07-16", "1986-08-16", "1986-09-16", "1986-10-16", "1986-11-16", "1986-12-16", "1987-01-16", "1987-02-15", "1987-03-16", "1987-04-16", "1987-05-16", "1987-06-16", "1987-07-16", "1987-08-16", 
#          "1987-09-16", "1987-10-16", "1987-11-16", "1987-12-16", "1988-01-16", "1988-02-15", "1988-03-16", "1988-04-16", "1988-05-16", "1988-06-16", "1988-07-16", "1988-08-16", "1988-09-16", "1988-10-16", "1988-11-16", "1988-12-16", "1989-01-16", "1989-02-15", "1989-03-16", "1989-04-16", 
#          "1989-05-16", "1989-06-16", "1989-07-16", "1989-08-16", "1989-09-16", "1989-10-16", "1989-11-16", "1989-12-16", "1990-01-16", "1990-02-15", "1990-03-16", "1990-04-16", "1990-05-16", "1990-06-16", "1990-07-16", "1990-08-16", "1990-09-16", "1990-10-16", "1990-11-16", "1990-12-16", 
#          "1991-01-16", "1991-02-15", "1991-03-16", "1991-04-16", "1991-05-16", "1991-06-16", "1991-07-16", "1991-08-16", "1991-09-16", "1991-10-16", "1991-11-16", "1991-12-16", "1992-01-16", "1992-02-15", "1992-03-16", "1992-04-16", "1992-05-16", "1992-06-16", "1992-07-16", "1992-08-16", 
#          "1992-09-16", "1992-10-16", "1992-11-16", "1992-12-16", "1993-01-16", "1993-02-15", "1993-03-16", "1993-04-16", "1993-05-16", "1993-06-16", "1993-07-16", "1993-08-16", "1993-09-16", "1993-10-16", "1993-11-16", "1993-12-16", "1994-01-16", "1994-02-15", "1994-03-16", "1994-04-16", 
#          "1994-05-16", "1994-06-16", "1994-07-16", "1994-08-16", "1994-09-16", "1994-10-16", "1994-11-16", "1994-12-16", "1995-01-16", "1995-02-15", "1995-03-16", "1995-04-16", "1995-05-16", "1995-06-16", "1995-07-16", "1995-08-16", "1995-09-16", "1995-10-16", "1995-11-16", "1995-12-16", 
#          "1996-01-16", "1996-02-15", "1996-03-16", "1996-04-16", "1996-05-16", "1996-06-16", "1996-07-16", "1996-08-16", "1996-09-16", "1996-10-16", "1996-11-16", "1996-12-16", "1997-01-16", "1997-02-15", "1997-03-16", "1997-04-16", "1997-05-16", "1997-06-16", "1997-07-16", "1997-08-16", 
#          "1997-09-16", "1997-10-16", "1997-11-16", "1997-12-16", "1998-01-16", "1998-02-15", "1998-03-16", "1998-04-16", "1998-05-16", "1998-06-16", "1998-07-16", "1998-08-16", "1998-09-16", "1998-10-16", "1998-11-16", "1998-12-16", "1999-01-16", "1999-02-15", "1999-03-16", "1999-04-16", 
#          "1999-05-16", "1999-06-16", "1999-07-16", "1999-08-16", "1999-09-16", "1999-10-16", "1999-11-16", "1999-12-16", "2000-01-16", "2000-02-15", "2000-03-16", "2000-04-16", "2000-05-16", "2000-06-16", "2000-07-16", "2000-08-16", "2000-09-16", "2000-10-16", "2000-11-16", "2000-12-16", 
#          "2001-01-16", "2001-02-15", "2001-03-16", "2001-04-16", "2001-05-16", "2001-06-16", "2001-07-16", "2001-08-16", "2001-09-16", "2001-10-16", "2001-11-16", "2001-12-16", "2002-01-16", "2002-02-15", "2002-03-16", "2002-04-16", "2002-05-16", "2002-06-16", "2002-07-16", "2002-08-16", 
#          "2002-09-16", "2002-10-16", "2002-11-16", "2002-12-16", "2003-01-16", "2003-02-15", "2003-03-16", "2003-04-16", "2003-05-16", "2003-06-16", "2003-07-16", "2003-08-16", "2003-09-16", "2003-10-16", "2003-11-16", "2003-12-16", "2004-01-16", "2004-02-15", "2004-03-16", "2004-04-16", 
#          "2004-05-16", "2004-06-16", "2004-07-16", "2004-08-16", "2004-09-16", "2004-10-16", "2004-11-16", "2004-12-16", "2005-01-16", "2005-02-15", "2005-03-16", "2005-04-16", "2005-05-16", "2005-06-16", "2005-07-16", "2005-08-16", "2005-09-16", "2005-10-16", "2005-11-16", "2005-12-16", 
#          "2006-01-16", "2006-02-15", "2006-03-16", "2006-04-16", "2006-05-16", "2006-06-16", "2006-07-16", "2006-08-16", "2006-09-16", "2006-10-16", "2006-11-16", "2006-12-16", "2007-01-16", "2007-02-15", "2007-03-16", "2007-04-16", "2007-05-16", "2007-06-16", "2007-07-16", "2007-08-16", 
#          "2007-09-16", "2007-10-16", "2007-11-16", "2007-12-16", "2008-01-16", "2008-02-15", "2008-03-16", "2008-04-16", "2008-05-16", "2008-06-16", "2008-07-16", "2008-08-16", "2008-09-16", "2008-10-16", "2008-11-16", "2008-12-16", "2009-01-16", "2009-02-15", "2009-03-16", "2009-04-16", 
#          "2009-05-16", "2009-06-16", "2009-07-16", "2009-08-16", "2009-09-16", "2009-10-16", "2009-11-16", "2009-12-16", "2010-01-16", "2010-02-15", "2010-03-16", "2010-04-16", "2010-05-16", "2010-06-16", "2010-07-16", "2010-08-16", "2010-09-16", "2010-10-16", "2010-11-16", "2010-12-16", 
#          "2011-01-16", "2011-02-15", "2011-03-16", "2011-04-16", "2011-05-16", "2011-06-16", "2011-07-16", "2011-08-16", "2011-09-16", "2011-10-16", "2011-11-16", "2011-12-16", "2012-01-16", "2012-02-15", "2012-03-16", "2012-04-16", "2012-05-16", "2012-06-16", "2012-07-16", "2012-08-16", 
#          "2012-09-16", "2012-10-16", "2012-11-16", "2012-12-16", "2013-01-16", "2013-02-15", "2013-03-16", "2013-04-16", "2013-05-16", "2013-06-16", "2013-07-16", "2013-08-16", "2013-09-16", "2013-10-16", "2013-11-16", "2013-12-16", "2014-01-16", "2014-02-15", "2014-03-16", "2014-04-16", 
#          "2014-05-16", "2014-06-16", "2014-07-16", "2014-08-16", "2014-09-16", "2014-10-16", "2014-11-16", "2014-12-16", "2015-01-16", "2015-02-15", "2015-03-16", "2015-04-16", "2015-05-16", "2015-06-16", "2015-07-16", "2015-08-16", "2015-09-16", "2015-10-16", "2015-11-16", "2015-12-16", 
#          "2016-01-16", "2016-02-15", "2016-03-16", "2016-04-16", "2016-05-16", "2016-06-16", "2016-07-16", "2016-08-16", "2016-09-16", "2016-10-16", "2016-11-16", "2016-12-16", "2017-01-16", "2017-02-15", "2017-03-16", "2017-04-16", "2017-05-16", "2017-06-16", "2017-07-16", "2017-08-16", 
#          "2017-09-16", "2017-10-16", "2017-11-16", "2017-12-16", "2018-01-16", "2018-02-15", "2018-03-16", "2018-04-16", "2018-05-16", "2018-06-16", "2018-07-16", "2018-08-16", "2018-09-16", "2018-10-16", "2018-11-16", "2018-12-16", "2019-01-16", "2019-02-15", "2019-03-16", "2019-04-16", 
#          "2019-05-16", "2019-06-16", "2019-07-16", "2019-08-16", "2019-09-16", "2019-10-16", "2019-11-16", "2019-12-16", "2020-01-16", "2020-02-15", "2020-03-16", "2020-04-16", "2020-05-16", "2020-06-16", "2020-07-16", "2020-08-16", "2020-09-16", "2020-10-16", "2020-11-16", "2020-12-16", 
#          "2021-01-16", "2021-02-15", "2021-03-16", "2021-04-16", "2021-05-16", "2021-06-16", "2021-07-16", "2021-08-16", "2021-09-16", "2021-10-16", "2021-11-16", "2021-12-16", "2022-01-16", "2022-02-15", "2022-03-16", "2022-04-16", "2022-05-16", "2022-06-16", "2022-07-16", "2022-08-16", 
#          "2022-09-16", "2022-10-16", "2022-11-16", "2022-12-16", "2023-01-16", "2023-02-15", "2023-03-16", "2023-04-16", "2023-05-16", "2023-06-16", "2023-07-16", "2023-08-16", "2023-09-16", "2023-10-16", "2023-11-16", "2023-12-16"
#          ]
# print(ds['tmp'].attrs)
# ds = xr.open_dataset(temperature)
# ds = ds.rename(t='t2m')
# ds = ds.rename(valid_time='time')
# ds['t2m'].attrs['units'] = 'C'
# ds['t2m'].values - 273.15
# ds.to_netcdf('TH_temperature_day_1940-2024.nc')

# import xclim
# import xarray as xr
# import pint

# # Create a unit registry
# units = pint.UnitRegistry()
# units.define('degrees_Celsius = kelvin - 273.15')  # Define degrees Celsius

# temperature_values = xr.open_dataset('temperature.nc')
# precipitation_values = xr.open_dataset('precipitation.nc')

# # Set the units for the data variables
# temperature_values = temperature_values.sel(time=slice('2000-01-01', '2000-12-31'))['t2m']
# temperature_values.attrs['units'] = 'degrees_Celsius'
# temperature_values = temperature_values.pint.quantify()
# precipitation_values = precipitation_values.sel(time=slice('2000-01-01', '2000-12-31'))['tp']
# precipitation_values.attrs['units'] = 'mm'
# precipitation_values = precipitation_values.pint.quantify()

# cold_and_dry_days = xclim.indices.cold_and_dry_days(
#     temperature_values,
#     precipitation_values,
#     tas_per=25,
#     pr_per=10,
#     freq='YS'
# )

# tmx_temperature = xr.open_dataset(max_temperature)
# tmn_temperature = xr.open_dataset(min_temperature)
# tmp_temperature = xr.open_dataset(temperature)
# precipitation = xr.open_dataset(precipitation)

# tmx_temperature = xr.open_dataset(tmx)
# tmn_temperature = xr.open_dataset(tmn)
# precipitation = xr.open_dataset(precipitation)
# tmx_temperature['mx2t'] = tmx_temperature['mx2t'] - 273.15
# tmx_temperature['mx2t'].attrs['units'] = 'degC'
# tmx_temperature['mx2t'] = tmx_temperature['mx2t'].assign_coords(tmx_temperature.coords)


# tmp_temperature['t2m'] = tmp_temperature['t2m'] - 273.15
# tmp_temperature['t2m'].attrs['units'] = 'degC'
# tmp_temperature['t2m'] = tmp_temperature['t2m'].assign_coords(tmp_temperature.coords)

# tmn_temperature['mn2t'] = tmn_temperature['mn2t'] - 273.15
# tmn_temperature['mn2t'].attrs['units'] = 'degC'
# tmn_temperature['mn2t'] = tmn_temperature['mn2t'].assign_coords(tmx_temperature.coords)

# precipitation = precipitation.rename(name_dict={'longitude': 'lon', 'latitude': 'lat'})
# precipitation['tp'] = precipitation['tp'] * 1000
# precipitation['tp'].attrs['units'] = 'mm/day'
# # precipitation['tp'].attrs['units'] = 'mm'
# precipitation['tp'] = precipitation['tp'].assign_coords(precipitation.coords)

# dataset = xr.open_dataset("precipitation.nc")
# tp_data = dataset.variables['tp'][:]
# time = dataset.variables['time'][:]
# lat = dataset.variables['lat'][:]
# lon = dataset.variables['lon'][:]

# new_dataset = nc.Dataset("corrected_precipitation.nc", "w", format="NETCDF4")
# new_dataset.createDimension('time', len(time))
# new_dataset.createDimension('lat', len(lat))
# new_dataset.createDimension('lon', len(lon))

# time_var = new_dataset.createVariable('time', np.float64, ('time',))
# lat_var = new_dataset.createVariable('lat', np.float32, ('lat',))
# lon_var = new_dataset.createVariable('lon', np.float32, ('lon',))
# tp_var = new_dataset.createVariable('tp', np.float32, ('time', 'lat', 'lon'))

# time_var[:] = time
# lat_var[:] = lat
# lon_var[:] = lon
# tp_var[:, :, :] = tp_data
# print(new_dataset)

# start_date = '1960-01-01'
# end_date = '1962-12-31'

# tmxtemperature = tmx_temperature.sel(longitude=slice(96, 106), latitude=slice(4, 21), time=slice(start_date, end_date))['mx2t']
# tmntemperature = tmn_temperature.sel(longitude=slice(96, 106), latitude=slice(4, 21), time=slice(start_date, end_date))['mn2t']
# tmptemperature = tmp_temperature.sel(longitude=slice(96, 106), latitude=slice(4, 21), time=slice(start_date, end_date))['t2m']
# precipitation_values = precipitation.sel(longitude=slice(96, 106), latitude=slice(4, 21), time=slice(start_date, end_date))['tp'] 

# tmxtemperature = tmx_temperature.sel(time=slice(start_date, end_date))['mx2t']
# tmntemperature = tmn_temperature.sel(time=slice(start_date, end_date))['mn2t']
# tmptemperature = tmp_temperature.sel(time=slice(start_date, end_date))['t2m']
# precipitation_values = precipitation.sel(time=slice(start_date, end_date))['tp'] 

# tmxtemperature = tmx_temperature.sel(lon=slice(96, 106), lat=slice(4, 21),time=slice(start_date, end_date))['tmx']
# tmntemperature = tmn_temperature.sel(lon=slice(96, 106), lat=slice(4, 21),time=slice(start_date, end_date))['tmn']
# precipitation_values = precipitation.sel(lon=slice(96, 106), lat=slice(4, 21), time=slice(start_date, end_date))['pre'] 

# cdd = xclim.indices.dry_spell_max_length(precipitation_values, freq='YS') # Maximum length of dry spell: maximum number of consecutive days with RR < 1mm
# print(cdd)
# cdd.plot()
# plt.title('CDD')
# print('cdd','-'*100)
# plt.show()
# x = precipitation.lon
# y = precipitation.lat

# cwd = xclim.indices.wet_spell_max_length(precipitation_values, freq='M') # Maximum length of wet spell: maximum number of consecutive days with RR ≥ 1mm
# # cwd = xclim.atmos.wet_spell_max_length(precipitation_values, freq='YS') # Maximum length of wet spell: maximum number of consecutive days with RR ≥ 1mm
# print(cwd)
# cwd_2d = cwd.mean(dim='time')
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# mesh = ax.pcolormesh(cwd['lon'], cwd['lat'], cwd_2d, transform=ccrs.PlateCarree(), cmap='viridis', shading='auto')
# cwd.plot(ax=ax, transform=ccrs.PlateCarree())
# ax.set_extent([96, 106, 4, 21], crs=ccrs.PlateCarree())
# shapefile.geometry.boundary.plot(ax=ax, color='black', linewidth=0.5)
# fig.colorbar(mesh, ax=ax, orientation='vertical', label='CWD')
# plt.title('CWD')
# print('cwd','-'*100)
# plt.show()

# def calculate_pet(temperature, lat, days_in_month):
#     """
#     Calculate Potential Evapotranspiration (PET) using the Thornthwaite equation.
    
#     Parameters:
#         temperature (array): Average monthly temperature in degrees Celsius.
#         lat (float): Latitude in degrees.
#         days_in_month (array): Number of days in each month.
        
#     Returns:
#         array: PET values for each month.
#     """
#     # Heat index (I)
#     I = np.sum((temperature / 5) ** 1.514)
    
#     # Empirical parameter (a)
#     a = (6.75e-7 * I ** 3) - (7.71e-5 * I ** 2) + (1.79e-2 * I) + 0.49239
    
#     # Calculate monthly PET
#     pet = 16 * (10 * temperature / I) ** a
    
#     # Correct for the day length factor
#     J = np.arange(1, 13)
#     dr = 1 + 0.033 * np.cos(2 * np.pi * J / 12)
#     delta = 0.409 * np.sin(2 * np.pi * J / 12 - 1.39)
#     ws = np.arccos(-np.tan(np.radians(lat)) * np.tan(delta))
#     N = 24 / np.pi * ws
#     pet_corrected = pet * days_in_month / (N * days_in_month.mean())
    
#     return pet_corrected

# # Example usage
# temperature = np.array([15, 16, 18, 20, 22, 24, 26, 25, 23, 20, 18, 16])  # Monthly mean temperature in Celsius
# lat = 13.75  # Latitude for Bangkok
# days_in_month = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])  # Days in each month

# pet = calculate_pet(temperature, lat, days_in_month)
# print("PET:", pet)

# def calculate_water_balance(precipitation, pet):
#     """
#     Calculate the water balance.
    
#     Parameters:
#         precipitation (array): Monthly precipitation in mm.
#         pet (array): Monthly potential evapotranspiration in mm.
    
#     Returns:
#         array: Monthly water balance values.
#     """
#     return precipitation - pet

# # Example usage
# precipitation = np.array([50, 40, 60, 80, 100, 150, 200, 180, 140, 90, 60, 50])  # Monthly precipitation in mm
# wb = calculate_water_balance(precipitation, pet)
# print("Water Balance:", wb)

# from scipy.stats import genextreme

# def standardize_series(series):
#     """
#     Standardize the series using the Generalized Extreme Value (GEV) distribution.
    
#     Parameters:
#         series (array): Accumulated water balance values.
    
#     Returns:
#         array: Standardized series.
#     """
#     params = genextreme.fit(series)
#     standardized_series = genextreme.cdf(series, *params)
#     standardized_series = (standardized_series - np.mean(standardized_series)) / np.std(standardized_series)
#     return standardized_series

# Example usage
# spei = standardize_series(accumulated_wb)
# print("SPEI:", spei)

# cdd = xclim.indices.dry_spell_max_length(precipitation_values) # Maximum length of dry spell: maximum number of consecutive days with RR < 1mm
# print(cdd)
# cdd.plot()
# plt.title('CDD')
# print('cdd','-'*100)
# plt.show()

# # tasmin = xr.open_dataset(min_temperature).isel(longitude=slice(96, 97), latitude=slice(4, 5))
# # tasmin = tasmin.dropna(dim='time', how='all')
# # tn10 = percentile_doy(tasmin, per=10).sel(percentiles=10)
# # csdi = xclim.indices.cold_spell_duration_index(tasmin, tn10)
# # print(csdi) 
# # print('-'*100)

# tn10 = percentile_doy(tmntemperature, per=10).sel(percentiles=10)
# csdi = xclim.indices.cold_spell_duration_index(tmntemperature, tn10) # Cold spell duration index: annual count of days with at least 6 consecutive days when TN < 10th percentile
# print(csdi)
# csdi.plot()
# plt.title('CSDI')
# print('csdi','-'*100)
# plt.show()

# cwd = xclim.indices.wet_spell_max_length(precipitation_values) # Maximum length of wet spell: maximum number of consecutive days with RR ≥ 1mm
# print(cwd)
# cwd.plot()
# plt.title('CWD')
# print('cwd','-'*100)
# plt.show()

# dtr = xclim.indices.daily_temperature_range(tmntemperature, tmxtemperature) # Daily temperature range
# print(dtr)
# dtr.plot()
# plt.title('DTR')
# print('dtr','-'*100)
# plt.show()

# fd = xclim.indices.frost_days(tmntemperature) # Number of frost days
# print(fd)
# fd.plot()
# plt.title('FD')
# print('fd','-'*100)
# plt.show()

# gsl = xclim.indices.growing_season_length(tmptemperature, thresh='25.0 degC')# Growing season length
# print(gsl)
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# gsl.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis')
# plt.title('GSL')
# print('gsl','-'*100)
# plt.show()

# # id = xclim.indices # Number of icing days
# # print('-'*100)

# prcptot = xclim.indices.prcptot(precipitation_values) # Annual total precipitation on wet days
# print(prcptot)
# plt.title('PRCPTOT')
# prcptot.plot()
# print('prcptot','-'*100)
# plt.show()

# # precipitation_values = xr.DataArray(precipitation_values)
# r10mm = xclim.indices.wetdays(precipitation_values, thresh='10.0 mm/day')# Annual count of days when PRCP ≥ 10mm
# print(r10mm)
# r10mm_2d = r10mm.mean(dim='time')
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# mesh = ax.pcolormesh(r10mm['longitude'], r10mm['latitude'], r10mm_2d, transform=ccrs.PlateCarree(), cmap='viridis', shading='auto')
# fig.colorbar(mesh, ax=ax, orientation='vertical', label='R10MM')
# plt.title('R10MM')
# # r10mm.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis')
# plt.show()

# r20mm = xclim.indices.wetdays(precipitation_values, thresh='20.0 mm/day')# Annual count of days when PRCP ≥ 20mm
# print(r20mm)
# r20mm_2d = r20mm.mean(dim='time')
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# mesh = ax.pcolormesh(r20mm['longitude'], r20mm['latitude'], r20mm_2d,transform=ccrs.PlateCarree(), cmap='viridis', shading='auto')
# fig.colorbar(mesh, ax=ax, orientation='vertical', label='R10MM')
# plt.title('R20MM')
# plt.show()
                                                       
# r95 = percentile_doy(precipitation_values, per=95).sel(percentiles=95)
# r95p = xclim.indices.days_over_precip_thresh(precipitation_values, r95) # Annual total PRCP when RR > 95th percentile
# print(r95p)
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# plt.title('R95P')
# r95p.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis')
# print('r95p','-'*100)
# plt.show()


# r99 = percentile_doy(precipitation_values, per=99).sel(percentiles=99)
# r99p = xclim.indices.days_over_precip_thresh(precipitation_values,r99) # Annual total PRCP when RR > 99th percentile
# print(r99p)
# print('r99p','-'*100)
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# plt.title('R99P')
# r99p.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis')
# plt.show()

# rx1day = xclim.indices.max_1day_precipitation_amount(precipitation_values) # Maximum 1-day precipitation
# rx1day.plot()
# plt.title('RX1DAY')
# print(rx1day)
# print('rx1day','-'*100)
# plt.show()

# rx5day = xclim.indices.max_n_day_precipitation_amount(precipitation_values,window=5)# Maximum consecutive 5-day precipitation
# rx5day.plot()
# plt.title('RX5DAY')
# print(rx5day)
# print('rx5day','-'*100)
# plt.show()

# sdii = xclim.indices.daily_pr_intensity(precipitation_values)# Simple precipitation intensity index
# sdii.plot()
# plt.title('SDII')
# print(sdii)
# print('sdii','-'*100)
# plt.show()

# su = xclim.indices.tx_days_above(tmxtemperature) # Number of summer days
# su.plot()
# plt.title('SU')
# print(su)
# print('su','-'*100)
# plt.show()

# txm = xclim.indices.tx_mean(tmxtemperature) # Mean TX
# txm.plot()
# plt.title('TXM')
# print(txm)
# print('txm','-'*100)
# plt.show()

# tnm = xclim.indices.tn_mean(tmntemperature) # Mean TN
# tnm.plot()
# plt.title('TNM')
# print(tnm)
# print('tnm','-'*100)
# plt.show()

# tn10p = xclim.indices.tn10p(tmntemperature, tn10) # Percentage of days when TN < 10th percentile
# tn10p.plot()
# plt.title('TN10P')
# print(tn10p)
# print('tn10p','-'*100)
# plt.show()

# tn90 = percentile_doy(tmntemperature, per=90).sel(percentiles=90)
# tn90p = xclim.indices.tn90p(tmntemperature, tn90) # Percentage of days when TN > 90th percentile
# tn90p.plot()
# plt.title('TN90P')
# print(tn90p)
# print('tn90p','-'*100)
# plt.show()

# tnn = xclim.indices.tn_min(tmntemperature) # Minimum value of daily minimum temperature
# tnn.plot()
# plt.title('TNN')
# print(tnn)
# print('tnn','-'*100)
# plt.show()

# txn = xclim.indices.tx_max(tmxtemperature) # Minimum value of daily maximum temperature
# txn.plot()
# plt.title('TXN')
# print(txn)
# print('txn','-'*100)
# plt.show()

# tr = xclim.indices.tn_days_above(tmntemperature) # Number of tropical nights
# tr.plot()
# plt.title('TR')
# print(tr)
# print('tr','-'*100)
# plt.show()

# tx10 = percentile_doy(tmxtemperature, per=10).sel(percentiles=10)
# tx10p = xclim.indices.tx10p(tmxtemperature, tx10)# Percentage of days when TX < 10th percentile
# tx10p.plot()
# plt.title('TX10p')
# print(tx10p)
# print('tx10p','-'*100)
# plt.show()

# tx90 = percentile_doy(tmxtemperature, per=90).sel(percentiles=90)
# tx90p = xclim.indices.tx90p(tmxtemperature, tx90)# Percentage of days when TX > 90th percentile
# tx90p.plot()
# plt.title('TX90p')
# print(tx90p)
# print('tx90p','-'*100)
# plt.show()

# tnx = xclim.indices.tn_max(tmntemperature) # Maximum value of daily minimum temperature
# tnx.plot()
# plt.title('TNX')
# print(tnx)
# print('tnx','-'*100)
# plt.show()

# txx = xclim.indices.tx_max(tmxtemperature) # Maximum value of daily maximum temperature
# txx.plot()
# plt.title('TXX')
# print(txx)
# print('txx','-'*100)
# plt.show()

# wsdi = xclim.indices.warm_spell_duration_index(tmxtemperature, tx90) # Warm spell duration index: annual count of days with at least 6 consecutive days when TX > 90th percentile
# wsdi.plot()
# plt.title('WSDI')
# print(wsdi)
# print('wsdi','-'*100)
# plt.show()

# if precipitation_values.isnull().sum() > 0:
#     print("Warning: Dataset contains NaN values. Filling NaNs with zero.")
#     precipitation_values = precipitation_values.fillna(0)

# if precipitation_values.size == 0:
#     raise ValueError("Selected region contains no data.")

# cal_start, cal_end = "1990-05-01", "1990-09-30"
# tmxtemperature_monthly = tmxtemperature.resample(time='M').sum()
# tmptemperature_monthly = tmptemperature.resample(time='M').sum()
# tmntemperature_monthly = tmntemperature.resample(time='M').sum()

# precipitation_filled = precipitation_values.interpolate_na(dim='time', method='linear')
# precipitation_monthly = precipitation_filled.resample(time='M', skipna=True).sum()
# # print(precipitation_monthly['time'])
# # fit_kwargs = {'floc': 0}
# spi = xclim.indices.standardized_precipitation_index(precipitation_values, freq="M", window=36)
# # spi = xclim.indices.standardized_precipitation_index(precipitation_monthly, freq="M", window=3, cal_start=cal_start, cal_end=cal_end, method="APP", dist="gamma", fitkwargs=fit_kwargs)
# spi = spi.compute()
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# print(spi)
# plt.title('SPI')
# print('spi','-'*100)
# spi.plot(ax=ax, transform=ccrs.PlateCarree())
# plt.show()

# xclim.icclim.TG()
# if spi.isnull().all():
#     raise ValueError("SPI calculation resulted in NaN values. Please check the data and parameters.")

# data = climate_V2.Climate(precipitation_monthly)
# spi = data.calculate_spi(thresh=3, dimension='time', precip_var='tp')
# spi[9].plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
# plt.show()
# wb = xclim.indices.water_budget(pr=precipitation_values, tasmin=tmntemperature, tasmax=tmxtemperature, tas=tmptemperature, method="MB05")
# wb = xclim.indices.water_budget(pr=precipitation_values, tasmin=tmntemperature, tasmax=tmxtemperature, tas=tmptemperature, lat='13.75')
# param = xclim.indices.stats.standardized_index_fit_params(da=precipitation_monthly, freq="M", window=1, dist="gamma", method="ML")
# wb = xclim.indices.water_budget(pr=precipitation_values, tasmin=tmntemperature, tasmax=tmxtemperature, tas=tmptemperature)

# wb = xclim.indices.water_budget(pr=precipitation_values, tas=tmptemperature)
# print(wb.values)
# spei = xclim.indices.standardized_precipitation_evapotranspiration_index(wb)

# data = pd.read_csv('precipitation.csv', usecols=[1])

# data = data.set_index(pd.date_range('1901', '2024', freq='M'))
# spi = xclim.indices.standardized_precipitation_index(data, freq="M", window=3)
# print(spi)




# temperature_values = temperature_values.sel(time=slice('2000-01-01', '2000-12-31'))['t2m'].metpy.quantify() * units.degC
# precipitation_values = precipitation_values.sel(time=slice('2000-01-01', '2000-12-31'))['tp'].metpy.quantify() * units.mm
# print(temperature_values['t2m'].attrs['units'])
# print(precipitation_values['tp'].attrs['units'])
# temperature_values = temperature_values['t2m']
# precipitation_values = precipitation_values['tp']
# t_monthly = temperature_values.resample(time='M').reduce(np.percentile, q=25, dim='time')
# p_monthly = precipitation_values.resample(time='M').reduce(np.percentile, q=25, dim='time')
# temp = ds.sel(time=slice('2000-01-01', '2000-12-31')).t2m
# ds = ds.sel(time=slice('2000-01-01', '2000-12-31'))
# print(temperature_values.values)
# xclim.indices.cold_and_dry_days(temperature_values.values, precipitation_values.values, freq='YS')
# temperature_values.attrs['units'] = 'K'
# precipitation_values.attrs['units'] = 'mm/day'

# cold_and_dry_days = xclim.indices.cold_and_dry_days(temperature_values, precipitation_values, tas_per=25, pr_per=10, freq='YS')
# print(cold_and_dry_days)

# ds = xr.open_dataset(temperature)
# temp = ds.t2m
# tasmax_per = percentile_doy(temp, per=10).sel(percentiles=10)
# cold_days = xclim.indices.tx10p(temp, tasmax_per)
# print(cold_days)
# cold_days.plot()
# plt.show()

# climate_index = ClimateIndex(tmp)
# climate_index = ClimateIndex(max_temperature)
# climate_index = ClimateIndex(temperature)
# # climate_index.pre_process(time_range=('2000-01-01', '2000-12-31'), resample_freq='D', fill_missing='interpolate')
# climate_index.pre_process(time_range=('1960-01-01', '1991-12-31'), resample_freq='M', fill_missing='interpolate')
# # tx10p_index = climate_index.calculate_tx10p(temp_var='mx2t')
# tx10p_index = climate_index.calculate_tx10p(temp_var='t2m')
# print(tx10p_index['tx10p'].values)


# temp = xr.open_dataset(temperature)
# max_temp = xr.open_dataset(max_temperature)
# min_temp = xr.open_dataset(min_temperature)

# print(temp['t'])
# xclim.indices.daily_temperature_range(min_temp, max_temp, freq="YS", op="mean")