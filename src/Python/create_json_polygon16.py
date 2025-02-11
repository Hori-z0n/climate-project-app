import xarray as xr
import pandas as pd
import json
from tqdm import tqdm
import xclim as xc
from xclim.core.calendar import percentile_doy

ds_tmax = xr.open_dataset("C:/Netcdf/TH_tmax_ERA5_day.1960-2022.nc")
ds_tmin = xr.open_dataset("C:/Netcdf/TH_tmin_ERA5_day.1960-2022.nc")
ds_pr = xr.open_dataset("C:/Netcdf/TH_precipitation_day_1960-2022.nc")

ds_tmin['mn2t'] = ds_tmin['mn2t'] - 273.15
ds_tmin['mn2t'].attrs['units'] = 'degC'  # องศาเซลเซียส
ds_tmin['mn2t'] = ds_tmin['mn2t'].assign_coords(ds_tmin.coords)

ds_tmax['mx2t'] = ds_tmax['mx2t'] - 273.15
ds_tmax['mx2t'].attrs['units'] = 'degC'  # องศาเซลเซียส
ds_tmax['mx2t'] = ds_tmax['mx2t'].assign_coords(ds_tmax.coords)

ds_pr['tp'] = ds_pr['tp'] * 1000  # m -> mm/day
ds_pr['tp'].attrs['units'] = 'mm/day'  # มิลลิเมตรต่อวัน
ds_pr['tp'] = ds_pr['tp'].assign_coords(ds_pr.coords)

def create_grid_polygon(lon_center, lat_center, lon_step, lat_step):
    return [
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างซ้าย
        [float(lon_center + lon_step / 2), float(lat_center - lat_step / 2)],  # มุมล่างขวา
        [float(lon_center + lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนขวา
        [float(lon_center - lon_step / 2), float(lat_center + lat_step / 2)],  # มุมบนซ้าย
        [float(lon_center - lon_step / 2), float(lat_center - lat_step / 2)]   # ปิดกรอบ
    ]

lon_step = float(ds_tmax['longitude'][1] - ds_tmax['longitude'][0])
lat_step = float(ds_tmax['latitude'][1] - ds_tmax['latitude'][0])

for year in range(1960, 1961):
    print(f"Processing data for the year {year}...")
    features = []

    ds_tmin_year = ds_tmin.sel(time=slice(f'{year}', f'{year}'))
    ds_tmax_year = ds_tmax.sel(time=slice(f'{year}', f'{year}'))
    ds_pr_year = ds_pr.sel(time=slice(f'{year}', f'{year}'))

    total_grids = len(ds_tmin_year.latitude) * len(ds_tmin_year.longitude)
    with tqdm(total=total_grids, desc=f"Year {year}") as pbar:
        for lat in ds_tmin_year.latitude:
            for lon in ds_tmin_year.longitude:
                grid_data_tmin = ds_tmin_year['mn2t'].sel(latitude=lat, longitude=lon, method='nearest')
                grid_data_tmax = ds_tmax_year['mx2t'].sel(latitude=lat, longitude=lon, method='nearest')
                grid_data_pr = ds_pr_year['tp'].sel(latitude=lat, longitude=lon, method='nearest')
                tn10 = percentile_doy(grid_data_tmin, per=10).sel(percentiles=10)
                tn90 = percentile_doy(grid_data_tmin, per=90).sel(percentiles=90)
                tx10 = percentile_doy(grid_data_tmax, per=10).sel(percentiles=10)
                tx90 = percentile_doy(grid_data_tmax, per=90).sel(percentiles=90)

                r95 = percentile_doy(grid_data_pr, per=95).sel(percentiles=95)
                r99 = percentile_doy(grid_data_pr, per=99).sel(percentiles=99)
                # คำนวณค่า TNn, TXx, rx1day แบบ yearly
                cdd_yearly = xc.indices.dry_spell_max_length(grid_data_pr, freq='YS')
                csdi_yearly = xc.indices.cold_spell_duration_index(grid_data_tmin, tn10, freq='YS')
                cwd_yearly = xc.indices.wet_spell_max_length(grid_data_pr, freq='YS')
                dtr_yearly = xc.indices.daily_temperature_range(grid_data_tmin, grid_data_tmax, freq='YS')
                # fd_yearly = xc.indices.frost_days(grid_data_tmin, freq='YS')
                gsl_yearly = xc.indices.growing_season_length(grid_data_tmin, thresh='25.0 degC', freq='YS')
                prcptot_yearly = xc.indices.prcptot(grid_data_pr, freq='YS') 
                r10mm_yearly = xc.indices.wetdays(grid_data_pr, thresh='10.0 mm/day', freq='YS')# Annual count of days when PRCP ≥ 10mm
                r20mm_yearly = xc.indices.wetdays(grid_data_pr, thresh='20.0 mm/day', freq='YS')# Annual count of days when PRCP ≥ 20mm
                r95p_yearly = xc.indices.days_over_precip_thresh(grid_data_pr, r95, freq='YS')
                r99p_yearly = xc.indices.days_over_precip_thresh(grid_data_pr, r99, freq='YS') # Annual total PRCP when RR > 99th percentile
                rx1day_yearly = xc.indices.max_1day_precipitation_amount(grid_data_pr, freq='YS')
                rx5day_yearly = xc.indices.max_n_day_precipitation_amount(grid_data_pr,window=5, freq='YS')
                sdii_yearly = xc.indices.daily_pr_intensity(grid_data_pr, freq='YS')
                su_yearly = xc.indices.tx_days_above(grid_data_tmax, freq='YS')
                txm_yearly = xc.indices.tx_mean(grid_data_tmax, freq='YS')
                tnm_yearly = xc.indices.tn_mean(grid_data_tmin, freq='YS')
                tn10p_yearly = xc.indices.tn10p(grid_data_tmin, tn10, freq='YS')
                tn90p_yearly = xc.indices.tn90p(grid_data_tmin, tn90, freq='YS')
                tnn_yearly = xc.indices.tn_min(grid_data_tmin, freq='YS')
                txn_yearly = xc.indices.tx_max(grid_data_tmax, freq='YS')
                tr_yearly = xc.indices.tn_days_above(grid_data_tmin, freq='YS')
                tx10p_yearly = xc.indices.tx10p(grid_data_tmax, tx10, freq='YS')
                tx90p_yearly = xc.indices.tx90p(grid_data_tmax, tx90, freq='YS')
                tnx_yearly = xc.indices.tn_max(grid_data_tmin, freq='YS')
                txx_yearly = xc.indices.tx_max(grid_data_tmax, freq='YS')
                wsdi_yearly = xc.indices.warm_spell_duration_index(grid_data_tmax, tx90, freq='YS') 
                rx1day_yearly = xc.indices.max_1day_precipitation_amount(grid_data_pr, freq='YS')

                # cdd_mm = float(cdd_yearly.isel(time=0).item()) if cdd_yearly.size > 0 else None
                # csdi_mm = float(csdi_yearly.isel(time=0).item()) if csdi_yearly.size > 0 else None
                # cwd_mm = float(cwd_yearly.isel(time=0).item()) if cwd_yearly.size > 0 else None
                cdd_mm = float(cdd_yearly.values.item()) if cdd_yearly.size > 0 else None
                csdi_mm = float(csdi_yearly.values.item()) if csdi_yearly.size > 0 else None
                cwd_mm = float(cwd_yearly.values.item()) if cwd_yearly.size > 0 else None
                dtr_celsius = float(dtr_yearly.values.item()) if dtr_yearly.size > 0 else None
                # fd_celsius = float(fd_yearly.values.item()) if fd_yearly.size > 0 else None
                gsl_celsius = float(gsl_yearly.values.item()) if gsl_yearly.size > 0 else None
                prcptot_celsius = float(prcptot_yearly.values.item()) if prcptot_yearly.size > 0 else None
                r10mm_celsius = float(r10mm_yearly.values.item()) if r10mm_yearly.size > 0 else None
                r20mm_celsius = float(r20mm_yearly.values.item()) if r20mm_yearly.size > 0 else None
                r95p_mm = float(r95p_yearly.values.item()) if r95p_yearly.size > 0 else None
                r99p_mm = float(r99p_yearly.values.item()) if r99p_yearly.size > 0 else None
                # rx1day_mm = float(rx1day_yearly.isel(time=0).item()) if rx1day_yearly.size > 0 else None
                rx1day_mm = float(rx1day_yearly.values.item()) if rx1day_yearly.size > 0 else None
                rx5day_mm = float(rx5day_yearly.values.item()) if rx5day_yearly.size > 0 else None
                sdii_mm = float(sdii_yearly.values.item()) if sdii_yearly.size > 0 else None
                su_celsius = float(su_yearly.values.item()) if su_yearly.size > 0 else None
                txm_celsius = float(txm_yearly.values.item()) if txm_yearly.size > 0 else None
                tnm_celsius = float(tnm_yearly.values.item()) if tnm_yearly.size > 0 else None
                tn10p_celsius = float(tn10p_yearly.values.item()) if tn10p_yearly.size > 0 else None
                tn90p_celsius = float(tn90p_yearly.values.item()) if tn90p_yearly.size > 0 else None
                tnn_celsius = float(tnn_yearly.values.item()) if tnn_yearly.size > 0 else None
                txn_celsius = float(txn_yearly.values.item()) if txn_yearly.size > 0 else None
                tr_celsius = float(tr_yearly.values.item()) if tr_yearly.size > 0 else None
                tx10p_celsius = float(tx10p_yearly.values.item()) if tx10p_yearly.size > 0 else None
                tx90p_celsius = float(tx90p_yearly.values.item()) if tx90p_yearly.size > 0 else None
                tnx_celsius = float(tnx_yearly.values.item()) if tnx_yearly.size > 0 else None
                txx_celsius = float(txx_yearly.values.item()) if txx_yearly.size > 0 else None
                wsdi_celsius = float(wsdi_yearly.values.item()) if wsdi_yearly.size > 0 else None
                grid_polygon = create_grid_polygon(lon.item(), lat.item(), lon_step, lat_step)

                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [grid_polygon]
                    },
                    "properties": {
                        "cdd": cdd_mm,
                        "csdi": csdi_mm,
                        "cwd": cwd_mm,
                        "dtr": dtr_celsius,
                        # "fd": fd_celsius,
                        "gsl": gsl_celsius,
                        "prcptot": prcptot_celsius, 
                        "r10mm": r10mm_celsius,
                        "r20mm": r20mm_celsius,
                        "r95p": r95p_mm,
                        "r99p": r99p_mm,
                        "rx1day": rx1day_mm,
                        "rx5day": rx5day_mm,
                        "sdii": sdii_mm,
                        "su": su_celsius,
                        "txm": txm_celsius,
                        "tnm": tnm_celsius,
                        "tn10p": tn10p_celsius,
                        "tn90p": tn90p_celsius,
                        "tnn": tnn_celsius,
                        "txn": txn_celsius,
                        "tr": tr_celsius,
                        "tx10p": tx10p_celsius,
                        "tx90p": tx90p_celsius,
                        "tnx": tnx_celsius,
                        "txx": txx_celsius,
                        "wsdi": wsdi_celsius,
                    }
                })

                pbar.update(1)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

output_file = "./src/Geo-data/Era-Dataset/era_index_grid.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=4)

print(f"ข้อมูลสำหรับปี {year} ถูกบันทึกในไฟล์ {output_file}")

print("Processing complete!")