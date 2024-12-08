import xarray as xr

import geopandas as gpd
import numpy as np
import json
from province import province_coord 
import warnings
warnings.filterwarnings('ignore')
# ds = xr.open_dataset('D:/Program/PROJECT/Python/cru_ts4.08.1901.2023.tmp.dat.nc')
data = gpd.read_file('C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/province_all_1901.json')

json_data = []
features = {}
geojson = {}
row = 1
count = 0
for region in province_coord():
    for province in region:
        name, geometry, region_name = province
        for i in range(min(data['month'].values) ,max(data['month'].values)+1):
        # for i in range(1,3):
            # print('name'+ ' ' + str(data[data['month'] == i][data['name'] == name]['name'].values[0]))
            # print('region'+ ' ' + str(region_name))
            # print('month'+ ' ' + str(i))
            # print('temperature'+ ' ' +str(data[data['month'] == i][data['name'] == name]['temperature'].values[0]))
            features = {
                'name': data[data['month'] == i][data['name'] == name]['name'].values[0],
                'region':region_name,
                'month':i,
                'temperature':data[data['month'] == i][data['name'] == name]['temperature'].values[0]
            }
            # print(str(row) + " " + str(count) + " region: " + str(region_name) + " month: " + str(i) + " name: " + str(data[data['month'] == i][data['name'] == name]['name'].values[0])+" temperature: "+ str(data[data['month'] == i][data['name'] == name]['temperature'].values[0]))
            json_data.append(features)
            row += 1
        count += 1
    
    # geojson_data = {
    #     "name":data[data['month'] == i][data['name'] == name]['name'].values[0],
    #     "features":json_data
    # }
    # geojson.update(geojson_data)
    
geojson_data = {
    "features":json_data
}
# print(row)
# print(geojson)
# print(features)
# json_string = json.dumps(geojson_data, indent=4)
output_file = f"C:/Users/konla/OneDrive/Desktop/Final_test/src/json_series/test2.json"
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(geojson_data, outfile, ensure_ascii=False, indent=4)
    # json.dump(geojson, outfile, ensure_ascii=False, indent=4)
    # json.dump(json_string, outfile, ensure_ascii=False)
