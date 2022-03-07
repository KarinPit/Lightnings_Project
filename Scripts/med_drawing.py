import pandas as pd
import math
from shapely import geometry
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# from matplotlib.patches import Rectangle
# import matplotlib.pyplot as plt
#
# fig, axes = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
# extent = [-5.5, 37, 28, 46]
# axes.add_feature(cfeature.LAND, color='white', zorder=50)
# axes.add_feature(cfeature.COASTLINE, color='k', zorder=50)
# axes.set_extent(extent)
# rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor='white')
# rect_right = Rectangle((27.5, 40), 10, 10, zorder=75, facecolor='white')
# axes.add_patch(rect_left)
# axes.add_patch(rect_right)
# axes.outline_patch.set_visible(False)
# plt.show()


def get_long_lats_med():
    med_coords = pd.read_excel('D:/WWLLN/Summary Graphs/Summary csv/Mediterranean coastline and Islands polygons.xlsx')
    long_points_med = med_coords.Long
    lat_points_med = med_coords.Lat

    islands = ['Majorca', 'Sardinia', 'Corsica', 'Sicily','Peleponnese', 'Crete', 'Cyprus', 'Rhodes', 'Kios_Lesbos']
    columns = med_coords.columns
    islands_column_dict = {}
    islands_coords_dict = {}

    for island in islands:
        island_column = []
        for column in columns:
            if island in column:
                island_column.append(column)
        islands_column_dict[island] = island_column

    for island in islands_column_dict:
        longs = []
        lats = []
        island_columns = islands_column_dict[island]
        long_column = island_columns[0]
        lat_column = island_columns[1]
        island_longs = med_coords[long_column]
        island_lats = med_coords[lat_column]
        for long, lat in zip(island_longs, island_lats):
            if math.isnan(long) == False and math.isnan(lat) == False:
                longs.append(long)
                lats.append(lat)
        coords = [longs, lats]
        islands_coords_dict[island] = coords
    return long_points_med, lat_points_med, islands_coords_dict


def get_island_polygon(island, islands_coords_dict):
    coords = islands_coords_dict[island]
    longs = coords[0]
    lats = coords[1]
    islands_line = geometry.LineString(zip(longs, lats))
    island = geometry.Polygon(islands_line)
    return island


def get_med_polygon(long_points_med, lat_points_med):
    med_line = geometry.LineString(zip(long_points_med, lat_points_med))
    med_poly = geometry.Polygon(med_line)
    return med_poly


def get_all_polygons():
    long_points_med, lat_points_med, islands_coords_dict = get_long_lats_med()
    med_poly = get_med_polygon(long_points_med, lat_points_med)
    majorca_poly = get_island_polygon('Majorca', islands_coords_dict)
    corsica_poly = get_island_polygon('Corsica', islands_coords_dict)
    sardinia_poly = get_island_polygon('Sardinia', islands_coords_dict)
    sicily_poly = get_island_polygon('Sicily', islands_coords_dict)
    peleponnese_poly = get_island_polygon('Peleponnese', islands_coords_dict)
    crete_poly = get_island_polygon('Crete', islands_coords_dict)
    cyprus_poly = get_island_polygon('Cyprus', islands_coords_dict)
    rhodes_poly = get_island_polygon('Rhodes', islands_coords_dict)
    kios_lesbos_poly = get_island_polygon('Kios_Lesbos', islands_coords_dict)
    return med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly


def main():
    fig, axes = plt.subplots()
    long_points_med, lat_points_med, islands_coords_dict = get_long_lats_med()
    # print(long_points_med.tolist())
    # print(lat_points_med.tolist())
    axes.fill(long_points_med, lat_points_med, color='#4DB3C4')
    axes.plot(long_points_med, lat_points_med, color='k')
    for island in islands_coords_dict:
        island_coords = islands_coords_dict[island]
        island_longs = island_coords[0]
        island_lats = island_coords[1]
        axes.fill(island_longs, island_lats, color='w')
        axes.plot(island_longs, island_lats, color='k')
    rect_right = Rectangle((32, 30.8), 4.5, 6.3, zorder=75, edgecolor='red', linewidth=4, linestyle='--', fill= False)
    axes.add_patch(rect_right)
    plt.xticks(np.arange(-6, 38, 2))
    plt.show()


if __name__ == '__main__':
    main()

