import pandas as pd
from shapely import geometry
import math
import os
import scipy.io
from scipy.stats import binned_statistic_2d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pygrib

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
    all_years_df = {}
    for year in all_files:
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
                    data.append([date, long, lat, energy])
            month_df = pd.DataFrame(data, columns=fields)
            month_df.drop_duplicates(['Date', 'Long', 'Lat', 'Energy_J'], keep='first', inplace=True)
            months_df[month] = month_df
        all_years_df[year] = months_df

    return all_years_df


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


def read_mat_files():
    mat = scipy.io.loadmat('D:/WWLLN-Intensity/DJF2020-21/AE20220118.mat')
    data = mat['data']
    df = pd.DataFrame(data)


def get_energy_plot_sum_single(year, all_years_points):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    total_longs = []
    total_lats = []
    total_energies = []

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]
    cmap = cm.get_cmap('YlOrRd')
    cmap.set_under('w')

    for island in islands_dict:
        coords = islands_dict[island]
        longs_island = coords[0]
        lats_island = coords[1]
        ax0.plot(longs_island, lats_island, color='k')
        ax1.plot(longs_island, lats_island, color='k')
        ax2.plot(longs_island, lats_island, color='k')
        ax3.plot(longs_island, lats_island, color='k')

    for month in list(all_years_points[year]):
        data = all_years_points[year][month]
        plot_3vars_sum, plot_3vars_mean, longs, lats, energies, long_bins, lat_bins = get_3vars_plot_per_month(data, long_points_med, lat_points_med)
        total_longs += longs
        total_lats += lats
        total_energies += energies

        if month == 'Dec':
            imshow_sum = ax0.imshow(plot_3vars_sum.statistic.T, origin='lower', cmap=cmap,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
            ax0.set_xlim(xmin=-7, xmax=37)
            ax0.set_ylim(ymin=28, ymax=47)
            ax0.plot(long_points_med, lat_points_med, color='k')
            imshow_sum.set_clim(vmin=100, vmax=100000)
            ax0.set_title(month, fontsize=20, color='darkred')

        if month == 'Jan':
            imshow_sum = ax1.imshow(plot_3vars_sum.statistic.T, origin='lower', cmap=cmap,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
            ax1.set_xlim(xmin=-7, xmax=37)
            ax1.set_ylim(ymin=28, ymax=47)
            ax1.plot(long_points_med, lat_points_med, color='k')
            imshow_sum.set_clim(vmin=100, vmax=100000)
            ax1.set_title(month, fontsize=20, color='darkred')

        if month == 'Feb':
            imshow_sum = ax2.imshow(plot_3vars_sum.statistic.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
            ax2.set_xlim(xmin=-7, xmax=37)
            ax2.set_ylim(ymin=28, ymax=47)
            ax2.plot(long_points_med, lat_points_med, color='k')
            imshow_sum.set_clim(vmin=100, vmax=100000)
            ax2.set_title(month, fontsize=20, color='darkred')

    long_bins = np.arange(min(long_points_med), max(long_points_med), 0.09).tolist()
    lat_bins = np.arange(min(lat_points_med), max(lat_points_med), 0.09).tolist()
    ax3.plot(long_points_med, lat_points_med, color='k')
    plot_3vars_sum = binned_statistic_2d(total_longs, total_lats, total_energies, statistic= 'sum', bins=[long_bins, lat_bins])
    imshow_sum = ax3.imshow(plot_3vars_sum.statistic.T, origin='lower', cmap=cmap,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    ax3.set_xlim(xmin=-7, xmax=37)
    ax3.set_ylim(ymin=28, ymax=47)
    imshow_sum.set_clim(vmin=100, vmax=100000)
    ax3.set_title('Total', fontsize=20, color='darkred')

    cb = fig.colorbar(imshow_sum, ax=axes, shrink=0.6)
    cb.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    fig.suptitle(f'Lightnings Intensity Sum (Joule) for {year}', fontsize=20)
    plt.show()


def get_energy_plot_mean_single(year, all_years_points):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    array_list = []

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]
    cmap = cm.get_cmap('YlOrRd')
    cmap.set_under('w')

    for island in islands_dict:
        coords = islands_dict[island]
        longs_island = coords[0]
        lats_island = coords[1]
        ax0.plot(longs_island, lats_island, color='k')
        ax1.plot(longs_island, lats_island, color='k')
        ax2.plot(longs_island, lats_island, color='k')
        ax3.plot(longs_island, lats_island, color='k')

    for month in list(all_years_points[year]):
        data = all_years_points[year][month]
        plot_3vars_sum, plot_3vars_mean, longs, lats, energies, long_bins, lat_bins = get_3vars_plot_per_month(data, long_points_med, lat_points_med)

        if month == 'Dec':
            imshow_mean = ax0.imshow(plot_3vars_mean.statistic.T, origin='lower', cmap=cmap,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
            ax0.plot(long_points_med, lat_points_med, color='k')
            ax0.set_xlim(xmin=-7, xmax=37)
            ax0.set_ylim(ymin=28, ymax=47)
            imshow_mean.set_clim(vmin=100, vmax=10000)
            ax0.set_title(month, fontsize=20, color='darkred')

            mean_array = np.nan_to_num(plot_3vars_mean.statistic)
            array_list.append(mean_array)
            df_t = pd.DataFrame(mean_array)
            df_t.to_csv(f'D:/WWLLN-Intensity/karin/{year}_december_mean.csv')

        if month == 'Jan':
            imshow_mean = ax1.imshow(plot_3vars_mean.statistic.T, origin='lower', cmap=cmap,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
            ax1.plot(long_points_med, lat_points_med, color='k')
            ax1.set_xlim(xmin=-7, xmax=37)
            ax1.set_ylim(ymin=28, ymax=47)
            imshow_mean.set_clim(vmin=100, vmax=10000)
            ax1.set_title(month, fontsize=20, color='darkred')

            mean_array = np.nan_to_num(plot_3vars_mean.statistic)
            array_list.append(mean_array)
            df_t = pd.DataFrame(mean_array)
            df_t.to_csv(f'D:/WWLLN-Intensity/karin/{year}_january_mean.csv')

        if month == 'Feb':
            imshow_mean = ax2.imshow(plot_3vars_mean.statistic.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
            ax2.plot(long_points_med, lat_points_med, color='k')
            ax2.set_xlim(xmin=-7, xmax=37)
            ax2.set_ylim(ymin=28, ymax=47)
            imshow_mean.set_clim(vmin=100, vmax=10000)
            ax2.set_title(month, fontsize=20, color='darkred')

            mean_array = np.nan_to_num(plot_3vars_mean.statistic)
            array_list.append(mean_array)
            df_t = pd.DataFrame(mean_array)
            df_t.to_csv(f'D:/WWLLN-Intensity/karin/{year}_february_mean.csv')

    total_mean_array = np.mean(array_list, axis=0)
    imshow_mean = ax3.imshow(total_mean_array.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    ax3.plot(long_points_med, lat_points_med, color='k')
    ax3.set_xlim(xmin=-7, xmax=37)
    ax3.set_ylim(ymin=28, ymax=47)
    imshow_mean.set_clim(vmin=100, vmax=10000)
    ax3.set_title('Total', fontsize=20, color='darkred')

    df_t = pd.DataFrame(total_mean_array)
    df_t.to_csv(f'D:/WWLLN-Intensity/karin/{year}_total_mean.csv')

    cb = fig.colorbar(imshow_mean, ax=axes, shrink=0.6)
    cb.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    fig.suptitle(f'Lightnings Intensity Mean (Joule) for {year}', fontsize=20)
    plt.show()


def get_energy_plot_sum(year, all_years_points):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    array_list = []
    dec_array = []
    jan_array = []
    feb_array = []

    for month in list(all_years_points[year]):
        data = all_years_points[year][month]
        plot_3vars_sum, plot_3vars_mean, longs, lats, energies, long_bins, lat_bins = get_3vars_plot_per_month(data, long_points_med, lat_points_med)

        if month == 'Dec':
            mean_array = np.nan_to_num(plot_3vars_sum.statistic)
            dec_array.append(mean_array)
            array_list.append(mean_array)

        if month == 'Jan':
            mean_array = np.nan_to_num(plot_3vars_sum.statistic)
            jan_array.append(mean_array)
            array_list.append(mean_array)

        if month == 'Feb':
            mean_array = np.nan_to_num(plot_3vars_sum.statistic)
            feb_array.append(mean_array)
            array_list.append(mean_array)

    total_mean_array = np.sum(array_list, axis=0)

    return dec_array, jan_array, feb_array, total_mean_array


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


def get_energy_plot_sum_total(dec_array_mean, jan_array_mean, feb_array_mean, total_array_mean):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]
    cmap = cm.get_cmap('YlOrRd')
    cmap.set_under('w')
    # norm = LogNorm(vmin=100, vmax=10000000)

    ax0.plot(long_points_med, lat_points_med, color='k')
    ax0.set_xlim(xmin=-7, xmax=37)
    ax0.set_ylim(ymin=28, ymax=47)

    ax1.plot(long_points_med, lat_points_med, color='k')
    ax1.set_xlim(xmin=-7, xmax=37)
    ax1.set_ylim(ymin=28, ymax=47)

    ax2.plot(long_points_med, lat_points_med, color='k')
    ax2.set_xlim(xmin=-7, xmax=37)
    ax2.set_ylim(ymin=28, ymax=47)

    ax3.plot(long_points_med, lat_points_med, color='k')
    ax3.set_xlim(xmin=-7, xmax=37)
    ax3.set_ylim(ymin=28, ymax=47)

    for island in islands_dict:
        coords = islands_dict[island]
        longs_island = coords[0]
        lats_island = coords[1]
        ax0.plot(longs_island, lats_island, color='k')
        ax1.plot(longs_island, lats_island, color='k')
        ax2.plot(longs_island, lats_island, color='k')
        ax3.plot(longs_island, lats_island, color='k')

    dec_sum = np.sum(dec_array_mean, axis=0)
    jan_sum = np.sum(jan_array_mean, axis=0)
    feb_sum = np.sum(feb_array_mean, axis=0)
    total_sum = np.sum(total_array_mean, axis=0)

    # imshow_mean_dec = ax0.imshow(dec_sum.T, origin='lower', cmap='YlOrRd', norm=norm, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    # imshow_mean_jan = ax1.imshow(jan_sum.T, origin='lower', cmap='YlOrRd', norm=norm, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    # imshow_mean_feb = ax2.imshow(feb_sum.T, origin='lower', cmap='YlOrRd', norm=norm, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    # imshow_mean_total = ax3.imshow(total_sum.T, origin='lower', cmap='YlOrRd', norm=norm, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])

    imshow_mean_dec = ax0.imshow(dec_sum.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_jan = ax1.imshow(jan_sum.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_feb = ax2.imshow(feb_sum.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_total = ax3.imshow(total_sum.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])

    imshow_mean_dec.set_clim(vmin=100, vmax=1000000)
    imshow_mean_jan.set_clim(vmin=100, vmax=1000000)
    imshow_mean_feb.set_clim(vmin=100, vmax=1000000)
    imshow_mean_total.set_clim(vmin=100, vmax=1000000)
    ticks = [10000, 20000, 40000, 60000, 80000, 100000, 1000000]

    ax0.set_title('Dec', fontsize=20, color='darkred')
    ax1.set_title('Jan', fontsize=20, color='darkred')
    ax2.set_title('Feb', fontsize=20, color='darkred')
    ax3.set_title('Total', fontsize=20, color='darkred')

    cb = fig.colorbar(imshow_mean_total, ax=axes, shrink=0.6, ticks=ticks)
    cb.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    fig.suptitle(f'Lightnings Intensity Sum (Joule) for 2009-2020', fontsize=20)
    plt.show()
    return dec_sum, jan_sum, feb_sum, total_sum


def get_energy_plot_mean_total(dec_array_mean, jan_array_mean, feb_array_mean, total_array_mean):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]
    cmap = cm.get_cmap('YlOrRd')
    cmap.set_under('w')

    ax0.plot(long_points_med, lat_points_med, color='k')
    ax0.set_xlim(xmin=-7, xmax=37)
    ax0.set_ylim(ymin=28, ymax=47)

    ax1.plot(long_points_med, lat_points_med, color='k')
    ax1.set_xlim(xmin=-7, xmax=37)
    ax1.set_ylim(ymin=28, ymax=47)

    ax2.plot(long_points_med, lat_points_med, color='k')
    ax2.set_xlim(xmin=-7, xmax=37)
    ax2.set_ylim(ymin=28, ymax=47)

    ax3.plot(long_points_med, lat_points_med, color='k')
    ax3.set_xlim(xmin=-7, xmax=37)
    ax3.set_ylim(ymin=28, ymax=47)

    for island in islands_dict:
        coords = islands_dict[island]
        longs_island = coords[0]
        lats_island = coords[1]
        ax0.plot(longs_island, lats_island, color='k')
        ax1.plot(longs_island, lats_island, color='k')
        ax2.plot(longs_island, lats_island, color='k')
        ax3.plot(longs_island, lats_island, color='k')

    dec_mean = np.mean(dec_array_mean, axis=0)
    jan_mean = np.mean(jan_array_mean, axis=0)
    feb_mean = np.mean(feb_array_mean, axis=0)
    total_mean = np.mean(total_array_mean, axis=0)

    imshow_mean_dec = ax0.imshow(dec_mean.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_jan = ax1.imshow(jan_mean.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_feb = ax2.imshow(feb_mean.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow_mean_total = ax3.imshow(total_mean.T, origin='lower', cmap=cmap, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])

    imshow_mean_dec.set_clim(vmin=100, vmax=10000)
    imshow_mean_jan.set_clim(vmin=100, vmax=10000)
    imshow_mean_feb.set_clim(vmin=100, vmax=10000)
    imshow_mean_total.set_clim(vmin=100, vmax=10000)

    ax0.set_title('Dec', fontsize=20, color='darkred')
    ax1.set_title('Jan', fontsize=20, color='darkred')
    ax2.set_title('Feb', fontsize=20, color='darkred')
    ax3.set_title('Total', fontsize=20, color='darkred')

    cb = fig.colorbar(imshow_mean_total, ax=axes, shrink=0.6)
    cb.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    fig.suptitle(f'Lightnings Intensity Mean (Joule) for 2009-2020', fontsize=20)
    plt.show()
    return dec_mean, jan_mean, feb_mean, total_mean


def main():
    years = get_years_path()
    all_years_files = get_year_files_dict(years)
    all_years_dfs = get_year_df_dict(all_years_files)
    all_years_points = get_points_inside_med(all_years_dfs)
    dec_array_mean = []
    jan_array_mean = []
    feb_array_mean = []
    total_array_mean = []

    for year in list(all_years_points.keys()):
        dec_array, jan_array, feb_array, total_array = get_energy_plot_sum(year, all_years_points)
        # dec_array, jan_array, feb_array, total_array = get_energy_plot_mean(year, all_years_points)
        dec_array_mean.append(dec_array)
        jan_array_mean.append(jan_array)
        feb_array_mean.append(feb_array)
        total_array_mean.append(total_array)
        print(f'finished statistics for {year}')

    dec_sum, jan_sum, feb_sum, total_sum = get_energy_plot_sum_total(dec_array_mean, jan_array_mean, feb_array_mean, total_array_mean)
    # dec_mean, jan_mean, feb_mean, total_mean = get_energy_plot_mean_total(dec_array_mean, jan_array_mean, feb_array_mean, total_array_mean)

    df_dec = pd.DataFrame(dec_sum[0])
    df_dec.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/dec_total_sum.csv')
    df_jan = pd.DataFrame(jan_sum[0])
    df_jan.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/jan_total_sum.csv')
    df_feb = pd.DataFrame(feb_sum[0])
    df_feb.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/feb_total_sum.csv')
    df_total = pd.DataFrame(total_sum)
    df_total.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/total_total_sum.csv')

    # df_dec = pd.DataFrame(dec_mean[0])
    # df_dec.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/dec_total_mean.csv')
    # df_jan = pd.DataFrame(jan_mean[0])
    # df_jan.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/jan_total_mean.csv')
    # df_feb = pd.DataFrame(feb_mean[0])
    # df_feb.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/feb_total_mean.csv')
    # df_total = pd.DataFrame(total_mean)
    # df_total.to_csv(f'D:/WWLLN-Intensity/Validation CSV/total_mean/total_total_mean.csv')

if __name__ == '__main__':
    main()