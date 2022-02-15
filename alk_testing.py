import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely import geometry
import math
from scipy.stats import binned_statistic_2d
from mpl_toolkits.axes_grid1 import make_axes_locatable


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


def get_alk_plot(mean_array, lat_list, long_list):
    # cmap = cm.get_cmap('YlGnBu')
    cmap = cm.get_cmap('PuBu')
    min_alk = round(2.462 * 974.658)
    max_alk = round(2.873 * 974.658)
    levels = np.linspace(min_alk, max_alk, 10)
    alk_plot = plt.contourf(long_list, lat_list, mean_array[0], alpha=1, cmap=cmap, levels=levels, zorder=0, linewidths=1)
    ticks = np.linspace(min_alk, max_alk, 5, endpoint=True)
    cb2 = plt.colorbar(alk_plot, ticks= ticks, shrink=0.55)
    cb2.ax.set_title('\u03BC' + 'mol' '/ Kg\n', fontsize=14)
    # cb2.set_label('\u03BC' + 'mol' '/ Kg', fontsize=14, labelpad=30)

    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    plt.plot(long_points_med, lat_points_med, color='k', zorder=100)
    for island in islands_dict:
        coords = islands_dict[island]
        longs_island = coords[0]
        lats_island = coords[1]
        plt.plot(longs_island, lats_island, color='k', zorder=100)
    ax = plt.gca()
    # plt.clabel(alk_plot, inline=True, fontsize=6)
    return ax


def get_nparr_from_csv():
    total_sum_file = 'D:/WWLLN-Intensity/Validation CSV/total_mean/sum/total_total_sum.csv'
    total_sum = pd.read_csv(total_sum_file)
    total_sum = total_sum.to_numpy()
    total_sum = np.where(total_sum < 2000000, np.nan, total_sum)
    return total_sum


def get_energy_plot_sum_total(total_sum, ax):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    cmap = cm.get_cmap('autumn')
    total_sum[total_sum == 0] = np.nan
    imshow_sum_total = ax.imshow(total_sum.T, origin='lower', cmap=cmap, alpha=1,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    # imshow_sum_total.set_clim(vmin=2800000, vmax=3000000)
    # divider = make_axes_locatable(plt.gca())
    # cax = divider.append_axes("right", "2%", pad="3%")
    # cb1 = plt.colorbar(imshow_sum_total, cax=cax, shrink=0.5)
    # cb1.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    ax.set_xlim([-7, 37])
    ax.set_ylim([29, 47])

    # cmap = cm.get_cmap('gray')
    # ax.plot(long_points_med, lat_points_med, color='k')
    # for island in islands_dict:
    #     coords = islands_dict[island]
    #     longs_island = coords[0]
    #     lats_island = coords[1]
    #     ax.plot(longs_island, lats_island, color='k')
    # cb1 = plt.colorbar(imshow_mean_total, shrink=0.5)
    # cb = fig.colorbar(imshow_mean_total, ax=ax, shrink=0.6)
    # cb.set_label('J * 100 km^-2', fontsize=14, rotation=-90, labelpad=30)
    # fig.suptitle(f'Lightnings Intensity Mean (Joule) for 2009-2020', fontsize=20)


def main():
    mean_array, lat_list, long_list = get_array_mean()
    ax = get_alk_plot(mean_array, lat_list, long_list)
    total_mean_light = get_nparr_from_csv()
    get_energy_plot_sum_total(total_mean_light, ax)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()







    # plt.clabel(alk_plot, inline=True, fontsize=5)
    # cb2 = plt.colorbar(alk_plot, shrink=0.5)
    # cb2.set_label('Mol * m^-3', fontsize=14, rotation=90, labelpad=20)
    # cmap = cm.get_cmap('winter')
    # cmap.set_under('w')
    # alk_plot = plt.pcolormesh(long_list, lat_list, mean_array[0], alpha= 1, cmap= cmap, shading='gouraud', zorder=0)

