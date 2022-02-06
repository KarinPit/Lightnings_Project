import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats

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


def get_years_path():
    main_dir_path = 'D:/WWLLN'
    years = []
    for item in os.listdir(main_dir_path):
        full_path = os.path.join(main_dir_path, item)
        if os.path.isdir(full_path) == True and len(item) == 4:
            full_path = full_path.replace('\\', '/')
            years.append(full_path)
    return years


def get_year_paths_dict(years):
    all_paths = {}
    for year in years:
        year_index = years.index(year)
        year_name = year[-4:]
        new_index = year_index - 1
        new_year = years[new_index]
        year_paths = set(())
        for item in os.listdir(year):
            item_name = item[0:3]
            full_path = os.path.join(year, item)
            full_path = full_path.replace('\\', '/')
            if os.path.isdir(full_path) == True:
                if item_name == 'Dec':
                    year_paths.add(full_path)

                new_year_name = new_year[-4:]
                new_dir_name = item_name + new_year_name
                if item_name == 'Feb':
                    if new_index != -1:
                        full_path = os.path.join(new_year, new_dir_name)
                        full_path = full_path.replace('\\', '/')
                        year_paths.add(full_path)

                if item_name == 'Jan':
                    if new_index != -1:
                        to_add = item[-1]
                        if year_name == '2010' and to_add not in ['0', '1']:
                            full_path = os.path.join(new_year, new_dir_name + to_add)
                            full_path = full_path.replace('\\', '/')
                            year_paths.add(full_path)
                        else:
                            full_path = os.path.join(new_year, new_dir_name)
                            full_path = full_path.replace('\\', '/')
                            year_paths.add(full_path)

        all_paths[year_name] = year_paths
    return all_paths


def get_year_files_dict(all_paths):
    yearly_files_dict = {}
    years = list(all_paths.keys())
    for year in years:
        all_files = []
        dirs = all_paths[year]
        for dir in dirs:
            files = get_all_files(dir)
            all_files = all_files + files
        yearly_files_dict[year] = all_files
    return yearly_files_dict


def get_yearly_df(yearly_files_dict):
    yearly_df_dict = {}
    years = list(yearly_files_dict.keys())
    for year in years:
        files = yearly_files_dict[year]
        data = []
        fields = ['Date', 'Long', 'Lat']

        for file in files:
            df = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'], usecols=fields)
            df = df[(df.Long > -6) & (df.Long < 36)]
            df = df[(df.Lat > 34) & (df.Lat < 40)]
            for date, long, lat in zip(df.Date, df.Long, df.Lat):
                if -5 <= long < 6.34:
                    calc_lat1 = 0.382 * long + 36.922
                    if calc_lat1 - 0.5 < lat < calc_lat1 + 0.5:
                        data.append([date, long, lat])

                if 6.34 <= long < 18.76:
                    calc_lat2 = -0.391 * long + 41.830
                    if calc_lat2 - 0.5 < lat < calc_lat2 + 0.5:
                        data.append([date, long, lat])

                if 18.76 <= long <= 38:
                    calc_lat3 = -0.074 * long + 35.884
                    if calc_lat3 - 0.5 < lat < calc_lat3 + 0.5:
                        data.append([date, long, lat])
        yearly_df = pd.DataFrame(data, columns=['Date', 'Long', 'Lat'])
        yearly_df.drop_duplicates(keep=False, inplace=True)
        yearly_df_dict[year] = yearly_df

    return yearly_df_dict


def get_values_dict(united_df):
    hist, xedges, yedges = np.histogram2d(united_df.Long, united_df.Lat, bins= (414, 77))
    value_dict = {}
    for i in range(len(yedges) -1):
        for j in range(len(xedges) -1):
            value = hist.T[i,j]
            x_value = xedges[j]
            if value != 0:
                value_dict[x_value] = value
    return value_dict


def get_values_dict_per_year(yearly_df_dict):
    years = list(yearly_df_dict.keys())
    years_list_to_df = []
    longs_list = []
    num_lightnings = []
    yearly_values_dict = {}
    for year in years:
        df = yearly_df_dict[year]
        value_dict = get_values_dict(df)
        yearly_values_dict[year] = value_dict
        longs = list(value_dict.keys())
        longs_list = longs_list + longs
        num_longs = len(longs)
        year_values = num_longs * [year]
        years_list_to_df = years_list_to_df + year_values
        num_lightnings = num_lightnings + list(value_dict.values())

    yearly_df = pd.DataFrame({})
    yearly_df['Years'] = years_list_to_df
    yearly_df['Longs'] = longs_list
    yearly_df['Num Lightnings'] = num_lightnings
    yearly_df.to_csv('D:/WWLLN/Distribution_per_year.csv')
    return yearly_values_dict


def get_slope(values_dict):
    x = np.array(list(values_dict.keys()))
    y = np.array(list(values_dict.values()))
    slope, intercept, r_value, p_value, std_err_bad = stats.linregress(x, y)
    std_err = np.std(y, ddof=1) / np.sqrt((np.size(y)))
    return slope, intercept, std_err


def create_scatter_plot_values_dict(yearly_values_dict):
    years = list(yearly_values_dict.keys())
    yearly_slope_stderr = {}
    for year in years:
        slope, intercept, std_err = get_slope(yearly_values_dict[year])
        yearly_slope_stderr[year] = slope, std_err
    return yearly_slope_stderr


def slope_bar_plot(yearly_slope_stderr):
    years = list(yearly_slope_stderr.keys())
    years_int = [int(year) for year in years]
    years_int_array = np.array(years_int)
    years_info = list(yearly_slope_stderr.values())
    years_slope = np.array([i[0] for i in years_info])
    slope_united, intercept_united, r_value, p_value, std_err = stats.linregress(years_int_array, years_slope)
    std_err = np.array([i[1] for i in years_info])

    fig, axes = plt.subplots()
    axes.bar(years_int, years_slope, color= '#24B3A8')
    axes.errorbar(years_int, years_slope, xerr= 0, yerr= std_err, fmt= 'o', capsize= 2)
    axes.invert_xaxis()
    axes.plot(years_int, slope_united*years_int_array + intercept_united, color= 'orange')
    axes.invert_xaxis()
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)

    for year in yearly_slope_stderr:
        slope = yearly_slope_stderr[year][0]
        value_to_show = str(round(slope,3))
        plt.text(int(year)-0.4, slope + 0.01, value_to_show)

    plt.xticks(np.arange(min(years_int), max(years_int) + 1, 1), fontsize= 10)
    plt.yticks(np.arange(-0.5, max(years_slope) + 1, 0.25),fontsize=10)
    plt.xlabel('Years', fontsize= 16)
    plt.ylabel('Slope', fontsize= 16)
    plt.suptitle('East to West Lightning Density Slope Comparison (2010- 2021)', fontsize= 18)
    plt.title(f'Regression line from yearly slopes is-   y = {round(slope_united,4)}X + {round(intercept_united,4)}')
    plt.show()



def main():

    years = get_years_path()
    year_paths = get_year_paths_dict(years)
    yearly_files_dict = get_year_files_dict(year_paths)
    yearly_files_dict.pop('2021')
    yearly_df_dict = get_yearly_df(yearly_files_dict)
    yearly_values_dict = get_values_dict_per_year(yearly_df_dict)
    yearly_slope = create_scatter_plot_values_dict(yearly_values_dict)
    slope_bar_plot(yearly_slope)



if __name__ == '__main__':
    main()

    #
    # df = pd.DataFrame({})
    # years_list = list(yearly_slope.keys())
    # slope_list = list(yearly_slope.values())
    # df['Years'] = years_list
    # df['Slope'] = slope_list
    # df.to_csv('D:/WWLLN/Yearly_slope.csv')










# def create_scatter_plot(values_dict):
#     longs = list(values_dict.keys())
#     num_lightning_list = list(values_dict.values())
#     for long in longs:
#         num_lightning = values_dict[long]
#         plt.plot(long, num_lightning, 'o', color= 'orange')
#     longs = np.array(longs)
#     num_lightning_list = np.array(num_lightning_list)
#     m, b = np.polyfit(longs, num_lightning_list, 1)
#     plt.plot(longs, m*longs + b)
#     m = round(m, 3)
#     b = round(b, 3)
#     return m, b
