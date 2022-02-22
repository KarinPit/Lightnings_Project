import pandas as pd
import math
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


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


def get_points_on_line(long_points_med, lat_points_med):
    long_points = []
    lat_points = []

    for long in long_points_med:
        for lat in lat_points_med:

            if -4.43 <= long < 6.35:
                calc_lat1 = 0.382 * long + 36.93
                if calc_lat1 - 0.5 < lat < calc_lat1 + 0.5:
                    long_points.append(long)
                    lat_points.append(lat)

            if 6.35 <= long < 17.13:
                calc_lat2 = -0.403 * long + 41.92
                if calc_lat2 -0.5 < lat < calc_lat2 + 0.5:
                    long_points.append(long)
                    lat_points.append(lat)

            if 17.13 <= long <= 34.84:
                calc_lat3 = -0.14 * long + 37.34
                if calc_lat3 -0.5 < lat < calc_lat3 + 0.5:
                    long_points.append(long)
                    lat_points.append(lat)

    return long_points, lat_points


def get_long_lat_index(long_bins, lat_bins, long_points, lat_points):
    long_index = []
    lat_index = []

    for long in long_points:
        index = long_bins.index(long)
        long_index.append(index)
    for lat in lat_points:
        index = lat_bins.index(lat)
        lat_index.append(index)

    return long_index, lat_index


def get_intensity_by_index(long_index, lat_index, long_bins, lat_bins):
    total_sum_file = 'D:/WWLLN-Intensity/Validation CSV/Summary/total_total_sum.csv'
    total_sum = pd.read_csv(total_sum_file)

    data = []
    for long, lat in zip(long_index, lat_index):
        lat = str(lat)
        intensity_val = total_sum[lat][long]
        data.append(intensity_val)

    longs = []
    lats = []

    for index in long_index:
        val = long_bins[index]
        longs.append(val)
    for index in lat_index:
        val = lat_bins[index]
        lats.append(val)

    df = pd.DataFrame({})
    df['longs'] = longs
    df['lats'] = lats
    df['Intensity'] = data
    df.to_excel('D:/WWLLN-Intensity/Validation CSV/Summary/intensity_distribution.xlsx')


def calc_sum():
    # df = pd.read_excel('D:/WWLLN-Intensity/Validation CSV/data/intensity_distribution_excel.xlsx', sheet_name='intensity_distribution')
    df = pd.read_excel('D:/WWLLN-Intensity/Validation CSV/Summary/intensity_distribution.xlsx')
    df2 = df.groupby('longs').mean()
    # longs = df2['longs'].tolist()
    df2.to_csv('D:/WWLLN-Intensity/Validation CSV/Summary/intensity_distribution_summary.csv')
    # print(longs)


def get_array_mean():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/alk.nc'
    alk_ds = xr.open_dataset(nc_file)
    pandas_times = alk_ds.time.to_pandas()
    array_list = []
    for i in pandas_times:
        file_name = str(i.year) + '-' + str(i.month)
        if i.month in [1, 2, 3]:
            ptimes_list = pandas_times.to_list()
            index = ptimes_list.index(i)
            alk_stime = alk_ds.talk.isel(time=index)
            np_arr = alk_stime.to_numpy()
            np_arr = np.nan_to_num(np_arr, nan=0)
            array_list.append(np_arr)

    mean_array = np.mean(array_list, axis=0)
    mean_array_micromol = mean_array * 974.658
    lat_list = alk_ds.latitude.data.tolist()
    long_list = alk_ds.longitude.data.tolist()
    return mean_array_micromol, lat_list, long_list


def main():
    long_points_med, lat_points_med, islands_coords_dict = get_long_lats_med()
    mean_array_micromol, lat_list, long_list = get_array_mean()
    # long_bins = np.arange(min(long_points_med), max(long_points_med), 0.045).tolist()
    # lat_bins = np.arange(min(lat_points_med), max(lat_points_med), 0.045).tolist()
    # long_bins = sorted(long_bins)
    # lat_bins = sorted(lat_bins)
    long_bins = sorted(long_list)
    lat_bins = sorted(lat_list)

    long_points, lat_points = get_points_on_line(long_bins, lat_bins)
    long_index, lat_index = get_long_lat_index(long_bins, lat_bins, long_points, lat_points)
    intensity_data = get_intensity_by_index(long_index, lat_index, long_bins, lat_bins)
    calc_sum()



if __name__ == '__main__':
    main()
