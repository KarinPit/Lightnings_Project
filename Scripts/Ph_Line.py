import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.cm as cm
import math


def get_array_mean():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/ph.nc'
    ph_ds = xr.open_dataset(nc_file)
    pandas_times = ph_ds.time.to_pandas()
    array_list = []
    for i in pandas_times:
        file_name = str(i.year) + '-' + str(i.month)
        if i.month in [1, 2, 3]:
            ptimes_list = pandas_times.to_list()
            index = ptimes_list.index(i)
            ph_stime = ph_ds.ph.isel(time=index)
            np_arr = ph_stime.to_numpy()
            # np_arr = np.nan_to_num(np_arr, nan=0)
            array_list.append(np_arr)

    mean_array = np.nanmean(array_list, axis=0)
    lat_list = ph_ds.latitude.data.tolist()
    long_list = ph_ds.longitude.data.tolist()
    return mean_array, lat_list, long_list


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


def get_ph_values(long_index, lat_index, mean_array):
    df = pd.DataFrame(mean_array[0])
    data = []
    for long, lat in zip(long_index, lat_index):
        ph_val = df[long][int(lat)]
        data.append(ph_val)
    return data


def export_ph_on_line(long_points, alk_data):
    df = pd.DataFrame({})
    df['longs'] = long_points
    df['ph'] = alk_data
    df2 = df.groupby('longs').mean()
    df2.to_csv('D:/WWLLN-Intensity/Validation CSV/data/ph_on_line_new.csv')


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


def get_ph_plot(mean_array, lat_list, long_list):
    cmap = cm.get_cmap('PuBu')
    min_ph = 8.05
    max_ph = 8.2
    levels = np.linspace(min_ph, max_ph, 10)
    alk_plot = plt.contourf(long_list, lat_list, mean_array[0], alpha=1, cmap=cmap, levels=levels, zorder=0)
    ticks = np.linspace(min_ph, max_ph, 5, endpoint=True)
    cb2 = plt.colorbar(alk_plot, ticks= ticks, shrink=0.55)
    cb2.ax.set_title('PH', fontsize=14)
    # cb2.set_label('\u03BC' + 'mol' '/ Kg', fontsize=14, labelpad=30)

    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    plt.plot(long_points_med, lat_points_med, color='k', zorder=100)
    plt.show()


def main():
    mean_array, lat_list, long_list = get_array_mean()
    long_points, lat_points, long_index, lat_index = get_points_on_line(lat_list, long_list)
    ph_data = get_ph_values(long_index, lat_index, mean_array)
    get_ph_plot(mean_array, lat_list, long_list)
    export_ph_on_line(long_points, ph_data)
    # plt.plot(long_points, lat_points)
    # plt.show()



if __name__ == '__main__':
    main()