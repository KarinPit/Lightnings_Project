import os
import pandas as pd
from scipy.stats import binned_statistic_2d
import numpy as np

# WWLN Intensity


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
            total_files = []
            files_folder = os.path.join(year,'loc_files')
            files_folder = files_folder.replace('\\', '/')
            files = get_all_files(files_folder)
            for file in files:
                if file[-8:-6] == '12':
                    total_files.append(file)
                if file[-8:-6] == '01':
                    total_files.append(file)
                if file[-8:-6] == '02':
                    total_files.append(file)
            all_files[year_name] = total_files
    return all_files


def get_united_file(all_files, year):
    with open(f'D:/WWLLN-Intensity/Summary_CSV/{year}_LFI.txt', 'w') as outfile:
        for fname in all_files:
            with open(fname) as infile:
                outfile.write(infile.read())


def get_year_df_dict(fullPath):
    fields = ['Date', 'Long', 'Lat', 'Energy_Uncertainty']
    df = pd.read_csv(fullPath, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nstn', 'Energy_J', 'Energy_Uncertainty', 'Nstn_Energy'], usecols=fields)
    df = df[(df.Lat < 60) & (df.Lat > -60)]
    year = fullPath[-15:-8]
    long_bins = np.arange(-180, 181, 2.0112)
    lat_bins = np.arange(-90, 91, 1.0056)
    plot_3vars_mean = binned_statistic_2d(df.Long, df.Lat, df.Energy_Uncertainty, statistic=np.nansum, bins=[long_bins, lat_bins])
    stats = plot_3vars_mean.statistic.T
    return stats
    # stat_df = pd.DataFrame(stats)
    # stat_df.to_csv(f'D:/WWLLN-Intensity/Summary_CSV/Int_Mats/Sum/All_year_avg_mat.csv')


# def get_all_year_stats():
#     main_dir = 'D:/WWLLN-Intensity/Summary_CSV/All_Years_data.csv'
#     df = pd.read_csv(main_dir)
#     print(df)
#     # year = fullPath[-15:-8]
#     # long_bins = np.arange(-180, 181, 2.0112)
#     # lat_bins = np.arange(-90, 91, 1.0056)
#     # plot_3vars_mean = binned_statistic_2d(df.Long, df.Lat, df.Energy_J, statistic=np.nanmean, bins=[long_bins, lat_bins])
#     # stats = plot_3vars_mean.statistic.T
#     # stat_df = pd.DataFrame(stats)
#     # stat_df.to_csv(f'D:/WWLLN-Intensity/Summary_CSV/Int_Mats/Sum/All_year_avg_mat.csv')


def main():
    # get_all_year_stats()

    main_dir = 'D:/WWLLN-Intensity/Summary_CSV'
    data = []
    for file in os.listdir(main_dir):
        if file[-3:] == 'txt':
            fullPath = os.path.join(main_dir,file)
            stats = get_year_df_dict(fullPath)
            data.append(stats)
    mean_data = np.nanmean(data, axis=0)
    # united_df = pd.concat(data)
    stat_df = pd.DataFrame(mean_data)
    stat_df.to_csv('D:/WWLLN-Intensity/Summary_CSV/All_Years_data_60_EU_Sum.csv')


if __name__ == '__main__':
    main()







































    # years = get_years_path()
    # yearly_files_dict = get_year_files_dict(years)
    # for year in yearly_files_dict:
    #     get_united_file(yearly_files_dict[year], year)
    # get_year_df_dict()


# # WWLN
#
#
# def get_years_path():
#     main_dir_path = 'D:/WWLLN'
#     years = []
#     for item in os.listdir(main_dir_path):
#         full_path = os.path.join(main_dir_path, item)
#         if os.path.isdir(full_path) == True and len(item) == 4:
#             full_path = full_path.replace('\\', '/')
#             years.append(full_path)
#     return years
#
#
# def get_all_files(dir):
#     # This function receives a path and returns a list of all existing files in that path.
#     all_files = os.listdir(dir)
#     loc_files = []
#     for file in all_files:
#         fullPath = os.path.join(dir, file)
#         fullPath = fullPath.replace('\\', '/')
#         if file.find('.loc') != -1 and file[0:2] != '._':
#             loc_files.append(fullPath)
#         else:
#             pass
#     return loc_files
#
#
# def get_yearly_files_dict():
#     # create dict which correlates between year and month, and the files in each month
#     years = get_years_path()
#     yearly_files_dict = {}
#     for year in years:
#         month_dict = get_month_files_dict(year, years)
#         year_name = year[-4:]
#         yearly_files_dict[year_name] = month_dict
#     yearly_files_dict.pop('2021')
#     return yearly_files_dict
#
#
# def get_month_files_dict(year_path, years):
#     month_files_dict = set()
#     year_index = years.index(year_path)
#
#     for item in os.listdir(year_path):
#         item_name = item[0:3]
#         full_path = os.path.join(year_path, item)
#         full_path = full_path.replace('\\', '/')
#
#         if os.path.isdir(full_path):
#             if item_name == 'Dec':
#                 files = get_all_files(full_path)
#                 month_files_dict.update(files)
#
#             if item_name == 'Jan':
#                 new_index = year_index - 1
#                 new_year = years[new_index]
#                 new_year_name = new_year[-4:]
#                 month_dir_list = []
#                 file_list = []
#                 if new_year_name in ['2010', '2011']:
#                     new_year_name = [new_year[-4:], new_year[-4:] + 'a', new_year[-4:] + 'b']
#                     for i in new_year_name:
#                         new_dir_name = item_name + i
#                         full_path = os.path.join(new_year, new_dir_name)
#                         full_path = full_path.replace('\\', '/')
#                         month_dir_list.append(full_path)
#                     for i in month_dir_list:
#                         files = get_all_files(i)
#                         file_list = file_list + files
#                     month_files_dict.update(file_list)
#                 else:
#                     new_index = year_index - 1
#                     new_year = years[new_index]
#                     new_year_name = new_year[-4:]
#                     new_dir_name = item_name + new_year_name
#                     full_path = os.path.join(new_year, new_dir_name)
#                     full_path = full_path.replace('\\', '/')
#                     files = get_all_files(full_path)
#                     month_files_dict.update(files)
#
#             if item_name == 'Feb':
#                 new_index = year_index - 1
#                 new_year = years[new_index]
#                 new_year_name = new_year[-4:]
#                 new_dir_name = item_name + new_year_name
#                 full_path = os.path.join(new_year, new_dir_name)
#                 full_path = full_path.replace('\\', '/')
#                 files = get_all_files(full_path)
#                 month_files_dict.update(files)
#
#     month_files_dict = sorted(month_files_dict)
#     return month_files_dict
#
#
# def get_united_file(all_files, year):
#     with open(f'D:/WWLLN/Summary_CSV/{year}_LFF.txt', 'w') as outfile:
#         for fname in all_files:
#             with open(fname) as infile:
#                 outfile.write(infile.read())
#
#
# def main():
#     years = [str(i) for i in range(2010, 2021)]
#     yearly_files_dict = get_yearly_files_dict()
#     for year in years:
#         get_united_file(yearly_files_dict[year], year)
#
#
# if __name__ == '__main__':
#     main()





# # ENTLN files
# def get_dirs(wanted_date, file_type):
#     main_dir_path = 'D:/ENTLN/ENTLN DATA/'
#     dirs = []
#     for item in os.listdir(main_dir_path):
#         full_path = os.path.join(main_dir_path, item)
#         if os.path.isdir(full_path) and full_path[-7:] == wanted_date:
#             full_path = full_path.replace('\\', '/')
#             for item in os.listdir(full_path):
#                 if os.path.isdir(full_path) and item == file_type:
#                     full_path = os.path.join(full_path, item)
#                     full_path = full_path.replace('\\', '/')
#                     dirs.append(full_path)
#     dirs.sort()
#     return dirs
#
#
# def get_all_files(dir):
#     all_files = os.listdir(dir)
#     txt_files = []
#     for file in all_files:
#         full_path = os.path.join(dir, file)
#         full_path = full_path.replace('\\', '/')
#         if file.find('.txt') != -1:
#             txt_files.append(full_path)
#         else:
#             pass
#     return txt_files
#
#
# def get_united_file(all_files):
#     with open('D:/ENTLN/ENTLN DATA/Dec_2021.txt', 'w') as outfile:
#         for fname in all_files:
#             with open(fname) as infile:
#                 outfile.write(infile.read())
#
#
# def main():
#     wanted_date = '12-2021'
#     file_type = 'flash'
#     dirs = get_dirs(wanted_date, file_type)
#     all_files = []
#     for dir in dirs:
#         files = get_all_files(dir)
#         all_files += files
#     get_united_file(all_files)