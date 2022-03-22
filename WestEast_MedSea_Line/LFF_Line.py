import pandas as pd
import os
import xarray as xr
import numpy as np


def get_longs_lats_dataset():
    examp_nc_file = 'D:/WWLLN-Intensity/Validation CSV/info/ph.nc'
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


def get_all_files(dir):
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


def get_yearly_files_dict():
    # create dict which correlates between year and month, and the files in each month
    years = get_years_path()
    yearly_files_dict = {}
    for year in years:
        month_dict = get_month_files_dict(year, years)
        year_name = year[-4:]
        yearly_files_dict[year_name] = month_dict
    yearly_files_dict.pop('2021')
    return yearly_files_dict


def get_month_files_dict(year_path, years):
    month_files_dict = {}
    year_index = years.index(year_path)
    for item in os.listdir(year_path):
        item_name = item[0:3]
        full_path = os.path.join(year_path, item)
        full_path = full_path.replace('\\', '/')
        if os.path.isdir(full_path) == True:
            if item_name == 'Dec':
                files = get_all_files(full_path)
                month_files_dict[item_name] = files

            if item_name == 'Jan':
                new_index = year_index - 1
                new_year = years[new_index]
                new_year_name = new_year[-4:]
                month_dir_list = []
                file_list = []
                if new_year_name in ['2010', '2011']:
                    new_year_name = [new_year[-4:], new_year[-4:] + 'a', new_year[-4:] + 'b']
                    for i in new_year_name:
                        new_dir_name = item_name + i
                        full_path = os.path.join(new_year, new_dir_name)
                        full_path = full_path.replace('\\', '/')
                        month_dir_list.append(full_path)
                    for i in month_dir_list:
                        files = get_all_files(i)
                        file_list = file_list + files
                    month_files_dict[item_name] = file_list
                else:
                    new_index = year_index - 1
                    new_year = years[new_index]
                    new_year_name = new_year[-4:]
                    new_dir_name = item_name + new_year_name
                    full_path = os.path.join(new_year, new_dir_name)
                    full_path = full_path.replace('\\', '/')
                    files = get_all_files(full_path)
                    month_files_dict[item_name] = files

            if item_name == 'Feb':
                new_index = year_index - 1
                new_year = years[new_index]
                new_year_name = new_year[-4:]
                new_dir_name = item_name + new_year_name
                full_path = os.path.join(new_year, new_dir_name)
                full_path = full_path.replace('\\', '/')
                files = get_all_files(full_path)
                month_files_dict[item_name] = files
    return month_files_dict


def get_yearly_df_dict(yearly_files_dict):
    # convert the files dict into df for each month of each year
    monthly_df_dict = {}
    united_df_dict = {}
    for year in list(yearly_files_dict.keys()):
        print(year)
        months = yearly_files_dict[year]
        df_dict = get_months_df_dict(months)
        united_df = get_united_df(df_dict)
        monthly_df_dict[year] = df_dict
        united_df_dict[year] = united_df
    return monthly_df_dict, united_df_dict


def get_months_df_dict(months_files_dict):
    # This function receives a file list and returns one united file.
    df_dict = {}
    dirs = list(months_files_dict.keys())
    fields = ['Date', 'Long', 'Lat']
    for dir in dirs:
        data = []
        files = months_files_dict[dir]
        for file in files:
            df = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'], usecols=fields)
            # df = df[(df.Long > -6) & (df.Long < 36.3)]
            df = df[(df.Long > 16.5) & (df.Long < 36.3)]
            df = df[(df.Lat > 30.18) & (df.Lat < 45.98)]
            data.append(df)
        month_df = pd.concat(data)
        month_df.drop_duplicates(['Date', 'Long', 'Lat'], keep= 'first', inplace= True)
        df_dict[dir] = month_df
        print(f'finished combining {dir}')
    return df_dict


def get_united_df(df_dict):
    months = list(df_dict.keys())
    united_df = pd.DataFrame({})
    for month in months:
        df = df_dict[month]
        united_df = pd.concat([united_df, df])
    return united_df


def get_line_df(df):
    data = []
    for date, long, lat in zip(df.Date, df.Long, df.Lat):
        if -4.43 <= long < 6.35:
            calc_lat1 = 0.382 * long + 36.93
            if calc_lat1 -0.5 < lat < calc_lat1 + 0.5:
                data.append([date, long, lat])

        if 6.35 <= long < 17.13:
            calc_lat2 = -0.403 * long + 41.92
            if calc_lat2 -0.5 < lat < calc_lat2 + 0.5:
                data.append([date, long, lat])

        if 17.13 <= long <= 34.84:
            calc_lat3 = -0.14 * long + 37.34
            if calc_lat3 -0.5 < lat < calc_lat3 + 0.5:
                data.append([date, long, lat])

    line_df = pd.DataFrame(data, columns=['Date', 'Long', 'Lat'])
    line_df.drop_duplicates(keep=False, inplace=True)
    return line_df


def get_values_dict(line_df, examp_longs, examp_lats):
    hist, xedges, yedges = np.histogram2d(line_df.Long, line_df.Lat, bins=[examp_longs, examp_lats])
    hist_df = pd.DataFrame(hist)
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
    df = pd.DataFrame({})
    df['Longs'] = x_values
    df['Num Lightnings'] = num_lightnings
    tp_df2 = df.groupby('Longs').mean()
    return tp_df2


def main():
    examp_longs, examp_lats = get_longs_lats_dataset()  # get the longs and the lats of copernicus dataset
    yearly_files_dict = get_yearly_files_dict()  # get a dict where each year is a key that contains the monthly df
    yearly_df_dict, united_df_dict = get_yearly_df_dict(yearly_files_dict)  # create df dict from yearly files dict

    writer = pd.ExcelWriter('D:/WWLLN/Summary Graphs/Yearly_LFF_Line.xlsx', engine='xlsxwriter')
    for year in yearly_df_dict:
        months = yearly_df_dict[year]
        line_data = []
        for month in months:
            month_df = months[month]
            df = get_line_df(month_df)
            line_data.append(df)
        line_df = pd.concat(line_data)
        line_df = get_values_dict(line_df, examp_longs, examp_lats)
        line_df.to_excel(writer, sheet_name=year)
    writer.save()


if __name__ == '__main__':
    main()
