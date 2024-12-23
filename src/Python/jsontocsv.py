import json
import pandas as pd
import geopandas as gpd
from tqdm import tqdm

start_year = 1901
stop_year = 1902
start_month = 1
stop_month = 13
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

features = []
# txx_year_value = []
# tnn_year_value = []
# for year in tqdm(range(start_year, stop_year)):
for year in range(start_year, stop_year):
    count = 0
    path = f'C:/Users/konla/OneDrive/Desktop/climate-project-app/src/Geo-data/Year-Dataset/data_{year}_V5.json'

    with open(path) as f:
        data = json.load(f)

    # data = gpd.read_file(path)
    # print(data)
    count = 0
    print('\n')
    for month in range(start_month, stop_month):
        for i in range(0, 77):
            # print(data['features'][count]['properties']['name'] == "Chiang Rai")
            
            if (data['features'][count]['properties']['name'] == "Chiang Rai"):
                print(data['features'][count]['properties'])
                # print(' pre: ', data['features'][count]['properties']['pre'], ' tmn: ', data['features'][count]['properties']['tmn'],' tmx: ', data['features'][count]['properties']['tmx'])
            count+=1
    
    # for ds in data.values:
    #     print(ds[])