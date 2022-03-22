import pandas as pd
import os
import xarray as xr
from shapely import geometry
import scipy.stats as stats
import math
import numpy as np
import seaborn as sns
import scipy as sp
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from scipy.stats import norm


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
        # if year != 'D:/WWLLN-Intensity/DJF2020-21':
        if year == 'D:/WWLLN-Intensity/DJF2009-10':
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


def get_long_sum(df, examp_longs):
    longs = df.Long
    energy = df.Energy_J
    hist = stats.binned_statistic(longs, energy, statistic=np.nansum, bins=examp_longs)
    # hist = stats.binned_statistic_2d(longs, lats, energy, statistic= np.nanmean, bins=[examp_longs, examp_lats])
    stats_data = hist.statistic
    x = hist.bin_edges[:-1]
    return stats_data, x


def get_long_kde(df, examp_longs):
    df2 = df.groupby('Long').sum()
    energy = df2.Energy_J
    print(df2)
    # sns.kdeplot(df.Long, df.Energy_J)
    # plt.show()


def main():
    examp_longs, examp_lats = get_longs_lats_dataset()
    years = get_years_path()
    all_years_files = get_year_files_dict(years)
    all_years_dfs = get_year_df_dict(all_years_files)

    for year in all_years_dfs:
        months = all_years_dfs[year]
        for month in months:
            month_df = months[month]
            stats_data, x = get_long_sum(month_df, examp_longs)



            # stat_df = pd.DataFrame({})
            # stat_df['longs'] = x
            # stat_df['stats'] = stats_data
            # sns.kdeplot(stat_df)
            # plt.show()
            # plt.bar(x, stats_data)
            # plt.show()









            # sns.jointplot(data=month_df.Energy_J, x=month_df.Long, y=month_df.Energy_J, kind='hist')
            # plt.show()
            # stats_data, x = get_long_sum(month_df, examp_longs)
            # plt.bar(x, stats_data)
            # sns.histplot(data=month_df.Energy_J, x=month_df.Long, stat="density", kde=True, common_norm=False)
            # sns.jointplot(data=month_df.Energy_J, x=month_df.Long, y=month_df.Energy_J)
            # plt.show()
            # stats_data, x = get_long_sum(month_df, examp_longs)
            # sns.histplot(x=month_df.Long, y=month_df.Energy_J)
            # sns.histplot(data=month_df, x="Long", kde=True)

            # sns.kdeplot(stats_data)
            # sns.distplot(stats_data, hist=False, rug=True,
            #              axlabel="Longs",
            #              kde_kws=dict(label="kde"),
            #              rug_kws=dict(height=.2, linewidth=2, color="C1", label="data"))
            # plt.bar(x, stats_data)
            # plt.show()


if __name__ == '__main__':
    main()














































# def get_long_lat_index(long_bins, lat_bins, long_points, lat_points):
#     long_index = []
#     lat_index = []
#
#     for long in long_points:
#         index = long_bins.index(long)
#         long_index.append(index)
#     for lat in lat_points:
#         index = lat_bins.index(lat)
#         lat_index.append(index)
#
#     return long_index, lat_index
#
#
# def get_intensity_by_index(df, long_index, lat_index, long_bins, lat_bins):
#     data = []
#     for long, lat in zip(long_index, lat_index):
#         # lat = str(lat)
#         intensity_val = df[lat][long]
#         data.append(intensity_val)
#
#     longs = []
#     lats = []
#
#     for index in long_index:
#         val = long_bins[index]
#         longs.append(val)
#     for index in lat_index:
#         val = lat_bins[index]
#         lats.append(val)
#
#     df = pd.DataFrame({})
#     df['longs'] = longs
#     df['lats'] = lats
#     df['Intensity'] = data
#     return df