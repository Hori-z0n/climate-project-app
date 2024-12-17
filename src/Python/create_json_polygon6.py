import xarray as xr
import geopandas as gpd
import json
from tqdm import tqdm, trange
import warnings

warnings.filterwarnings('ignore')

dtr = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.dtr.dat.nc')
pre = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.pre.dat.nc')
tmn = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmn.dat.nc')
tmp = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmp.dat.nc')
tmx = xr.open_dataset('C:/Users/konla/OneDrive/Desktop/Weather/cru_ts4.08.1901.2023.tmx.dat.nc')

start_year = 1901
stop_year = 1901
start_month = 1
stop_month = 12

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


for year in tqdm(range(start_year, stop_year+1), desc="Start Create Value Year...", ascii=False, ncols=75, colour='green'):
    print('\n')
    value = []
    path = f'C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/Year-Dataset/data_{year}.json'
    data = gpd.read_file(path)
    txx_year_value = []
    tnn_year_value = []
    features = []

    for province in provinces:
        max_value = {'name':str(), 'temperature':0.0}
        min_value = {'name':str(), 'temperature':100.0}
        max_value['temperature'] = max(data[data['name'] == province]['tmx'])
        max_value['name'] = province
        txx_year_value.append(max_value)
        min_value['temperature'] = min(data[data['name'] == province]['tmn'])
        min_value['name'] = province
        tnn_year_value.append(min_value)
    print("\nGeoJSON data Climate Extreme Index create successfully.")

    
    with open(path) as f:
        data = json.load(f)

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    count = 0
    for month in tqdm(range(start_month, stop_month+1), desc="Start Create GeoJson...", ascii=False, ncols=75, colour='yellow'):
        _max = None
        _min = None
        for i, province in enumerate(provinces):
            for j, province in enumerate(provinces):
                if txx_year_value[j]['name'] == data['features'][i]['properties']['name']:
                    _max = txx_year_value[j]
                else:
                    continue

                if tnn_year_value[j]['name'] == data['features'][i]['properties']['name']:
                    _min = tnn_year_value[j]
                else:
                    continue

            features = {
                "type": "Feature",
                "geometry": {
                    "type":data['features'][count]['geometry']['type'],
                    "coordinates": data['features'][count]['geometry']['coordinates']
                },  
                "properties": {
                'name': data['features'][count]['properties']['name'],
                'region': data['features'][count]['properties']['region'],
                'month': month,
                'pre': data['features'][count]['properties']['pre'],
                'dtr': data['features'][count]['properties']['dtr'], 
                'tmn': data['features'][count]['properties']['tmn'], 
                'tmp': data['features'][count]['properties']['tmp'], 
                'tmx': data['features'][count]['properties']['tmx'],
                'txx': _max['temperature'],
                'tnn': _min['temperature']
                }
            }
            geojson_data['features'].append(features)
            count += 1

    output_geojson_path = f'./src/Geo-data/Year-Dataset/data_{year}_V4.json'
    with open(output_geojson_path, 'w', encoding='utf-8') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

print("\nGeoJSON file polygon saved complete.")

