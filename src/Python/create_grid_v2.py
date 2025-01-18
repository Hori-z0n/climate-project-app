import climate_V_thailand as climate
import numpy as np
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')



# cell 2: specifiying the parameter for creating the source shapefile
# name of the sample nc file (give only one if there are separaete file for each year or month)
name_of_nc = 'C:/Netcdf/TH_pr_ERA5_day.1960-2022.nc'
# sample varibale from nc file (similar to all the dimensions for all the varibales with intend to read)
name_of_variable = 'tp'
# name of varibale in nc file (and not dimension) that holed the longituge values
name_of_lon_var = 'longitude'
# name of varibale in nc file (and not dimension) that holds the latitiute values
name_of_lat_var = 'latitude'
# bounding box the trim the created shepefile
# it should be in form of np.array([min_lat,max_lat,min_lon,max_lon]) 
# or should be give False if there is not box
box_values =  np.array([4,22,95,107])# or False;
# if the nc file lon is 0 to 360 and want to transfor to -180 to 180
# in the case the box_value should be in either of east or west hemisphere

correct_360 = False
# name of the shapefile that is created and saved
name_of_shp = './src/shapefile/ThailandGrid2.shp'
# creating the shapefile and preparing the 2D lat/lon field based on shapefile for indexing
lat_2D, lon_2D = climate.NetCDF_SHP_lat_lon(name_of_nc, name_of_variable, name_of_lat_var, name_of_lon_var, name_of_shp, box_values, correct_360)

print(f"Create {name_of_shp} Finish")