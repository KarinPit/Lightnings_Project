import pandas as pd
import os
import xarray as xr
from shapely import geometry
import math
import numpy as np
import scipy.stats as stats
from statistics import median
import matplotlib.pyplot as plt
import matplotlib.cm as cm


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
        # if year == 'D:/WWLLN-Intensity/DJF2014-15':
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
                df = df[(df.Long > 32) & (df.Long < 36.3)]
                df = df[(df.Lat > 30.18) & (df.Lat < 45.98)]
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


def get_stats(df):
    stat_list = ['sum', 'mean', 'median']
    stats_sum = None
    stats_mean = None
    stats_median = None
    x = None
    y = None

    for stat in stat_list:
        if stat == 'sum':
            hist = stats.binned_statistic_2d(df.Long, df.Lat, df.Energy_J, statistic=np.nansum, bins=[48, 176])
            stats_sum = hist.statistic
            x = hist.x_edge
            y = hist.y_edge
        if stat == 'mean':
            hist = stats.binned_statistic_2d(df.Long, df.Lat, df.Energy_J, statistic=np.nanmean, bins=[48, 176])
            stats_mean = hist.statistic
        if stat == 'median':
            hist = stats.binned_statistic_2d(df.Long, df.Lat, df.Energy_J, statistic=np.nanmedian, bins=[48, 176])
            stats_median = hist.statistic
    return stats_sum, stats_mean, stats_median, x, y


def main():
            years = get_years_path()
            all_years_files = get_year_files_dict(years)
            yearly_df_dict = get_year_df_dict(all_years_files)
            writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/Sum_intens_yearly.xlsx',engine='xlsxwriter')

            for year in yearly_df_dict:
                df = pd.DataFrame({})
                longs = []
                lats = []
                energy = []

                months = yearly_df_dict[year]
                for month in months:
                    month_data = months[month]
                    long = month_data['Long'].tolist()
                    lat = month_data['Lat'].tolist()
                    energy_J = month_data['Energy_J'].tolist()
                    longs.append(long)
                    lats.append(lat)
                    energy.append(energy_J)

                df['Long'] = longs[0]
                df['Lat'] = lats[0]
                df['Energy_J'] = energy[0]
                df = df.replace(to_replace=0, value=np.nan)
                hist = stats.binned_statistic_2d(df.Long, df.Lat, df.Energy_J, statistic=np.nansum, bins=[48, 176])
                stats_data = hist.statistic
                x = hist.x_edge
                y = hist.y_edge
                df = pd.DataFrame(stats_data)

                longs_index = [i for i in range(48)]
                longs = []
                lats = []
                energy = []

                for lat in df:
                    lat_index = int(lat)
                    lat_val = round(y[lat_index], 2)
                    lat_column = df[lat]
                    for int_val in lat_column:
                        energy.append(int_val)
                        lats.append(lat_val)
                    for long_index in longs_index:
                        long_val = round(x[long_index], 2)
                        longs.append(long_val)

                df = pd.DataFrame({})
                df['Long'] = longs
                df['Lat'] = lats
                df['Energy_J'] = energy
                df['Sum_above_10K'] = energy
                df = df.replace(to_replace=0, value=np.nan)
                df.loc[df.Sum_above_10K < 100000, 'Sum_above_10K'] = np.nan
                sum_energy = np.nansum(df.Sum_above_10K)
                print(sum_energy)
                df.to_excel(writer, sheet_name=year)
            writer.save()


























        # def main():
        #     years = get_years_path()
        #     all_years_files = get_year_files_dict(years)
        #     yearly_df_dict = get_year_df_dict(all_years_files)
        #     # writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/MEDIAN_Intens.xlsx',engine='xlsxwriter')
        #
        #     for year in yearly_df_dict:
        #         df = pd.DataFrame({})
        #         longs = []
        #         lats = []
        #         energy = []
        #
        #         months = yearly_df_dict[year]
        #         for month in months:
        #             month_data = months[month]
        #             long = month_data['Long'].tolist()
        #             lat = month_data['Lat'].tolist()
        #             energy_J = month_data['Energy_J'].tolist()
        #             longs.append(long)
        #             lats.append(lat)
        #             energy.append(energy_J)
        #
        #         df['Long'] = longs[0]
        #         df['Lat'] = lats[0]
        #         df['Energy_J'] = energy[0]
        #         df = df.replace(to_replace=0, value=np.nan)
        #         hist = stats.binned_statistic_2d(df.Long, df.Lat, df.Energy_J, statistic=np.nansum, bins=[48, 176])
        #         stats_data = hist.statistic
        #         x = hist.x_edge
        #         y = hist.y_edge
        #         df = pd.DataFrame(stats_data)
        #
        #         longs_index = [i for i in range(48)]
        #         longs = []
        #         lats = []
        #         energy = []
        #
        #         for lat in df:
        #             lat_index = int(lat)
        #             lat_val = round(y[lat_index], 2)
        #             lat_column = df[lat]
        #             for int_val in lat_column:
        #                 energy.append(int_val)
        #                 lats.append(lat_val)
        #             for long_index in longs_index:
        #                 long_val = round(x[long_index], 2)
        #                 longs.append(long_val)
        #
        #         df = pd.DataFrame({})
        #         df['Long'] = longs
        #         df['Lat'] = lats
        #         df['Energy_J'] = energy
        #         df = df.replace(to_replace=0, value=np.nan)
        #         print(df)

        # df_stat = pd.DataFrame({})
        # df_stat['Long'] = x[:-1]
        # df_stat['Sum'] = stats_data
        # df_stat['Sum_above_10K'] = stats_data
        # df_stat.loc[df_stat.Sum_above_10K < 10000, 'Sum_above_10K'] = np.nan
        # print(df_stat)

        # cmap = cm.get_cmap('YlOrRd')
        # cmap.set_under('w')
        # imshow = plt.imshow(stats_data, origin='lower', cmap=cmap, extent=[32, 36.3, 30.18, 45.98])
        # imshow.set_clim(vmin=10000, vmax=100000)
        # plt.colorbar()
        # plt.show()


        # ax3.set_xlim(xmin=-7, xmax=37)
        # ax3.set_ylim(ymin=28, ymax=47)
        # imshow_sum.set_clim(vmin=100, vmax=100000)
        # year_min = np.nanmin(df.Energy_J)
        # year_max = np.nanmax(df.Energy_J)
        # year_sum = round(np.nansum(df.Energy_J), 2)
        # year_mean = round(np.nanmean(df.Energy_J), 2)
        # year_median = round(np.nanmedian(df.Energy_J), 2)
        #
        # print(f'Year min {year_min}', f'Year max {year_max}' ,f'Year Sum {year_sum}', f'Year Mean {year_mean}', f'Year Median {year_median}')


            # cmap = cm.get_cmap('YlOrRd')
            # cmap.set_under('w')
            # plt.scatter(longs, lats, c= energy, cmap=cmap)
            # plt.clim(100000, 500000)
            # plt.colorbar()
            # plt.title(month)
            # plt.show()


if __name__ == '__main__':
    main()







    # def main():
    #     years = get_years_path()
    #     all_years_files = get_year_files_dict(years)
    #     yearly_df_dict = get_year_df_dict(all_years_files)
    #     # writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/MEDIAN_Intens.xlsx',engine='xlsxwriter')
    #
    #     for year in yearly_df_dict:
    #         df = pd.DataFrame({})
    #         longs = []
    #         lats = []
    #         energy = []
    #
    #         months = yearly_df_dict[year]
    #         for month in months:
    #             month_data = months[month]
    #             long = month_data['Long'].tolist()
    #             lat = month_data['Lat'].tolist()
    #             energy_J = month_data['Energy_J'].tolist()
    #             longs.append(long)
    #             lats.append(lat)
    #             energy.append(energy_J)
    #
    #         df['Long'] = longs[0]
    #         df['Lat'] = lats[0]
    #         df['Energy_J'] = energy[0]
    #         df = df.replace(to_replace=0, value=np.nan)
    #         stats_sum, stats_mean, stats_median, x, y = get_stats(df)
    #
    #         df_sum = pd.DataFrame(stats_sum)
    #         df_mean = pd.DataFrame(stats_mean)
    #         df_med = pd.DataFrame(stats_median)
    #         longs_index = [i for i in range(48)]
    #
    #         # info for sum
    #         longs_sum = []
    #         lats_sum = []
    #         energy_sum = []
    #
    #         for lat in df_sum:
    #             lat_index = int(lat)
    #             lat_val = round(y[lat_index], 2)
    #             lat_column = df.iloc[lat]
    #             print(lat_column)
    #             for int_val in lat_column:
    #                 energy_sum.append(int_val)
    #                 lats_sum.append(lat_val)
    #             for long_index in longs_index:
    #                 long_val = round(x[long_index], 2)
    #                 longs_sum.append(long_val)
    #
    #         # info for mean
    #         longs_mean = []
    #         lats_mean = []
    #         energy_mean = []
    #
    #         for lat in df_mean:
    #             lat_index = int(lat)
    #             lat_val = round(y[lat_index], 2)
    #             lat_column = df.iloc[lat]
    #             for int_val in lat_column:
    #                 energy_mean.append(int_val)
    #                 lats_mean.append(lat_val)
    #             for long_index in longs_index:
    #                 long_val = round(x[long_index], 2)
    #                 longs_mean.append(long_val)
    #
    #         # info for med
    #         longs_med = []
    #         lats_med = []
    #         energy_med = []
    #
    #         for lat in df_med:
    #             lat_index = int(lat)
    #             lat_val = round(y[lat_index], 2)
    #             lat_column = df.iloc[lat]
    #             for int_val in lat_column:
    #                 energy_med.append(int_val)
    #                 lats_med.append(lat_val)
    #             for long_index in longs_index:
    #                 long_val = round(x[long_index], 2)
    #                 longs_med.append(long_val)

            # df = pd.DataFrame({})
            # df['Long'] = longs_sum
            # df['Lat'] = lats_sum
            # df['Energy_Sum'] = energy_sum
            # df['Energy_Mean'] = energy_mean
            # df['Energy_Median'] = energy_med
            # df = df.replace(to_replace=0, value=np.nan)
            # print(df)














    # for year in yearly_df_dict:
    #     df = pd.DataFrame({})
    #     months = yearly_df_dict[year]
    #     for month in months:
    #         month_data = months[month]
    #         # month_data = month_data.replace(to_replace=0, value=np.nan)
    #         longs = month_data['Long']
    #         lats = month_data['Lat']
    #         energy = month_data['Energy_J']
    #         month_data.loc[month_data.Energy_J < 1000000, 'Energy_J'] = np.nan
    #         med_energy = np.nanmedian(energy)
    #         df[f'{month}_Median'] = [med_energy]
    #         print(month, np.nanmin(energy), np.nanmax(energy), med_energy)
    #     df.to_excel(writer, sheet_name=year)
    # writer.save()

    # writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/All_Data_Intens.xlsx', engine='xlsxwriter')

    # for year in yearly_df_dict:
    #     df = pd.DataFrame({})
    #     months_dict = yearly_df_dict[year]
    #     for month in months_dict:
    #         month_data = months_dict[month]
    #         count = len(month_data)
    #         area_size = 837088.74  # squared km
    #         average_count = count / area_size
    #         sum_intens = month_data['Energy_J'].sum()
    #         mean_intens = month_data['Energy_J'].mean()
    #         df[f'{month}_Count'] = [count]
    #         df[f'{month}_Avg_Count'] = [average_count]
    #         df[f'{month}_Sum_Intensity'] = [sum_intens]
    #         df[f'{month}_Mean_Intensity'] = [mean_intens]
    #
    #     df.to_excel(writer, sheet_name=year)
    # writer.save()


    # years = get_years_path()
    # all_years_files = get_year_files_dict(years)
    # yearly_df_dict = get_year_df_dict(all_years_files)
    #
    # for year in yearly_df_dict:
    #     months = yearly_df_dict[year]
    #     for month in months:
    #         month_data = months[month]
    #         longs = month_data['Long']
    #         lats = month_data['Lat']
    #         energy = month_data['Energy_J']
    #         med_energy = median(energy)
    #         print(month, min(energy), max(energy), med_energy)
    #         # cmap = cm.get_cmap('YlOrRd')
    #         # cmap.set_under('w')
    #         # plt.scatter(longs, lats, c= energy, cmap=cmap)
    #         # plt.clim(100000, 500000)
    #         # plt.colorbar()
    #         # plt.title(month)
    #         # plt.show()
