import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import time
import json
import warnings
warnings.filterwarnings('ignore')

start = time.perf_counter()

# thai_shape = gpd.read_file("./shapefile/gadm41_THA_1.shp")
data = gpd.read_file('./Geo-data/nc_to_json_2000_1.json')
shapefile = gpd.read_file('./Geo-data/thailand-Geo.json')

# coord = shapefile[shapefile['NAME_1'] == 'Yasothon']
coord = shapefile[shapefile['NAME_1'] == np.array(shapefile['NAME_1'])[-1]]
# print(coord)

province=['Amnat Charoen', 'Ang Thong', 'Bangkok Metropolis', 'Bueng Kan', 'Buri Ram', 'Chachoengsao', 'Chai Nat',
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

total = 0
index = []
temperature = []
percentage = []
geojson_polygons = []
dictionary = {"zone": index, "temperature":temperature, "percentage":percentage}

grid_in = data[data.geometry.intersects(coord.geometry.unary_union)]
with open('./Geo-data/thailand-Geo.json', mode='r', encoding='utf-8') as f:
    data = json.load(f)   
for row, coordinate in enumerate(province):
    coord = shapefile[shapefile['NAME_1'] == coordinate]
    coord_area = coord.geometry.unary_union.area
    for idx, grid in grid_in.iterrows():
        intersection_area = grid.geometry.intersection(coord.geometry.unary_union).area

        intersection_percentage_of_korat = (intersection_area / coord_area) * 100

        temperature_value = grid['temperature']
        index.append(idx)
        temperature.append(grid.temperature)
        percentage.append(intersection_percentage_of_korat)

        x, y = grid.geometry.centroid.x, grid.geometry.centroid.y
        total = total + intersection_percentage_of_korat

    dictionary = {"zone": index, "temperature":temperature, "percentage":percentage}

    inx = 0
    for zone in range(len(dictionary['zone'])):
        if dictionary['percentage'][zone] > dictionary['percentage'][inx]:
            inx = zone
        else:
            inx = inx

    a = np.array(dictionary['percentage'])
    b = np.array(dictionary['temperature'])

    temp_value = []
    for i in range(len(dictionary['zone'])):
        temp_value.append(a[i] * b[i])
    result = np.sum(temp_value)/np.sum(dictionary['percentage'])

    geojson_polygons.append({
        'type': 'Feature',
        'geometry': {
        'type': data['features'][row]['geometry']['type'],
            'coordinates': data['features'][row]['geometry']['coordinates']
        },
        'properties': {
            'temperature': float(result),
            'name' : shapefile['NAME_1'][row]
            }
        })
    
geojson_data = {
    'type': 'FeatureCollection',
    'features': geojson_polygons
}
with open(f"./Geo-data/NEW_TEST.json", "w") as f:
    json.dump(geojson_data, f, indent=4)

elapsed = time.perf_counter() - start
print(f"{__file__} executed in {elapsed} seconds.")

