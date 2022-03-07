import pandas as pd
import os
import xarray as xr
from shapely import geometry
from scipy.stats import binned_statistic_2d
import math
import numpy as np


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

            if item_name == 'Nov':
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


def get_months_df_dict(months_files_dict):
    # This function receives a file list and returns one united file.
    med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly = get_all_polygons()

    df_dict = {}
    dirs = list(months_files_dict.keys())
    fields = ['Date', 'Long', 'Lat']
    for dir in dirs:
        data = []
        files = months_files_dict[dir]
        for file in files:
            df = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'], usecols=fields)
            df = df[(df.Long > -6) & (df.Long < 36.3)]
            df = df[(df.Lat > 30.18) & (df.Lat < 45.98)]
            for date, long, lat in zip(df.Date, df.Long, df.Lat):
                point = geometry.Point(long, lat)
                if med_poly.contains(point):
                    if majorca_poly.contains(point) is False and corsica_poly.contains(
                            point) is False and sardinia_poly.contains(point) is False and sicily_poly.contains(
                            point) is False and peleponnese_poly.contains(point) is False and crete_poly.contains(
                            point) is False and cyprus_poly.contains(point) is False and rhodes_poly.contains(
                            point) is False and kios_lesbos_poly.contains(point) is False:
                        coords = (date, long, lat)
                        data.append([date, long, lat])

        month_df = pd.DataFrame(data, columns=['Date', 'Long', 'Lat'])
        month_df.drop_duplicates(['Long', 'Lat'], keep= 'first', inplace= True)
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


def get_longs_lats_dataset():
    examp_nc_file = 'D:/WWLLN-Intensity/Validation CSV/ph.nc'
    examp_ds = xr.open_dataset(examp_nc_file)
    examp_longs = examp_ds.longitude.to_numpy().tolist()
    examp_lats = examp_ds.latitude.to_numpy().tolist()
    return examp_longs, examp_lats


def get_data_stats(df, examp_longs, examp_lats):
    longs = df.Long
    lats = df.Lat
    plot_3vars_count = binned_statistic_2d(longs, lats, None, statistic='count', bins=[examp_longs, examp_lats])
    stats_data = plot_3vars_count.statistic
    return stats_data


def main():
    # # get a dict where each year is a key that contains the monthly df
    # yearly_files_dict = get_yearly_files_dict()
    # yearly_df_dict, united_df_dict = get_yearly_df_dict(yearly_files_dict)
    #
    # # get the lightning count for each grid box in the given grid
    # examp_longs, examp_lats = get_longs_lats_dataset()
    # for year in yearly_df_dict:
    #     months_dict = yearly_df_dict[year]
    #     for month in months_dict:
    #         data = months_dict[month]
    #         data.to_csv(f'D:/WWLLN/Summary Graphs/all_med_sea_data_freq/{year}-{month}.csv')
    #         stats_data = get_data_stats(data, examp_longs, examp_lats)
    #         df = pd.DataFrame(stats_data)
    #         df.to_csv(f'D:/WWLLN/Summary Graphs/all_med_sea_data_freq/{year}-{month}-matrix.csv')


    examp_longs, examp_lats = get_longs_lats_dataset()

    years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    main_dir = 'D:/WWLLN/Summary Graphs/all_med_sea_data_freq/'
    files = os.listdir(main_dir)

    for year in years:
        year_df = pd.DataFrame({})
        file_list = [i for i in files if year in i and 'matrix' in i]
        file_list = sorted(file_list)

        for file in file_list:
            month = file[5:8]
            full_path = os.path.join(main_dir, file)
            df = pd.read_csv(full_path)
            df = df.iloc[:, 1:]
            df = df.replace(0, np.nan)
            df['Mean'] = df.mean(axis=1, skipna= True)
            mean_values = df.Mean.to_list()
            year_df['Longs'] = examp_longs[0:-1]
            year_df[month] = mean_values
        output_path = main_dir + 'Summary/' + f'{year}.csv'
        year_df.to_csv(output_path)





    #
    # dec_df = pd.DataFrame({})
    # dec_df['Longs'] = examp_longs[0:-1]
    # dec_df['Average Frequency'] = mean_values
    # dec_df.to_csv('D:/WWLLN/Summary Graphs/all_med_sea_data_freq/2010-Dec-summary.csv')



if __name__ == '__main__':
    main()


    # df = pd.read_csv('D:/WWLLN/Summary Graphs/all_med_sea_data_freq/2010-Dec-matrix.csv')
    # df = df.iloc[:, 1:]
    # df['Mean'] = df.mean(axis=1)
    # mean_values = df.Mean.to_list()
    #
    # dec_df = pd.DataFrame({})
    # dec_df['Longs'] = examp_longs[0:-1]
    # dec_df['Average Frequency'] = mean_values
    # dec_df.to_csv('D:/WWLLN/Summary Graphs/all_med_sea_data_freq/2010-Dec-summary.csv')
