import pandas as pd
import numpy as np
from shapely import geometry
import math
import os
import matplotlib.cm as cm
from scipy.stats import binned_statistic_2d
import matplotlib.pyplot as plt
from scipy import stats


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

    # num_points = 0
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
                        # num_points += 1
            months_points[month] = month_data
        print(f'finished {year}')
        all_years_points[year] = months_points
        # print(num_points)
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
    plot_3vars_count = binned_statistic_2d(longs, lats, energies, statistic='count', bins=[long_bins, lat_bins])
    return plot_3vars_count


def get_energy_plot_count(year, all_years_points):
    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    num_array = []
    dec_num = []
    jan_num = []
    feb_num = []

    for month in list(all_years_points[year]):
        data = all_years_points[year][month]
        plot_3vars_count = get_3vars_plot_per_month(data, long_points_med, lat_points_med)

        if month == 'Dec':
            num = np.nan_to_num(plot_3vars_count.statistic)
            dec_num.append(num)
            num_array.append(num)

        if month == 'Jan':
            num = np.nan_to_num(plot_3vars_count.statistic)
            jan_num.append(num)
            num_array.append(num)

        if month == 'Feb':
            num = np.nan_to_num(plot_3vars_count.statistic)
            feb_num.append(num)
            num_array.append(num)

    total_num_array = np.sum(num_array, axis=0)
    return dec_num, jan_num, feb_num, total_num_array


def get_high_int_percentage():
    # get the total sum data and it's columns
    total_sum_file = 'D:/WWLLN-Intensity/Validation CSV/total_mean/sum/total_total_sum.csv'
    total_sum = pd.read_csv(total_sum_file)
    columns = list(total_sum.columns)
    columns = columns[1:]

    # loop over the columns and create two lists- one for all the data and one for the high intensity only
    data = []
    for col in columns:
        col_data = total_sum[col].tolist()
        col_data = [i for i in col_data if i > 0]
        data += col_data
    high_int = [i for i in data if i >= 2000000]

    # calculate percentage of high intensity lightnings
    num_data = len(data)
    num_high_int = len(high_int)
    percentage = num_high_int / num_data * 100
    percentage = round(percentage, 2)


def get_frequency():
    # get the total count data and it's columns
    total_count_file = 'D:/WWLLN-Intensity/Validation CSV/count/total_total_count.csv'
    total_count = pd.read_csv(total_count_file)
    columns = list(total_count.columns)
    columns = columns[1:]

    # loop over the columns and count only non-zero cells
    data = []
    for col in columns:
        col_data = total_count[col].tolist()
        col_data = [i for i in col_data if i > 0]
        data += col_data
    num_boxes = len(data)
    num_lights = sum(data)
    freq = num_lights / num_boxes
    print(freq)
    return freq


def get_normalized_int_plot(freq):
    total_count_file = 'D:/WWLLN-Intensity/Validation CSV/count/total_total_count.csv'
    total_count = pd.read_csv(total_count_file)
    total_count = total_count.loc[:, total_count.columns != total_count.columns[0]]
    total_sum_file = 'D:/WWLLN-Intensity/Validation CSV/total_mean/sum/total_total_sum.csv'
    total_sum = pd.read_csv(total_sum_file)
    total_sum = total_sum.loc[:, total_sum.columns != total_sum.columns[0]]
    total_count = total_count.to_numpy()
    total_sum = total_sum.to_numpy()

    total_sum = total_sum * freq
    normed_array = np.divide(total_sum, total_count)

    long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    cmap = cm.get_cmap('YlOrRd')
    cmap.set_under('w')
    imshow = plt.imshow(normed_array.T, origin='lower', alpha=1, extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    imshow.set_clim(vmin=10000, vmax=10000000)
    plt.colorbar(imshow)
    plt.show()



# def get_normalized_int_plot(freq):
#     total_count_file = 'D:/WWLLN-Intensity/Validation CSV/count/total_total_count.csv'
#     total_sum_file = 'D:/WWLLN-Intensity/Validation CSV/total_mean/sum/total_total_sum.csv'
#     total_count = pd.read_csv(total_count_file)
#     total_sum = pd.read_csv(total_sum_file)
#
#     total_count = total_count.loc[:, total_count.columns != total_count.columns[0]]
#     total_sum = total_sum.loc[:, total_sum.columns != total_sum.columns[0]]
#     total_count = total_count.to_numpy()
#     total_sum = total_sum.to_numpy()
#
#     freq_div_count = freq / total_count
#     total_sum_high_index = np.where(total_sum >= 2000000)
#     # listOfCoordinates = list(zip(total_sum_high_index[0], total_sum_high_index[1]))
#     values = np.take(freq_div_count, [list(total_sum_high_index[0]), list(total_sum_high_index[1])])
#     print(values)

    # total_sum_new = np.where(total_sum >= 2000000, total_sum * freq_div_count, total_sum)
    # total_sum_new = pd.DataFrame(total_sum_new)
    # total_sum_new.to_csv(f'D:/WWLLN-Intensity/Validation CSV/count/total_sum_new.csv')

    # total_sum = np.where(total_sum >= 2000000, total_sum * freq, total_sum)
    # normed_array = np.divide(total_sum, total_count)

    # long_points_med, lat_points_med, islands_dict = get_long_lats_med()
    # plt.imshow(normed_array.T, origin='lower', alpha=1,  extent=[min(long_points_med), max(long_points_med), min(lat_points_med), max(lat_points_med)])
    # plt.show()


def freq_testing():
    total_count_file = 'D:/WWLLN-Intensity/Validation CSV/count/total_total_count.csv'
    total_count = pd.read_csv(total_count_file)
    total_count = total_count.loc[:, total_count.columns != total_count.columns[0]]
    total_sum_file = 'D:/WWLLN-Intensity/Validation CSV/total_mean/sum/total_total_sum.csv'
    total_sum = pd.read_csv(total_sum_file)
    total_sum = total_sum.loc[:, total_sum.columns != total_sum.columns[0]]
    total_count = total_count.to_numpy()
    total_sum = total_sum.to_numpy()

    plt.scatter(total_count, total_sum)
    plt.xlabel('Frequency')
    plt.ylabel('Intensity')
    total_count_list = total_count.flatten()
    total_sum_list = total_sum.flatten()
    df = pd.DataFrame({})
    df['Frequency'] = total_count_list
    df['Intensity'] = total_sum_list
    df.to_csv('D:/WWLLN-Intensity/Validation CSV/freq_vs_intensity.csv')
    # df = pd.DataFrame([total_count_list, total_sum_list], columns=['Frequency', 'Intensity'])

    #
    # slope, intercept, r, p, se = stats.linregress(total_count_list, total_sum_list)
    # print(slope, intercept, r)
    # plt.plot(total_count, slope*total_count + intercept)
    # plt.show()


def main():
    # get_high_int_percentage()
    freq = get_frequency()
    get_normalized_int_plot(freq)
    # freq_testing()


if __name__ == '__main__':
    main()

























    # columns = list(total_sum.columns)
    # columns = columns[1:]
    # data_sum = []
    # data_count = []
    # for col in columns:
    #     col_data_sum = total_sum[col].tolist()
    #     col_data_count = total_count[col].tolist()
    #     col_data_sum = [i for i in col_data_sum if i > 0]
    #     col_data_count = [i for i in col_data_count if i > 0]
    #     data_sum += col_data_sum
    #     data_count += col_data_count
    #
    # for sum, count in zip(data_sum, data_count):
    #     norm_val = sum * freq / count

    # years = get_years_path()
    # all_years_files = get_year_files_dict(years)
    # all_years_dfs = get_year_df_dict(all_years_files)
    # all_years_points = get_points_inside_med(all_years_dfs)
    # dec_array_num = []
    # jan_array_num = []
    # feb_array_num = []
    # total_array_num = []
    #
    # for year in list(all_years_points.keys()):
    #     dec_array, jan_array, feb_array, total_array = get_energy_plot_count(year, all_years_points)
    #     dec_array_num.append(dec_array)
    #     jan_array_num.append(jan_array)
    #     feb_array_num.append(feb_array)
    #     total_array_num.append(total_array)
    #     print(f'finished statistics for {year}')
    #
    # dec_count = np.sum(dec_array_num, axis=0)
    # jan_count = np.sum(jan_array_num, axis=0)
    # feb_count = np.sum(feb_array_num, axis=0)
    # total_count = np.sum(total_array_num, axis=0)
    #
    # df_dec = pd.DataFrame(dec_count[0])
    # df_dec.to_csv(f'D:/WWLLN-Intensity/Validation CSV/count/dec_total_count.csv')
    # df_jan = pd.DataFrame(jan_count[0])
    # df_jan.to_csv(f'D:/WWLLN-Intensity/Validation CSV/count/jan_total_count.csv')
    # df_feb = pd.DataFrame(feb_count[0])
    # df_feb.to_csv(f'D:/WWLLN-Intensity/Validation CSV/count/feb_total_count.csv')
    # df_total = pd.DataFrame(total_count)
    # df_total.to_csv(f'D:/WWLLN-Intensity/Validation CSV/count/total_total_count.csv')


    # total_num_light = []
    # num_high_int_light = []
    # for i in total_sum:
    #     data = total_sum[i]
    #     for b in data:
    #         print(b)
    #     total_num_light.append(i)
    #     # if i > 0:
    #     #     total_num_light.append(i)
    #     if i >= 2000000:
    #         num_high_int_light.append(i)
    #
    # print(len(total_num_light))
    # high_percent = len(num_high_int_light) / len(total_num_light) * 100
    # print(len(num_high_int_light), len(total_num_light), high_percent)
