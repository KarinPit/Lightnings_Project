import xarray as xr
import pandas as pd
import numpy as np
import os


def get_longs_lats_dataset():
    examp_nc_file = 'D:/WWLLN-Intensity/Validation CSV/ph.nc'
    examp_ds = xr.open_dataset(examp_nc_file)
    examp_longs = examp_ds.longitude.to_numpy().tolist()
    examp_lats = examp_ds.latitude.to_numpy().tolist()
    return examp_longs, examp_lats


def get_years_path():
    main_dir_path = 'D:/WWLLN'
    years = []
    for item in os.listdir(main_dir_path):
        full_path = os.path.join(main_dir_path, item)
        if os.path.isdir(full_path) == True and len(item) == 4:
            full_path = full_path.replace('\\', '/')
            years.append(full_path)
    return years


def get_files_in_dir(dir):
    # This function receives a path and returns a list of all existing files in that path.
    all_files = os.listdir(dir)
    loc_files = []
    for file in all_files:
        fullPath = os.path.join(dir, file)
        fullPath = fullPath.replace('\\', '/')
        if file.find('.loc') != -1 and file[0:2] != '._':
            loc_files.append(fullPath)
        else:
            pass
    return loc_files


def get_sum_files_list(dir):
    files = []
    for item in os.listdir(dir):
        item_name = item[0:3]
        full_path = os.path.join(dir, item)
        full_path = full_path.replace('\\', '/')
        if os.path.isdir(full_path) == True and item_name in ['Dec', 'Jan', 'Feb']:
            dir_files = get_files_in_dir(full_path)
            files = files + dir_files
    return files


def get_united_df(files_list):
    united_df = pd.DataFrame({})
    fields = ['Date', 'Time', 'Long', 'Lat']
    for file in files_list:
        print(f'started {file}')
        df = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'], usecols=fields)
        df = df[(df.Long > -6) & (df.Long < 36.3)]
        df = df[(df.Lat > 30.18) & (df.Lat < 45.98)]
        united_df = pd.concat([united_df, df])
    return united_df


def get_united_df_line(df):
    data = []
    for date, time, long, lat in zip(df.Date, df.Time, df.Long, df.Lat):
        if -4.43 <= long < 6.35:
            calc_lat1 = 0.382 * long + 36.93
            if calc_lat1 -0.5 < lat < calc_lat1 + 0.5:
                data.append([date, time, long, lat])

        if 6.35 <= long < 17.13:
            calc_lat2 = -0.403 * long + 41.92
            if calc_lat2 -0.5 < lat < calc_lat2 + 0.5:
                data.append([date, time, long, lat])

        if 17.13 <= long <= 34.84:
            calc_lat3 = -0.14 * long + 37.34
            if calc_lat3 -0.5 < lat < calc_lat3 + 0.5:
                data.append([date, time, long, lat])

    united_df = pd.DataFrame(data, columns=['Date', 'Time', 'Long', 'Lat'])
    united_df.drop_duplicates(keep=False, inplace=True)
    return united_df


def get_values_dict(united_df, examp_longs, examp_lats):
    hist, xedges, yedges = np.histogram2d(united_df.Long, united_df.Lat, bins=[examp_longs, examp_lats])
    hist_df = pd.DataFrame(hist)
    hist_df.to_csv('D:/WWLLN/Frequency_matrix.csv')
    print(yedges[:-1][1] - yedges[:-1][0], 'this is y width')
    width = 0.85 * (xedges[:-1][1] - xedges[:-1][0])
    value_dict = {}
    x_values = []
    num_lightnings = []

    for i in range(len(yedges) -1):
        for j in range(len(xedges) -1):
            value = hist.T[i,j]
            x_value = xedges[j]
            if value != 0:
                x_values.append(x_value)
                num_lightnings.append(value)
                value_dict[x_value] = value
    ticks = np.arange(int(min(value_dict.keys())), int(max(value_dict.keys())) + 1.5, 0.5)
    df = pd.DataFrame({})
    df['Longs'] = x_values
    df['Num Lightnings'] = num_lightnings
    tp_df2 = df.groupby('Longs').mean()
    tp_df2.to_csv('D:/WWLLN/Distribution_on_line.csv')

    # df.to_csv( 'D:/WWLLN/Distribution.csv')
    return width, value_dict, ticks


def main():
    examp_longs, examp_lats = get_longs_lats_dataset()
    years = get_years_path()
    file_list = []
    for year in years:
        dir_files = get_sum_files_list(year)
        file_list = file_list + dir_files

    raw_df = get_united_df(file_list)
    # united_df = get_united_df_line(raw_df)
    width, value_dict, ticks = get_values_dict(raw_df, examp_longs, examp_lats)


if __name__ == '__main__':
    main()