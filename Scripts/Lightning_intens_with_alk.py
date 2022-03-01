import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely import geometry
import math
import os
import scipy.io
from scipy.stats import binned_statistic_2d


# def get_years_path():
#     main_dir_path = 'D:/WWLLN-Intensity'
#     years = []
#     for item in os.listdir(main_dir_path):
#         full_path = os.path.join(main_dir_path, item)
#         if os.path.isdir(full_path) == True and item[0:3] == 'DJF':
#             full_path = full_path.replace('\\', '/')
#             years.append(full_path)
#     years.sort()
#     return years
#
#
# def get_all_files(dir_path):
#     # This function receives a path and returns a list of all existing files in that path.
#     all_files = os.listdir(dir_path)
#     loc_files = []
#     for file in all_files:
#         fullPath = os.path.join(dir_path, file)
#         fullPath = fullPath.replace('\\', '/')
#         if file.find('.loc') != -1 and file[0:2] != '._':
#             loc_files.append(fullPath)
#         else:
#             pass
#     return loc_files
#
#
# def get_year_files_dict(year_paths):
#     all_files = {}
#     for year in year_paths:
#         year_name = year[-7:]
#         if year != 'D:/WWLLN-Intensity/DJF2020-21':
#             dec_files = []
#             jan_files = []
#             feb_files = []
#             files_folder = os.path.join(year,'loc_files')
#             files_folder = files_folder.replace('\\', '/')
#             files = get_all_files(files_folder)
#             for file in files:
#                 if file[-8:-6] == '12':
#                     dec_files.append(file)
#                 if file[-8:-6] == '01':
#                     jan_files.append(file)
#                 if file[-8:-6] == '02':
#                     feb_files.append(file)
#             all_files[year_name] = {'Dec': dec_files, 'Jan': jan_files, 'Feb': feb_files}
#     return all_files
#
#
# def get_year_df_dict(all_files):
#     all_years_df = {}
#     for year in all_files:
#         months = list(all_files[year].keys())
#         months_df = {}
#         for month in months:
#             files = all_files[year][month]
#             fields = ['Date', 'Long', 'Lat', 'Energy_J']
#             data = []
#             for file in files:
#                 df = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nstn', 'Energy_J', 'Energy_Uncertainty', 'Nstn_Energy'], usecols=fields)
#                 df = df[(df.Long > -6) & (df.Long < 36)]
#                 df = df[(df.Lat > 30) & (df.Lat < 46)]
#                 for date, long, lat, energy in zip(df.Date, df.Long, df.Lat, df.Energy_J):
#                     data.append([date, long, lat, energy])
#             month_df = pd.DataFrame(data, columns=fields)
#             month_df.drop_duplicates(['Date', 'Long', 'Lat', 'Energy_J'], keep='first', inplace=True)
#             months_df[month] = month_df
#         all_years_df[year] = months_df
#
#     return all_years_df


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


def get_points_inside_med(monthly_df_dict):
    med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly = get_all_polygons()

    all_years_points = {}
    for year in list(monthly_df_dict.keys()):
        months = monthly_df_dict[year]
        months_points = {}
        for month in list(months.keys()):
            month_df = months[month]
            month_data = []
            for long, lat, energy in zip(month_df.Long, month_df.Lat, month_df.Energy_J):
                point = geometry.Point(long, lat)
                if med_poly.contains(point):
                    if majorca_poly.contains(point) is False and corsica_poly.contains(point) is False and sardinia_poly.contains(point) is False and sicily_poly.contains(point) is False and peleponnese_poly.contains(point) is False and crete_poly.contains(point) is False and cyprus_poly.contains(point) is False and rhodes_poly.contains(point) is False and kios_lesbos_poly.contains(point) is False:
                        data = (long, lat, energy)
                        month_data.append(data)
            months_points[month] = month_data
        print(f'finished {year}')
        all_years_points[year] = months_points
    return all_years_points


def get_3vars_plot_per_month(month_data, long_points_med, lat_points_med):
    longs = []
    lats = []
    energies = []
    for tup in month_data:
        long = tup[0]
        lat = tup[1]
        energy = tup[2]
        longs.append(long)
        lats.append(lat)
        energies.append(energy)

    long_bins = np.arange(min(long_points_med), max(long_points_med), 0.09).tolist()
    lat_bins = np.arange(min(lat_points_med), max(lat_points_med), 0.09).tolist()

    plot_3vars_sum = binned_statistic_2d(longs, lats, energies, statistic= 'sum', bins=[long_bins, lat_bins])
    plot_3vars_mean = binned_statistic_2d(longs, lats, energies, statistic= np.nanmean, bins=[long_bins, lat_bins])
    return plot_3vars_sum, plot_3vars_mean, longs, lats, energies, long_bins, lat_bins


def get_energy_plot_mean(year, all_years_points):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    array_list = []
    dec_array = []
    jan_array = []
    feb_array = []

    for month in list(all_years_points[year]):
        data = all_years_points[year][month]
        plot_3vars_sum, plot_3vars_mean, longs, lats, energies, long_bins, lat_bins = get_3vars_plot_per_month(data, long_points_med, lat_points_med)

        if month == 'Dec':
            mean_array = np.nan_to_num(plot_3vars_mean.statistic)
            dec_array.append(mean_array)
            array_list.append(mean_array)

        if month == 'Jan':
            mean_array = np.nan_to_num(plot_3vars_mean.statistic)
            jan_array.append(mean_array)
            array_list.append(mean_array)

        if month == 'Feb':
            mean_array = np.nan_to_num(plot_3vars_mean.statistic)
            feb_array.append(mean_array)
            array_list.append(mean_array)

    total_mean_array = np.mean(array_list, axis=0)

    return dec_array, jan_array, feb_array, total_mean_array


def get_energy_plot_mean_total(total_mean, ax):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    cmap = cm.get_cmap('YlOrRd')
    # cmap = cm.get_cmap('gray')
    # ax.plot(long_points_med, lat_points_med, color='k')
    #
    # for island in islands_dict:
    #     coords = islands_dict[island]
    #     longs_island = coords[0]
    #     lats_island = coords[1]
    #     ax.plot(longs_island, lats_island, color='k')

    total_mean[total_mean == 0] = np.nan
    imshow_mean_total = ax.imshow(total_mean.T, origin='lower', cmap=cmap, alpha=0.3,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_total.set_clim(vmin=100, vmax=10000)
    # cb1 = plt.colorbar(imshow_mean_total, shrink=0.5)

    # cb = fig.colorbar(imshow_mean_total, ax=ax, shrink=0.6)
    # cb.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    # fig.suptitle(f'Lightnings Intensity Mean (Joule) for 2009-2020', fontsize=20)


def main():
    total_mean_file = 'D:/WWLLN-Intensity/Validation CSV/total_mean/total_total_mean.csv'
    total_mean = pd.read_csv(total_mean_file)
    total_mean = total_mean.to_numpy()
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
    lat_list = alk_ds.latitude.data.tolist()
    long_list = alk_ds.longitude.data.tolist()

    # cmap = cm.get_cmap('winter')
    cmap = cm.get_cmap('viridis')
    # cmap.set_under('w')
    # alk_plot = plt.pcolormesh(long_list, lat_list, mean_array[0], alpha= 1, cmap= cmap, shading='gouraud', zorder=0)

    levels = np.linspace(2, 3, 30)
    alk_plot = plt.contour(long_list, lat_list, mean_array[0], alpha= 1, cmap= cmap, levels=levels, shading='gouraud', zorder=75, linewidths= 4)
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    plt.plot(long_points_med, lat_points_med, color='k', zorder=100)
    for island in islands_dict:
        coords = islands_dict[island]
        longs_island = coords[0]
        lats_island = coords[1]
        plt.plot(longs_island, lats_island, color='k', zorder=100)
    # plt.clabel(alk_plot, inline=True, fontsize=5)
    ax = plt.gca()
    get_energy_plot_mean_total(total_mean, ax)

    ax.set_xlim([-7, 37])
    ax.set_ylim([29, 47])
    plt.clim(2.4, 2.8)
    # cb2 = plt.colorbar(alk_plot, shrink=0.5)
    # cb2.set_label('Mol * m^-3', fontsize=14, rotation=90, labelpad=20)
    plt.title('Mean Alklanity for 2009-2020 DJF\n', fontsize=24, color='darkred')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()




   # years = get_years_path()
    # all_years_files = get_year_files_dict(years)
    # all_years_dfs = get_year_df_dict(all_years_files)
    # all_years_points = get_points_inside_med(all_years_dfs)
    # dec_array_mean = []
    # jan_array_mean = []
    # feb_array_mean = []
    # total_array_mean = []

    # for year in list(all_years_points.keys()):
    #     dec_array, jan_array, feb_array, total_array = get_energy_plot_mean(year, all_years_points)
    #     dec_array_mean.append(dec_array)
    #     jan_array_mean.append(jan_array)
    #     feb_array_mean.append(feb_array)
    #     total_array_mean.append(total_array)
    #     print(f'finished statistics for {year}')



# def main():
#     nc_file = 'D:/WWLLN-Intensity/Validation CSV/alk.nc'
#     alk_ds = xr.open_dataset(nc_file)
#     times = alk_ds.time.to_pandas()
#     pandas_times = alk_ds.time.to_pandas()
#     array_list = []
#     for i in pandas_times:
#         file_name = str(i.year) + '-' + str(i.month)
#         if i.month in [1, 2, 3]:
#             ptimes_list = pandas_times.to_list()
#             index = ptimes_list.index(i)
#             alk_stime = alk_ds.talk.isel(time=index)
#             np_arr = alk_stime.to_numpy()
#             np_arr = np.nan_to_num(np_arr, nan=0)
#             df = pd.DataFrame(np_arr[0])
#
#             df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/{file_name}.csv')
#             array_list.append(np_arr)
#     mean_array = np.mean(array_list, axis=0)
#     df = pd.DataFrame(mean_array[0])
#     df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/mean.csv')
#     lat_list = alk_ds.latitude.data.tolist()
#     long_list = alk_ds.longitude.data.tolist()
#
#     fig = plt.figure(figsize=(12, 6))
#     cmap = cm.get_cmap('rainbow')
#     cmap.set_under('w')
#     plt.pcolormesh(long_list, lat_list, mean_array[0], cmap=cmap, shading='gouraud')
#     plt.clim(2.4, 2.8)
#     cb = plt.colorbar()
#     cb.set_label('Mol * m^-3', fontsize=14, rotation=90, labelpad=30)
#     plt.title('Mean Alklanity for 2009-2020 DJF\n', fontsize=24, color='darkred')
#     plt.show()
#
