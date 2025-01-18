import geopandas as gpd
import matplotlib.pyplot as plt

thailand = gpd.read_file("./src/Geo-data/candex_to_geo2.json")
fig, ax = plt.subplots(figsize=(64, 64))

# thai_source.plot(column='temperature', cmap='jet', linewidth=0.5, ax=ax, edgecolor='black', legend=True)

thailand.plot(column='precipitation', ax=ax, legend=True, cmap='jet')
# thailand.plot(column='precipitation', ax=ax)
count = 1
for idx, grid in thailand.iterrows():
    x, y = grid.geometry.centroid.x, grid.geometry.centroid.y
    value = grid['precipitation']
    # ax.text(x, y, f'{value:.10f}', fontsize=5, ha='center', color='black')
    ax.text(x, y, f'{count}', fontsize=5, ha='center', color='black')
    count += 1
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()