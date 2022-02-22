import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np


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
            # np_arr = np.nan_to_num(np_arr, nan=0)
            array_list.append(np_arr)

    mean_array = np.nanmean(array_list, axis=0)
    mean_array_micromol = mean_array * 974.658
    lat_list = alk_ds.latitude.data.tolist()
    long_list = alk_ds.longitude.data.tolist()
    return mean_array_micromol, lat_list, long_list

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


def get_alk_values(long_index, lat_index, mean_array_micromol):
    df = pd.DataFrame(mean_array_micromol[0])
    data = []
    for long, lat in zip(long_index, lat_index):
        alk_val = df[long][int(lat)]
        data.append(alk_val)
    return data


def export_alk_on_line(long_points, alk_data):
    df = pd.DataFrame({})
    df['longs'] = long_points
    df['alkalinity'] = alk_data
    df2 = df.groupby('longs').mean()
    df2.to_csv('D:/WWLLN-Intensity/Validation CSV/data/alk_on_line_new.csv')


def main():
    mean_array_micromol, lat_list, long_list = get_array_mean()
    long_points, lat_points, long_index, lat_index = get_points_on_line(lat_list, long_list)
    alk_data = get_alk_values(long_index, lat_index, mean_array_micromol)
    export_alk_on_line(long_points, alk_data)
    # plt.plot(long_points, lat_points)
    # plt.show()



if __name__ == '__main__':
    main()