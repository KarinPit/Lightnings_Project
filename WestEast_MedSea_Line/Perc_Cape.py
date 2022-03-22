import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.cm as cm
import math
from scipy.interpolate import interp2d
from shapely import geometry


def get_longs_lats_dataset():
    examp_nc_file = 'D:/WWLLN-Intensity/Validation CSV/ph.nc'
    examp_ds = xr.open_dataset(examp_nc_file)
    examp_longs = examp_ds.longitude.to_numpy().tolist()
    examp_lats = examp_ds.latitude.to_numpy().tolist()
    return examp_longs, examp_lats


def get_interp2d(examp_longs, examp_lats, long_list, lat_list, tp_mean_array, cape_mean_array):
    tp_f = interp2d(long_list, lat_list, tp_mean_array, kind='cubic')
    tp_interp_arr = tp_f(examp_longs, examp_lats)
    cape_f = interp2d(long_list, lat_list, cape_mean_array, kind='cubic')
    cape_interp_arr = cape_f(examp_longs, examp_lats)
    return tp_interp_arr, cape_interp_arr


def get_array_mean():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/perc_cape.nc'
    perc_cape_ds = xr.open_dataset(nc_file)
    times = perc_cape_ds.time.to_numpy().tolist()

    tp_array_list = []
    cape_array_list = []
    for time in times:
        index_time = times.index(time)
        perc_val = perc_cape_ds.tp.isel(time=index_time)
        cape_val = perc_cape_ds.cape.isel(time=index_time)
        tp_np_arr = perc_val.to_numpy()
        cape_np_arr = cape_val.to_numpy()
        tp_array_list.append(tp_np_arr)
        cape_array_list.append(cape_np_arr)

    tp_mean_array = np.nanmean(tp_array_list, axis=0)
    cape_mean_array = np.nanmean(cape_array_list, axis=0)
    lat_list = perc_cape_ds.latitude.data.tolist()
    long_list = perc_cape_ds.longitude.data.tolist()
    return tp_mean_array, cape_mean_array, lat_list, long_list


def get_points_on_line(lat_list, long_list):
    long_points = []
    lat_points = []
    long_index = []
    lat_index = []

    for long in long_list:
        for lat in lat_list:

            if -4.43 <= long < 6.35:
                calc_lat1 = 0.382 * long + 36.93
                if calc_lat1 - 0.5 < lat < calc_lat1 + 0.5:
                    long_points.append(long)
                    lat_points.append(lat)
                    index_x = long_list.index(long)
                    index_y = lat_list.index(lat)
                    long_index.append(index_x)
                    lat_index.append(index_y)

            if 6.35 <= long < 17.13:
                calc_lat2 = -0.403 * long + 41.92
                if calc_lat2 - 0.5 < lat < calc_lat2 + 0.5:
                    long_points.append(long)
                    lat_points.append(lat)
                    index_x = long_list.index(long)
                    index_y = lat_list.index(lat)
                    long_index.append(index_x)
                    lat_index.append(index_y)

            if 17.13 <= long <= 34.84:
                calc_lat3 = -0.14 * long + 37.34
                if calc_lat3 - 0.5 < lat < calc_lat3 + 0.5:
                    long_points.append(long)
                    lat_points.append(lat)
                    index_x = long_list.index(long)
                    index_y = lat_list.index(lat)
                    long_index.append(index_x)
                    lat_index.append(index_y)

    return long_points, lat_points, long_index, lat_index


def get_perc_cape_values(long_index, lat_index, tp_mean_array, cape_mean_array):
    # total percipitation dataframe
    tp_df = pd.DataFrame(tp_mean_array)
    tp_data = []
    for long, lat in zip(long_index, lat_index):
        tp_val = tp_df[long][int(lat)]
        tp_data.append(tp_val)

    # cape dataframe
    cape_df = pd.DataFrame(cape_mean_array)
    cape_data = []
    for long, lat in zip(long_index, lat_index):
        cape_val = cape_df[long][int(lat)]
        cape_data.append(cape_val)

    return tp_data, cape_data


def export_perc_cape_on_line(long_points, lat_points, tp_data, cape_data):
    # percipitation export
    tp_df = pd.DataFrame({})
    tp_df['longs'] = long_points
    tp_df['percipitaion'] = tp_data
    tp_df2 = tp_df.groupby('longs').mean()
    tp_df2.to_csv('D:/WWLLN-Intensity/Validation CSV/data/perc_on_line.csv')

    # cape export
    cape_df = pd.DataFrame({})
    cape_df['longs'] = long_points
    cape_df['cape'] = cape_data
    cape_df2 = cape_df.groupby('longs').mean()
    cape_df2.to_csv('D:/WWLLN-Intensity/Validation CSV/data/cape_on_line.csv')


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


def get_points_inside_med(examp_longs, examp_lats):
    med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly = get_all_polygons()
    longs = []
    lats = []
    for long in examp_longs:
        for lat in examp_lats:
            point = geometry.Point(long, lat)
            if med_poly.contains(point) == False:
                long_index = examp_longs.index(long)
                lat_index = examp_lats.index(lat)
                longs.append(long_index)
                lats.append(lat_index)
            else:
                if majorca_poly.contains(point) or corsica_poly.contains(point) or sardinia_poly.contains(point) or sicily_poly.contains(point) or peleponnese_poly.contains(point) or crete_poly.contains(point) or cyprus_poly.contains(point) or rhodes_poly.contains(point) or kios_lesbos_poly.contains(point):
                    long_index = examp_longs.index(long)
                    lat_index = examp_lats.index(lat)
                    longs.append(long_index)
                    lats.append(lat_index)
    return longs, lats


def make_land_mask(tp_interp_arr, cape_interp_arr, longs, lats):
    tp_df = pd.DataFrame(tp_interp_arr)
    cape_df = pd.DataFrame(cape_interp_arr)

    for long, lat in zip(longs, lats):
        tp_df.at[lat, long] = np.nan
        cape_df.at[lat, long] = np.nan

    tp_array = tp_df.to_numpy()
    cape_array = cape_df.to_numpy()
    return tp_array, cape_array


def get_perc_plot(mean_array, long_list, lat_list):
    cmap = cm.get_cmap('YlOrRd')
    min_perc_cape = 0.001
    max_perc_cape = 0.009
    levels = np.linspace(min_perc_cape, max_perc_cape, 10)
    perc_cape_plot = plt.contourf(long_list, lat_list, mean_array, alpha=1, cmap=cmap, levels=levels, zorder=0)
    ticks = np.linspace(min_perc_cape, max_perc_cape, 5, endpoint=True)
    cb2 = plt.colorbar(perc_cape_plot, ticks= ticks, shrink=0.55)
    cb2.ax.set_title('precipitiation', fontsize=14)
    # cb2.set_label('\u03BC' + 'mol' '/ Kg', fontsize=14, labelpad=30)

    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    plt.plot(long_points_med, lat_points_med, color='k', zorder=100)
    plt.show()


def get_cape_plot(mean_array, long_list, lat_list):
    cmap = cm.get_cmap('YlOrRd')
    min_perc_cape = 5
    max_perc_cape = 70
    levels = np.linspace(min_perc_cape, max_perc_cape, 10)
    perc_cape_plot = plt.contourf(long_list, lat_list, mean_array, alpha=1, cmap=cmap, levels=levels, zorder=0)
    ticks = np.linspace(min_perc_cape, max_perc_cape, 5, endpoint=True)
    cb2 = plt.colorbar(perc_cape_plot, ticks= ticks, shrink=0.55)
    cb2.ax.set_title('cape', fontsize=14)
    # cb2.set_label('\u03BC' + 'mol' '/ Kg', fontsize=14, labelpad=30)

    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    plt.plot(long_points_med, lat_points_med, color='k', zorder=100)
    plt.show()


def main():
    # get longs and lats in order to make land mask
    examp_longs, examp_lats = get_longs_lats_dataset()
    longs, lats = get_points_inside_med(examp_longs, examp_lats)

    # get data in order to create the interpolation
    tp_mean_array, cape_mean_array, lat_list, long_list = get_array_mean()
    tp_interp_arr, cape_interp_arr = get_interp2d(examp_longs, examp_lats, long_list, lat_list, tp_mean_array, cape_mean_array)

    # make land mask
    tp_array, cape_array = make_land_mask(tp_interp_arr, cape_interp_arr, longs, lats)

    # get data on the med line and export it to csv
    long_points, lat_points, long_index, lat_index = get_points_on_line(examp_lats, examp_longs)
    tp_data, cape_data = get_perc_cape_values(long_index, lat_index, tp_interp_arr, cape_interp_arr)
    export_perc_cape_on_line(long_points, lat_points, tp_data, cape_data)

    # create cape an precipitation plots
    # get_perc_plot(tp_array, examp_longs, examp_lats)
    get_cape_plot(cape_array, examp_longs, examp_lats)



if __name__ == '__main__':
    main()



    # # print(lat_index)

    # # for sea_long, sea_lat in zip(long_index, lat_index):
    #
    #

    # # for long in tp_df.columns:
    # #     lat_index = len(tp_df[long])
    # #     print(len(val))

    #     tp_df.at[str(long), str(lat)] = 'bla'
    # print(tp_df)

    # for long, lat in zip(longs, lats):
    #     val = tp_df[long][lat]
    #     tp_df[long] = tp_df[long].replace([val], np.nan)
    # print(tp_df)

    # tp_df.replace(lats)
    # for long, lat in zip(longs, lats):
    #     val = tp_df[long][lat]
    #     tp_df.replace(to_replace=val, value=0, inplace=True)

    # columns = [i for i in range(1005)]
    # rows = [i for i in range(380)]
    # new_rows = []
    # for col in columns:
    #     for row in rows:
    #        new_rows.append(row)
    #
    # for long, lat in zip(longs, lats):

    # all_points = []
    # for col in columns:
    #     for row in rows:
    #         point = (col, row)
    #         all_points.append(point)
    #
    # for point in points:
    #     if point in all_points:
    #         all_points.remove(point)
    # print(all_points)
    #
    # for point in all_points:
    #     long_index = point[0]
    #     lat_index = point[1]
    #     tp_df.at[lat_index, str(long_index)] = np.nan
    # print(tp_df)

    # def make_land_mask(tp_interp_arr, cape_interp_arr, points):
    #     tp_df = pd.DataFrame(tp_interp_arr)
    #     cape_df = pd.DataFrame(cape_interp_arr)
    #
    #     columns = [i for i in range(1005)]
    #     rows = [i for i in range(380)]
    #     all_points = []
    #     for col in columns:
    #         for row in rows:
    #             point = (col, row)
    #             all_points.append(point)
    #
    #     for point in points:
    #         if point in all_points:
    #             all_points.remove(point)
    #     print(all_points)
    #
    #     for point in all_points:
    #         long_index = point[0]
    #         lat_index = point[1]
    #         tp_df.at[lat_index, str(long_index)] = np.nan
    #     print(tp_df)


# def get_points_inside_med(examp_longs, examp_lats):
#     med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly = get_all_polygons()
#     points = []
#     for long in examp_longs:
#         for lat in examp_lats:
#             point = geometry.Point(long, lat)
#             if med_poly.contains(point):
#                 if majorca_poly.contains(point) is False and corsica_poly.contains(point) is False and sardinia_poly.contains(point) is False and sicily_poly.contains(point) is False and peleponnese_poly.contains(point) is False and crete_poly.contains(point) is False and cyprus_poly.contains(point) is False and rhodes_poly.contains(point) is False and kios_lesbos_poly.contains(point) is False:
#                     long_index = examp_longs.index(long)
#                     lat_index = examp_lats.index(lat)
#                     point = (long_index, lat_index)
#                     points.append(point)
#     return points

