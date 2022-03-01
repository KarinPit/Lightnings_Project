import pandas as pd
from shapely import geometry
import matplotlib.pyplot as plt
import math
import os
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
            df = df[(df.Long > -6) & (df.Long < 36)]
            df = df[(df.Lat > 30) & (df.Lat < 46)]
            for date, long, lat in zip(df.Date, df.Long, df.Lat):
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


def main_heavylifting():
    yearly_files_dict = get_yearly_files_dict()
    monthly_df_dict, united_df_dict = get_yearly_df_dict(yearly_files_dict)

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

    yearly_month_nums = {}
    yearly_sum_nums = {}

    for year in list(monthly_df_dict.keys()):
        months = monthly_df_dict[year]
        months_dict = {}
        sums_dict = {}
        for month in list(months.keys()):
            month_points_west = []
            month_points_east = []
            month_coords_dict = {}

            month_df = months[month]
            for long, lat in zip(month_df.Long, month_df.Lat):
                point = geometry.Point(long, lat)
                if med_poly.contains(point):
                    if majorca_poly.contains(point) == False and corsica_poly.contains(point) == False and sardinia_poly.contains(point) == False and sicily_poly.contains(point) == False and peleponnese_poly.contains(point) == False and crete_poly.contains(point) == False and cyprus_poly.contains(point) == False and rhodes_poly.contains(point) == False and kios_lesbos_poly.contains(point) == False:
                        if long < 16.5:
                            month_points_west.append(point)
                        if long > 16.5:
                            month_points_east.append(point)

            month_coords_dict['West'] = len(month_points_west)
            month_coords_dict['East'] = len(month_points_east)
            months_dict[month] = month_coords_dict

        west_sum = months_dict['Dec']['West'] + months_dict['Jan']['West'] + months_dict['Feb']['West']
        east_sum = months_dict['Dec']['East'] + months_dict['Jan']['East'] + months_dict['Feb']['East']
        sums_dict['West'] = west_sum
        sums_dict['East'] = east_sum

        yearly_month_nums[year] = months_dict
        yearly_sum_nums[year] = sums_dict

    print(yearly_month_nums)
    print(yearly_sum_nums)




def main():
    yearly_files_dict = get_yearly_files_dict()
    monthly_df_dict, united_df_dict = get_yearly_df_dict(yearly_files_dict)

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

    yearly_month_nums = {}
    yearly_sum_nums = {}

    for year in list(monthly_df_dict.keys()):
        months = monthly_df_dict[year]
        months_dict = {}
        sums_dict = {}
        for month in list(months.keys()):
            month_points_west = []
            month_points_east = []
            month_coords_dict = {}

            month_df = months[month]
            for long, lat in zip(month_df.Long, month_df.Lat):
                point = geometry.Point(long, lat)
                if med_poly.contains(point):
                    if majorca_poly.contains(point) == False and corsica_poly.contains(
                            point) == False and sardinia_poly.contains(point) == False and sicily_poly.contains(
                            point) == False and peleponnese_poly.contains(point) == False and crete_poly.contains(
                            point) == False and cyprus_poly.contains(point) == False and rhodes_poly.contains(
                            point) == False and kios_lesbos_poly.contains(point) == False:
                        if long < 16.5:
                            month_points_west.append(point)
                        if long > 16.5:
                            month_points_east.append(point)

            month_coords_dict['West'] = month_points_west
            month_coords_dict['East'] = month_points_east
            months_dict[month] = month_coords_dict

        yearly_month_nums[year] = months_dict
        yearly_sum_nums[year] = sums_dict




    x_east = np.arange(-10, 16, 0.01)
    x_west = np.arange(16, 50, 0.01)
    y = np.arange(20, 50, 0.1)
    fig, axes = plt.subplots()
    axes.plot(long_points_med, lat_points_med)
    axes.scatter(x_east, y, color='blue')
    axes.scatter(x_west, y, color='red')
    plt.show()

    # my_points_west = yearly_month_nums['2020']['Dec']['West']
    # my_points_east = yearly_month_nums['2020']['Dec']['East']
    # my_points_west_xs = [point.x for point in my_points_west]
    # my_points_west_ys = [point.y for point in my_points_west]
    # my_points_east_xs = [point.x for point in my_points_east]
    # my_points_east_ys = [point.y for point in my_points_east]
    # fig, axes = plt.subplots()
    # axes.plot(long_points_med, lat_points_med)
    # axes.scatter(my_points_west_xs, my_points_west_ys, color='blue')
    # axes.scatter(my_points_east_xs, my_points_east_ys, color='red')
    # plt.show()




if __name__ == '__main__':
    main_heavylifting()


































    # the_table = plt.table(cellText=vals,
    #                       rowLabels=rows_labels,
    #                       rowColours=["palegreen"] * len_rows,
    #                       colLabels=columns_labels,
    #                       loc='bottom'
    #                       )

    # ax.set_axis_off()
    # table = ax.table(
    #     cellText=vals,
    #     rowLabels=rows_labels,
    #     colLabels=columns_labels,
    #     rowColours=["palegreen"] * len_rows,
    #     colColours=["palegreen"] * len_columns,
    #     cellLoc='center',
    #     loc='upper left')
    # plt.show()



    # my_points_west = yearly_month_points['2020']['Dec']['West']
    # my_points_east = yearly_month_points['2020']['Dec']['East']
    #
    # my_points_west_xs = [point.x for point in my_points_west]
    # my_points_west_ys = [point.y for point in my_points_west]
    # my_points_east_xs = [point.x for point in my_points_east]
    # my_points_east_ys = [point.y for point in my_points_east]
    # fig, axes = plt.subplots()
    # axes.plot(long_points_med, lat_points_med)
    # axes.scatter(my_points_west_xs, my_points_west_ys, color='blue')
    # axes.scatter(my_points_east_xs, my_points_east_ys, color='red')
    # plt.show()

    # good_points_xs = [point.x for point in good_points]
    # good_points_ys = [point.y for point in good_points]
    # island_points_xs = [point.x for point in island_points]
    # island_points_ys = [point.y for point in island_points]
    # not_med_points_xs = [point.x for point in not_med_points]
    # not_med_points_ys = [point.y for point in not_med_points]

    # fig, axes = plt.subplots()
    # axes.plot(long_points_med, lat_points_med)
    # axes.scatter(good_points_xs, good_points_ys, color='green')
    # axes.scatter(island_points_xs, island_points_ys, color='blue')
    # axes.scatter(not_med_points_xs, not_med_points_ys, color='red')
    # plt.show()
