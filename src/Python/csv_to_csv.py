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

data = pd.read_csv('C:/climpact-master/csv/3881824.csv')

dataframe = []
for i, dates in enumerate(data['DATE'].values):
    date = dates.split('-')
    year = date[0]
    month = date[1]
    day = date[2]
    pre = data['PRCP'][i]
    tmax = data['TMAX'][i]
    tmin = data['TMIN'][i]
    if pd.isnull(pre) == True:
        pre = -99.9
        
    if pd.isnull(tmax) == True:
        tmax = -99.

    if pd.isnull(tmin) == True:
        tmin = -99.9

    row = [year, month, day, pre, tmax, tmin]
    dataframe.append(row)

df = pd.DataFrame(data=dataframe)
df.to_csv('text.csv', index=False)