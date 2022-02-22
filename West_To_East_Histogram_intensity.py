import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
from scipy.stats import binned_statistic_2d


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
        if year == 'D:/WWLLN-Intensity/DJF2009-10':
        # if year != 'D:/WWLLN-Intensity/DJF2020-21':
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


def get_united_df_line(df):
    data = []
    for date, long, lat, energy in zip(df.Date, df.Long, df.Lat, df.Energy_J):
        if -4.43 <= long < 6.35:
            calc_lat1 = 0.382 * long + 36.93
            if calc_lat1 -0.5 < lat < calc_lat1 + 0.5:
                data.append([date, long, lat, energy])

        if 6.35 <= long < 17.13:
            calc_lat2 = -0.403 * long + 41.92
            if calc_lat2 -0.5 < lat < calc_lat2 + 0.5:
                data.append([date, long, lat, energy])

        if 17.13 <= long <= 34.84:
            calc_lat3 = -0.14 * long + 37.34
            if calc_lat3 -0.5 < lat < calc_lat3 + 0.5:
                data.append([date, long, lat, energy])

    united_df = pd.DataFrame(data, columns=['Date', 'Long', 'Lat', 'Energy'])
    united_df.drop_duplicates(keep=False, inplace=True)
    return united_df


def get_values_dict(united_df):
    hist, xedges, yedges = np.histogram2d(united_df.Long, united_df.Energy, bins= (414, 77))
    print(yedges[:-1][1] - yedges[:-1][0], 'this is y width')
    width = 0.85 * (xedges[:-1][1] - xedges[:-1][0])
    value_dict = {}
    x_values = []
    num_lightnings = []

    for i in range(len(yedges) -1):
        for j in range(len(xedges) -1):
            value = hist.T[i,j]
            x_value = xedges[j]
            if value != 0:
                x_values.append(x_value)
                num_lightnings.append(value)
                value_dict[x_value] = value
    ticks = np.arange(int(min(value_dict.keys())), int(max(value_dict.keys())) + 1.5, 0.5)
    df = pd.DataFrame({})
    df['Longs'] = x_values
    df['Num Lightnings'] = num_lightnings
    df.to_csv( 'D:/WWLLN/Distribution_Intensity.csv')
    return width, value_dict, ticks


def draw_plot(width, value_dict, ticks):
    fig, axes = plt.subplots()
    for key in value_dict.keys():
        value = value_dict[key]
        value_to_show = str(int(value)) + '\n'
        axes.bar(key, value, align='edge', width=width, color= 'orange')
        # plt.text(key, value, value_to_show)

    with mpl.cbook.get_sample_data('C:/Users/karin/Desktop/Work/Python/Lightning mapping/Photos/Med_Line_with_arrow_layout_only.png') as file:
        image = plt.imread(file, format='png')
    axin = axes.inset_axes([-4,210,10,80], transform=axes.transData)
    axin.imshow(image, aspect='auto', zorder=0)
    axin.axis('off')

    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    plt.xticks(ticks, rotation= 90, fontsize= 10)
    plt.xlabel("Longtitude ($^{\circ}$)", labelpad=25, fontsize= 16)
    plt.yticks(fontsize= 14)
    plt.ylabel('Intensity', labelpad=25, fontsize= 16)
    plt.title('Lightning Intensity Distribution in The Mediterranean Sea 2009-2020\n', color= '#AF4700', fontsize= 20)
    plt.show()


def main():
    years = get_years_path()
    all_years_files = get_year_files_dict(years)
    all_years_dfs = get_year_df_dict(all_years_files)
    data = []
    for year in all_years_dfs:
        months = list(all_years_dfs[year].keys())
        for month in months:
            month_data = all_years_dfs[year][month]
            for date, long, lat, energy in zip(month_data.Date, month_data.Long, month_data.Lat, month_data.Energy_J):
                data.append([date, long, lat, energy])

    united_df = pd.DataFrame(data, columns = ['Date', 'Long', 'Lat', 'Energy_J'])
    line_data = get_united_df_line(united_df)
    plot_3vars_sum = binned_statistic_2d(line_data.Long, line_data.Lat, line_data.Energy, statistic=np.nansum, bins=[10, 10])
    light_sum = plot_3vars_sum.statistic
    longs = plot_3vars_sum.x_edge
    lats = plot_3vars_sum.y_edge

    print(longs)
    print(lats)
    print(light_sum)
    # print(len(light_sum), len(longs), len(lats))
    # plt.scatter(longs, lats, s=light_sum)
    # plt.show()


    # imshow = plt.imshow(plot_3vars_sum.statistic.T, origin='lower', extent= [min(line_data.Long), max(line_data.Long), min(line_data.Lat), max(line_data.Lat)])
    # plt.show()
    # width, value_dict, ticks = get_values_dict(line_data)
    # draw_plot(width, value_dict, ticks)


if __name__ == '__main__':
    main()
