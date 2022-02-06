import pandas as pd
from shapely import geometry
import matplotlib.pyplot as plt
import math
import os
import numpy as np
from scipy.stats import binned_statistic_2d

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

def main():
    long = np.random.uniform(-10, 50)
    lat = np.random.uniform(20, 50)
    random_long = []
    random_lat = []
    random_voltage = []
    for i in range(100):
        long = np.random.uniform(-10, 50)
        lat = np.random.uniform(20, 50)
        voltage = np.random.uniform(300, 600)
        random_long.append(long)
        random_lat.append(lat)
        random_voltage.append(voltage)

    # plt.hist2d(random_long, random_lat)
    # plt.scatter(random_long, random_lat, c= random_voltage)
    # plt.colorbar()

    fig ,(ax0, ax1) = plt.subplots(1, 2)
    plot_3vars = binned_statistic_2d(random_long, random_lat, random_voltage, statistic=np.sum, bins=(10, 10))
    ax0.scatter(random_long, random_lat, c= random_voltage)
    imshow = ax1.imshow(plot_3vars.statistic.T, extent=(min(random_long), max(random_long), min(random_lat), max(random_lat)))
    plt.colorbar(imshow)
    plt.show()





    # long_points_med, lat_points_med, islands_coords_dict = get_long_lats_med()
    # med_poly = get_med_polygon(long_points_med, lat_points_med)
    # majorca_poly = get_island_polygon('Majorca', islands_coords_dict)
    # corsica_poly = get_island_polygon('Corsica', islands_coords_dict)
    # sardinia_poly = get_island_polygon('Sardinia', islands_coords_dict)
    # sicily_poly = get_island_polygon('Sicily', islands_coords_dict)
    # peleponnese_poly = get_island_polygon('Peleponnese', islands_coords_dict)
    # crete_poly = get_island_polygon('Crete', islands_coords_dict)
    # cyprus_poly = get_island_polygon('Cyprus', islands_coords_dict)
    # rhodes_poly = get_island_polygon('Rhodes', islands_coords_dict)
    # kios_lesbos_poly = get_island_polygon('Kios_Lesbos', islands_coords_dict)
    #
    #
    # random_long = []
    # random_lat = []
    # for i in range(1000000):
    #     long = np.random.uniform(-10, 50)
    #     lat = np.random.uniform(20, 50)
    #     random_long.append(long)
    #     random_lat.append(lat)
    #
    # east = []
    # west = []
    #
    # for long, lat in zip(random_long, random_lat):
    #     point = geometry.Point(long, lat)
    #     if med_poly.contains(point):
    #         if majorca_poly.contains(point) == False and corsica_poly.contains(
    #                 point) == False and sardinia_poly.contains(point) == False and sicily_poly.contains(
    #                 point) == False and peleponnese_poly.contains(point) == False and crete_poly.contains(
    #                 point) == False and cyprus_poly.contains(point) == False and rhodes_poly.contains(
    #                 point) == False and kios_lesbos_poly.contains(point) == False:
    #             if long < 16.5:
    #                 west.append(point)
    #             if long > 16.5:
    #                 east.append(point)
    #
    # east_x = [point.x for point in east]
    # east_y = [point.y for point in east]
    # west_x = [point.x for point in west]
    # west_y = [point.y for point in west]
    #
    # fig, axes = plt.subplots()
    # axes.plot(long_points_med, lat_points_med)
    # axes.scatter(east_x,east_y, color='blue')
    # axes.scatter(west_x, west_y, color='red')
    # plt.show()

if __name__ == '__main__':
    main()