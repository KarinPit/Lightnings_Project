import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.cm as cm
import math


def get_array_mean():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/sal.nc'
    sal_ds = xr.open_dataset(nc_file)
    pandas_times = sal_ds.time.to_pandas()
    array_list = []
    for i in pandas_times:
        file_name = str(i.year) + '-' + str(i.month)
        if i.month in [1, 2, 3]:
            stimes_list = pandas_times.to_list()
            index = stimes_list.index(i)
            sal_stime = sal_ds.so.isel(time=index)
            np_arr = sal_stime.to_numpy()
            # np_arr = np.nan_to_num(np_arr, nan=0)
            array_list.append(np_arr)

    mean_array = np.nanmean(array_list, axis=0)
    lat_list = sal_ds.lat.data.tolist()
    long_list = sal_ds.lon.data.tolist()
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


def get_sal_values(long_index, lat_index, mean_array):
    df = pd.DataFrame(mean_array[0])
    data = []
    for long, lat in zip(long_index, lat_index):
        ph_val = df[long][int(lat)]
        data.append(ph_val)
    return data


def export_sal_on_line(long_points, sal_data):
    df = pd.DataFrame({})
    df['longs'] = long_points
    df['sal'] = sal_data
    df2 = df.groupby('longs').mean()
    df2.to_csv('D:/WWLLN-Intensity/Validation CSV/data/sal_on_line.csv')


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


def get_sal_plot(mean_array, lat_list, long_list):
    cmap = cm.get_cmap('YlOrRd')
    min_sal = 36.5
    max_sal = 40
    levels = np.linspace(min_sal, max_sal, 10)
    sal_plot = plt.contourf(long_list, lat_list, mean_array[0], alpha=1, cmap=cmap, levels=levels, zorder=0)
    ticks = np.linspace(min_sal, max_sal, 5, endpoint=True)
    cb2 = plt.colorbar(sal_plot, ticks= ticks, shrink=0.55)
    cb2.ax.set_title('sal', fontsize=14)
    # cb2.set_label('\u03BC' + 'mol' '/ Kg', fontsize=14, labelpad=30)

    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    plt.plot(long_points_med, lat_points_med, color='k', zorder=100)
    plt.show()


def main():
    mean_array, lat_list, long_list = get_array_mean()
    long_points, lat_points, long_index, lat_index = get_points_on_line(lat_list, long_list)
    sal_data = get_sal_values(long_index, lat_index, mean_array)
    get_sal_plot(mean_array, lat_list, long_list)
    export_sal_on_line(long_points, sal_data)
    # plt.plot(long_points, lat_points)
    # plt.show()



if __name__ == '__main__':
    main()