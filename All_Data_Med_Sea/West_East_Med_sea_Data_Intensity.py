import matplotlib.pyplot as plt
import pandas as pd
import os
import xarray as xr
from shapely import geometry
import scipy.stats as stats
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


def get_points_on_line(longs, lats):
    long_points = []
    lat_points = []

    for long in longs:
        for lat in lats:

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


def get_years_path():
    main_dir_path = 'D:/WWLLN-Intensity'
    years = []
    for item in os.listdir(main_dir_path):
        full_path = os.path.join(main_dir_path, item)
        if os.path.isdir(full_path) == True and item[0:3] == 'DJF':
            full_path = full_path.replace('\\', '/')
            years.append(full_path)
    years.sort()
    return years


def get_all_files(dir_path):
    # This function receives a path and returns a list of all existing files in that path.
    all_files = os.listdir(dir_path)
    loc_files = []
    for file in all_files:
        fullPath = os.path.join(dir_path, file)
        fullPath = fullPath.replace('\\', '/')
        if file.find('.loc') != -1 and file[0:2] != '._':
            loc_files.append(fullPath)
        else:
            pass
    return loc_files


def get_year_files_dict(year_paths):
    all_files = {}
    for year in year_paths:
        year_name = year[-7:]
        if year != 'D:/WWLLN-Intensity/DJF2020-21':
        # if year == 'D:/WWLLN-Intensity/DJF2009-10':
            dec_files = []
            jan_files = []
            feb_files = []
            files_folder = os.path.join(year,'loc_files')
            files_folder = files_folder.replace('\\', '/')
            files = get_all_files(files_folder)
            for file in files:
                if file[-8:-6] == '12':
                    dec_files.append(file)
                if file[-8:-6] == '01':
                    jan_files.append(file)
                if file[-8:-6] == '02':
                    feb_files.append(file)
            all_files[year_name] = {'Dec': dec_files, 'Jan': jan_files, 'Feb': feb_files}
    return all_files


def get_year_df_dict(all_files):
    med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly = get_all_polygons()
    all_years_df = {}

    for year in all_files:
        print(year)
        months = list(all_files[year].keys())
        months_df = {}
        for month in months:
            files = all_files[year][month]
            fields = ['Date', 'Long', 'Lat', 'Energy_J']
            data = []
            for file in files:
                df = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nstn', 'Energy_J', 'Energy_Uncertainty', 'Nstn_Energy'], usecols=fields)
                df = df[(df.Long > -6) & (df.Long < 36)]
                df = df[(df.Lat > 30) & (df.Lat < 46)]
                for date, long, lat, energy in zip(df.Date, df.Long, df.Lat, df.Energy_J):
                    point = geometry.Point(long, lat)
                    if med_poly.contains(point):
                        if majorca_poly.contains(point) is False and corsica_poly.contains(
                                point) is False and sardinia_poly.contains(point) is False and sicily_poly.contains(
                            point) is False and peleponnese_poly.contains(point) is False and crete_poly.contains(
                            point) is False and cyprus_poly.contains(point) is False and rhodes_poly.contains(
                            point) is False and kios_lesbos_poly.contains(point) is False:
                            coords = date, long, lat, energy
                            data.append(coords)

            month_df = pd.DataFrame(data, columns=fields)
            month_df.drop_duplicates(['Date', 'Long', 'Lat', 'Energy_J'], keep='first', inplace=True)
            months_df[month] = month_df
        all_years_df[year] = months_df

    return all_years_df


def get_longs_lats_dataset():
    examp_nc_file = 'D:/WWLLN-Intensity/Validation CSV/info/ph.nc'
    examp_ds = xr.open_dataset(examp_nc_file)
    examp_longs = examp_ds.longitude.to_numpy().tolist()
    examp_lats = examp_ds.latitude.to_numpy().tolist()
    return examp_longs, examp_lats


def get_long_mean(df, examp_longs, examp_lats):
    longs = df.Long
    energy = df.Energy_J
    lats = df.Lat
    # hist = stats.binned_statistic(longs, energy, statistic=np.nansum, bins=examp_longs)
    hist = stats.binned_statistic_2d(longs, lats, energy, statistic= np.nanmean, bins=[examp_longs, examp_lats])
    stats_data = hist.statistic
    return stats_data, longs, lats


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


def get_intensity_by_index(df, long_index, lat_index, long_bins, lat_bins):
    data = []
    for long, lat in zip(long_index, lat_index):
        # lat = str(lat)
        intensity_val = df[lat][long]
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
    return df


def main():
    examp_longs, examp_lats = get_longs_lats_dataset()
    long_line_points, lat_line_points = get_points_on_line(examp_longs, examp_lats)
    long_index, lat_index = get_long_lat_index(examp_longs, examp_lats, long_line_points, lat_line_points)

    years = get_years_path()
    all_years_files = get_year_files_dict(years)
    all_years_dfs = get_year_df_dict(all_years_files)
    writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/INT_LINE.xlsx', engine='xlsxwriter')

    for year in all_years_dfs:
        months = all_years_dfs[year]
        yearly_df = pd.DataFrame({})
        yearly_df['Longs'] = examp_longs
        for month in months:
            month_df = months[month]
            stats_data, longs, lats = get_long_mean(month_df, examp_longs, examp_lats)
            stats_df = pd.DataFrame(stats_data)
            line_df = get_intensity_by_index(stats_df, long_index, lat_index, examp_longs, examp_lats)
            yearly_df[month] = line_df.Intensity
        yearly_df.to_excel(writer, sheet_name=year)
    writer.save()


if __name__ == '__main__':
    main()























    # for year in all_years_dfs:
    #     writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/Quartiles/{year}.xlsx', engine='xlsxwriter')
    #     months_dict = all_years_dfs[year]
    #
    #     for month in months_dict:
    #         # create the df and the longs and total sum columns
    #         data = months_dict[month]
    #         stat_data = get_long_mean(data, examp_longs, examp_lats)
    #         df = pd.DataFrame({})
    #         df['Longs'] = examp_longs[0:-1]
    #         df['All_Data'] = stat_data
    #         # df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/{year}-{month}_1d.csv')
    #
    #         # calculate percentage of each threshold
    #         num_all_data = len(df)
    #         first_threshold_perc = round(len(df[(df.All_Data > 100000)]) / num_all_data * 100, 2)
    #         second_threshold_perc = round(len(df[(df.All_Data > 500000)]) / num_all_data * 100, 2)
    #         third_threshold_perc = round(len(df[(df.All_Data > 1000000)]) / num_all_data * 100, 2)
    #         fourth_threshold_perc = round(len(df[(df.All_Data > 1500000)]) / num_all_data * 100, 2)
    #         fifth_threshold_perc = round(len(df[(df.All_Data > 2000000)]) / num_all_data * 100, 2)
    #         print(year, month, first_threshold_perc, second_threshold_perc, third_threshold_perc, fourth_threshold_perc, fifth_threshold_perc)
    #
    #         # create columns for each threshold with the percentage and save to csv
    #         df['first_quart'] = df.All_Data
    #         df['second_quart'] = df.All_Data
    #         df['third_quart'] = df.All_Data
    #
    #         # calc third quartile values
    #         quart_1, quart_2, quart_3 = get_quartile(df.All_Data)
    #         df.loc[df.first_quart < quart_1, 'first_quart'] = np.nan
    #         df.loc[df.second_quart < quart_2, 'second_quart'] = np.nan
    #         df.loc[df.third_quart < quart_3, 'third_quart'] = np.nan
    #
    #         df.to_excel(writer, sheet_name=month)
    #     writer.save()
    #         # df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/QUARTILES_{year}-{month}.csv')



    # def get_data_stats(df, examp_longs, examp_lats):
    #     longs = df.Long
    #     lats = df.Lat
    #     energy = df.Energy_J
    #     plot_3vars_count = stats.binned_statistic_2d(longs, lats, energy, statistic=np.nanmean,
    #                                                  bins=[examp_longs, examp_lats])
    #     stats_data = plot_3vars_count.statistic
    #     return stats_data
    #
    #

    #
    #
    # def get_quartile(df_vals):
    #     quart_1 = np.percentile(df_vals, 25)
    #     quart_2 = np.percentile(df_vals, 50)
    #     quart_3 = np.percentile(df_vals, 75)
    #     return quart_1, quart_2, quart_3

    # def main():
    #     examp_longs, examp_lats = get_longs_lats_dataset()
    #     years = get_years_path()
    #     all_years_files = get_year_files_dict(years)
    #     all_years_dfs = get_year_df_dict(all_years_files)
    #     for year in all_years_dfs:
    #         months_dict = all_years_dfs[year]
    #         for month in months_dict:
    #             # create the df and the longs and total sum columns
    #             data = months_dict[month]
    #             stat_data = get_long_mean(data, examp_longs, examp_lats)
    #             df = pd.DataFrame({})
    #             df['Longs'] = examp_longs[0:-1]
    #             df['All_Data'] = stat_data
    #             # df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/{year}-{month}_1d.csv')
    #
    #             # calculate percentage of each threshold
    #             num_all_data = len(df)
    #             first_threshold_perc = len(df[(df.All_Data > 100000)]) / num_all_data * 100
    #             second_threshold_perc = len(df[(df.All_Data > 500000)]) / num_all_data * 100
    #             third_threshold_perc = len(df[(df.All_Data > 1000000)]) / num_all_data * 100
    #             fourth_threshold_perc = len(df[(df.All_Data > 1500000)]) / num_all_data * 100
    #             fifth_threshold_perc = len(df[(df.All_Data > 2000000)]) / num_all_data * 100
    #             # print(year, month, first_threshold_perc, second_threshold_perc, third_threshold_perc, fourth_threshold_perc, fifth_threshold_perc)
    #
    #             # create columns for each threshold with the percentage and save to csv
    #             df[f'first_threshold'] = df.All_Data
    #             df[f'second_threshold'] = df.All_Data
    #             df[f'third_threshold'] = df.All_Data
    #             df[f'fourth_threshold'] = df.All_Data
    #             df[f'fifth_threshold'] = df.All_Data
    #
    #             # calc third quartile values
    #             quart_1, quart_2, quart_3 = get_quartile(df.All_Data)
    #
    #             df.loc[df.first_threshold < 100000, 'first_threshold'] = np.nan
    #             df.loc[df.second_threshold < 500000, 'second_threshold'] = np.nan
    #             df.loc[df.third_threshold < 1000000, 'third_threshold'] = np.nan
    #             df.loc[df.fourth_threshold < 1500000, 'fourth_threshold'] = np.nan
    #             df.loc[df.fifth_threshold < 2000000, 'fifth_threshold'] = np.nan
    #
    #             # df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/{year}-{month}.csv')

    # # create df and columns for each threshold
    # df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/2009-10-Dec_1d.csv')
    # df = df.iloc[:, 1:]
    # df['first_threshold'] = df.Dec
    # df['second_threshold'] = df.Dec
    # df['third_threshold'] = df.Dec
    # df['fourth_threshold'] = df.Dec
    # df['fifth_threshold'] = df.Dec
    # df.loc[df.first_threshold < 100000, 'first_threshold'] = np.nan
    # df.loc[df.second_threshold < 500000, 'second_threshold'] = np.nan
    # df.loc[df.third_threshold < 1000000, 'third_threshold'] = np.nan
    # df.loc[df.fourth_threshold < 1500000, 'fourth_threshold'] = np.nan
    # df.loc[df.fifth_threshold < 2000000, 'fifth_threshold'] = np.nan
    # df.to_csv('D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/2009-10-Dec_1d_Summary.csv')

    # calculate percentage for each threshold
    # df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/2009-10-Dec_1d_Summary.csv')
    # first_threshold = len(df[(df.Dec > 500000)])
    # second_threshold = len(df[(df.Dec > 1000000)])
    # third_threshold = len(df[(df.Dec > 1500000)])
    # total_lines = len(df)
    # first_threshold_perc = round(first_threshold / total_lines * 100, 2)
    # second_threshold_perc = round(second_threshold / total_lines * 100, 2)
    # third_threshold_perc = round(third_threshold / total_lines * 100, 2)
    # print(first_threshold_perc, second_threshold_perc, third_threshold_perc)


    #         # df = pd.DataFrame(stat_data)

    #         # imshow = plt.imshow(df, origin='lower', cmap='YlOrRd')
    #         # imshow.set_clim(vmin=100, vmax=10000)
    #         # plt.show()
    #         # df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/{year}-{month}_MATRIX.csv')
    #

    # df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/2009-10-Dec_MATRIX.csv')
    # # mean_list = []
    # # for col in df:
    # #     col_values = df[col].tolist()
    # #     mean_val = np.nanmean(col_values)
    # #     mean_list.append(mean_val)
    # # mean_df = pd.DataFrame({})
    # # mean_df['longs'] = list(df.columns)
    # # mean_df['Mean'] = mean_list
    # # mean_df.to_csv('D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/2009-10-Dec_MEAN.csv')
    # df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/2009-10-Dec_MATRIX.csv')



    # examp_longs, examp_lats = get_longs_lats_dataset()
    # years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    # main_dir = 'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/raw_data/'
    # input_files_path = f'{main_dir}/files/'
    # files = os.listdir(input_files_path)
    #
    # for year in years:
    #     year_df = pd.DataFrame({})
    #     file_list = [i for i in files if year in i]
    #     file_list = sorted(file_list)
    #
    #     for file in file_list:
    #         month = file[8:11]
    #         full_path = os.path.join(input_files_path, file)
    #         df = pd.read_csv(full_path)
    #         df = df.iloc[:, 1:]
    #         df = df.replace(0, np.nan)
    #         df.sort_values('Long')
    #         print(df)
    #         # get statistics for df
    #         stat_data = get_long_mean(df, examp_longs)
    #         # plt.scatter(examp_longs[0:-1], stat_data)
    #         # plt.show()
    #         year_df['Longs'] = examp_longs[0:-1]
    #         year_df[month] = stat_data
    #
    #     output_path = main_dir + 'Summary/' + f'{year}.csv'
    #     year_df.to_csv(output_path)



    # # get a dict where each year is a key that contains the monthly df
    # years = get_years_path()
    # all_years_files = get_year_files_dict(years)
    # all_years_dfs = get_year_df_dict(all_years_files)
    #
    # # get the lightning count for each grid box in the given grid
    # examp_longs, examp_lats = get_longs_lats_dataset()
    #
    # for year in all_years_dfs:
    #     months_dict = all_years_dfs[year]
    #     for month in months_dict:
    #         data = months_dict[month]
    #         data.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/{year}-{month}.csv')
    #         stats_data = get_data_stats(data, examp_longs, examp_lats)
    #         df = pd.DataFrame(stats_data)
    #         df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/{year}-{month}-matrix.csv')

            # df['Mean'] = df.mean(axis=1, skipna= True)
            # mean_values = df.Mean.to_list()
            # year_df['Longs'] = examp_longs[0:-1]
            # year_df[month] = mean_values
            # output_path = main_dir + 'Summary/' + f'{year}.csv'
            # year_df.to_csv(output_path)


    # for file in file_list:
    #     month = file[8:11]
    #     print(file, month)
    #     full_path = os.path.join(main_dir, file)
    #     df = pd.read_csv(full_path)
    #         df = df.iloc[:, 1:]
    #         df = df.replace(0, np.nan)
    #         df['Mean'] = df.mean(axis=1, skipna= True)
    #         mean_values = df.Mean.to_list()
    #         year_df['Longs'] = examp_longs[0:-1]
    #         year_df[month] = mean_values
    #     output_path = main_dir + 'Summary/' + f'{year}.csv'
    #     year_df.to_csv(output_path)


    # dec_df = pd.DataFrame({})
    # dec_df['Longs'] = examp_longs[0:-1]
    # dec_df['Average Frequency'] = mean_values
    # dec_df.to_csv('D:/WWLLN/Summary Graphs/all_med_sea_data_freq/2010-Dec-summary.csv')


    # df = pd.read_csv('D:/WWLLN/Summary Graphs/all_med_sea_data_freq/2010-Dec-matrix.csv')
    # df = df.iloc[:, 1:]
    # df['Mean'] = df.mean(axis=1)
    # mean_values = df.Mean.to_list()
    #
    # dec_df = pd.DataFrame({})
    # dec_df['Longs'] = examp_longs[0:-1]
    # dec_df['Average Frequency'] = mean_values
    # dec_df.to_csv('D:/WWLLN/Summary Graphs/all_med_sea_data_freq/2010-Dec-summary.csv')



    # examp_longs, examp_lats = get_longs_lats_dataset()
    #
    #
    # years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    # main_dir = 'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/raw_data/'
    # files = os.listdir(main_dir)
    #
    # for year in years:
    #     year_df = pd.DataFrame({})
    #     file_list = [i for i in files if year in i]
    #     file_list = sorted(file_list)
    #
    #     long_list = []
    #     energy_list = []
    #     for file in file_list:
    #         full_path = os.path.join(main_dir, file)
    #         df = pd.read_csv(full_path)
    #         df = df.iloc[:, 1:]
    #         longs = df.Long.tolist()
    #         energy = df.Energy_J.tolist()
    #         long_list = long_list + longs
    #         energy_list = energy_list + energy
    #
    #     df = pd.DataFrame({})
    #     df['Longs'] = long_list
    #     df['Energy'] = energy_list
    #     df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/raw_data/merged_months/{year}.csv')