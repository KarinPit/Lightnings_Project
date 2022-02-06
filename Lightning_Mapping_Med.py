import os
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from matplotlib import cm
from matplotlib.patches import Rectangle
import matplotlib.colors

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


def get_year_files_list():
    years = get_years_path()
    year_file_list = []
    for year in years:
        year_name = year[-4:]
        year_files_dict = {}
        if year_name != '2021':
            month_files_dict = get_month_files_dict(year, years)
            year_files_dict[year_name] = month_files_dict
            year_file_list.append(year_files_dict)
    return year_file_list


def get_months_df_dict(months_files_dict):
    # This function receives a file list and returns one united file.
    df_dict = {}
    dirs = months_files_dict.keys()
    for dir in dirs:
        files = months_files_dict[dir]
        combined_file = pd.DataFrame({})
        for file in files:
            csv_file = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'])
            combined_file = pd.concat([combined_file, csv_file])
            print(f'combined {file}')
        left_part = combined_file[((combined_file.Long < 0) & (combined_file.Lat < 41))]
        middle_part = combined_file[((combined_file.Long > 0) & (combined_file.Long < 28))]
        right_part = combined_file[((combined_file.Long > 28) & (combined_file.Lat < 41))]
        combined_file = pd.concat([left_part, middle_part, right_part])
        print('finished combining ' + dir)
        df_dict[dir] = combined_file
    return df_dict


def get_united_months_df(df_dict):
    months = df_dict.keys()
    united_df = pd.DataFrame({})
    for month in months:
        month_df = df_dict[month]
        united_df = pd.concat([united_df, month_df])
    return united_df


def get_all_month_files():
    years = get_years_path()
    months = ['Dec', 'Jan', 'Feb']
    dec_files_dict = {}
    jan_files_dict = {}
    feb_files_dict = {}
    for year in years:
        year_name = year[-4:]
        jan_files_dict[year_name] = []
        for item in os.listdir(year):
            full_path = os.path.join(year, item)
            full_path = full_path.replace('\\', '/')
            if os.path.isdir(full_path) == True:
                month_name = item[0:3]
                if month_name == 'Dec':
                    files = get_all_files(full_path)
                    dec_files_dict[year_name] = files
                if month_name == 'Jan':
                    if year_name in ['2011', '2010']:
                        files = get_all_files(full_path)
                        jan_files_dict[year_name].append(files)
                    else:
                        files = get_all_files(full_path)
                        jan_files_dict[year_name] = files
                if month_name == 'Feb':
                    files = get_all_files(full_path)
                    feb_files_dict[year_name] = files
    total_list = []
    for i in jan_files_dict['2010']:
        total_list = total_list + i
    jan_files_dict['2010'] = total_list
    total_list = []
    for i in jan_files_dict['2011']:
        total_list = total_list + i
    jan_files_dict['2011'] = total_list
    return dec_files_dict, jan_files_dict, feb_files_dict


def get_df_dict(files_dict):
    dec_df_dict = {}
    years = files_dict.keys()
    for year in years:
        united_df = pd.DataFrame({})
        year_files = files_dict[year]
        for file in year_files:
            csv_file = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'])
            united_df = pd.concat([united_df, csv_file])
            left_part = united_df[((united_df.Long < 0) & (united_df.Lat < 41))]
            middle_part = united_df[((united_df.Long > 0) & (united_df.Long < 28))]
            right_part = united_df[((united_df.Long > 28) & (united_df.Lat < 41))]
            united_df = pd.concat([left_part, middle_part, right_part])
        print(f'finished combining {year}')
        dec_df_dict[year] = united_df
    return dec_df_dict


def unite_df(month_dict):
    df_list = list(month_dict.values())
    united_df = pd.concat(df_list)
    # years = list(month_dict.keys())
    # for year in years:
    #     year_df = month_dict[year]
    #     united_df = pd.concat([united_df,year_df])
    return united_df


def make_colormap():
    colors = ["#F9F6DD", "#FAF3C0", "#FBF19F", "#FDED6E", "#F7E458", "#FAD645", "#F5BE44", "#F2AF43", "#EE9940", "#E9773C", "#E55E38", "#E23C33", "#D31034", "#AD1827", "#661315"]
    cmap = matplotlib.colors.ListedColormap(colors)
    cmap.set_under("w")
    norm = matplotlib.colors.Normalize(vmin= 1, vmax= 1000)
    return cmap, norm


def multiple_med_plot(df_dict, united_df, year_name):
    extent = [-5.5, 37, 28, 46]
    # cmap, norm = make_colormap()
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(26, 11), constrained_layout=True, subplot_kw={'projection': ccrs.PlateCarree()})
    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]
    axes_dict = {'Dec': ax0, 'Jan': ax1, 'Feb': ax2, 'Sum': ax3}
    cmap = cm.get_cmap('YlOrRd')
    norm = matplotlib.colors.LogNorm(vmin= 1, vmax= 1000)

    for month in axes_dict.keys():
        ax = axes_dict[month]
        ax.add_feature(cfeature.LAND, color='white', zorder=50)
        ax.add_feature(cfeature.COASTLINE, color='k', zorder=50)
        ax.set_extent(extent)
        gl = ax.gridlines(draw_labels=True, zorder=100, color='grey', linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 16}
        gl.ylabel_style = {'size': 16}
        if ax in [ax1, ax3]:
            gl.left_labels = False

        if month != 'Sum':
            if month == 'Dec':
                title = f'{month} {year_name}'
                ax.set_title(title, fontsize=20, color='darkred')
            else:
                title = f'{month} {str(int(year_name) + 1)}'
                ax.set_title(title, fontsize=20, color='darkred')

            rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor= 'white')
            rect_right = Rectangle((27.5, 40), 10, 10, zorder=75, facecolor= 'white')
            ax.add_patch(rect_left)
            ax.add_patch(rect_right)
            ax.outline_patch.set_visible(False)
            hist0 = ax.hist2d(df_dict[month].Long, df_dict[month].Lat, range=[(-5.5, 37), (30, 46)], bins=(500, 200), cmap= cmap, norm=norm)
            vmin, vmax = hist0[-1].get_clim()
            print(vmin, vmax)

        elif month == 'Sum':
            ax.set_title('Sum', fontsize=20, color='darkred')
            rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor= 'white')
            rect_right = Rectangle((27, 40), 10, 10, zorder=75, facecolor= 'white')
            ax.add_patch(rect_left)
            ax.add_patch(rect_right)
            ax.outline_patch.set_visible(False)
            hist1 = ax.hist2d(united_df.Long, united_df.Lat, range=[(-5.5, 37), (30, 46)], bins=(500, 200), cmap= cmap, norm=norm)
            vmin, vmax = hist1[-1].get_clim()
            print(vmin, vmax)

    fig.suptitle(f'Lightning Density per Month {year_name}\n', fontsize= 22)
    fig.tight_layout()
    cbar = fig.colorbar(hist0[3], ax=axes, shrink=0.95)
    cbar.set_label('# of lightnings', fontsize=20, rotation=-90, labelpad=30)
    cbar.ax.tick_params(labelsize=16)
    path = 'D:/WWLLN/Summary Graphs/DJF per Year/' + year_name
    plt.savefig(path, dpi=100, bbox_inches= 'tight')


def multiple_med_plot_all_years(dec_united_df, jan_united_df, feb_united_df, united_df):
    extent = [-5.5, 37, 28, 46]
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(26, 11), constrained_layout=True, subplot_kw={'projection': ccrs.PlateCarree()})
    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]
    axes_dict = {'Dec': ax0, 'Jan': ax1, 'Feb': ax2, 'Sum': ax3}
    cmap = cm.get_cmap('YlOrRd')
    norm = matplotlib.colors.LogNorm(vmin= 1, vmax= 1000)

    months = ['Dec', 'Jan', 'Feb', 'Sum']
    for month in months:
        ax = axes_dict[month]
        ax.add_feature(cfeature.LAND, color='white', zorder=50)
        ax.add_feature(cfeature.COASTLINE, color='k', zorder=50)
        ax.set_extent(extent)
        gl = ax.gridlines(draw_labels=True, zorder=100, color='grey', linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 16}
        gl.ylabel_style = {'size': 16}
        if ax in [ax1, ax3]:
            gl.left_labels = False

        if month == 'Dec':
            ax.set_title(month, fontsize=20, color='darkred')
            rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor= 'white')
            rect_right = Rectangle((27.5, 40), 10, 10, zorder=75, facecolor= 'white')
            ax.add_patch(rect_left)
            ax.add_patch(rect_right)
            ax.outline_patch.set_visible(False)
            hist0 = ax.hist2d(dec_united_df.Long, dec_united_df.Lat, range=[(-5.5, 37), (30, 46)], bins=(500, 200), cmap= cmap, norm= norm)

        if month == 'Jan':
            ax.set_title(month, fontsize=20, color='darkred')
            rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor= 'white')
            rect_right = Rectangle((27.5, 40), 10, 10, zorder=75, facecolor= 'white')
            ax.add_patch(rect_left)
            ax.add_patch(rect_right)
            ax.outline_patch.set_visible(False)
            hist1 = ax.hist2d(jan_united_df.Long, jan_united_df.Lat, range=[(-5.5, 37), (30, 46)], bins=(500, 200), cmap= cmap, norm= norm)

        if month == 'Feb':
            ax.set_title(month, fontsize=20, color='darkred')
            rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor= 'white')
            rect_right = Rectangle((27.5, 40), 10, 10, zorder=75, facecolor= 'white')
            ax.add_patch(rect_left)
            ax.add_patch(rect_right)
            ax.outline_patch.set_visible(False)
            hist2 = ax.hist2d(feb_united_df.Long, feb_united_df.Lat, range=[(-5.5, 37), (30, 46)], bins=(500, 200), cmap= cmap, norm= norm)

        elif month == 'Sum':
            ax.set_title('Sum', fontsize=20, color='darkred')
            rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor= 'white')
            rect_right = Rectangle((27, 40), 10, 10, zorder=75, facecolor= 'white')
            ax.add_patch(rect_left)
            ax.add_patch(rect_right)
            ax.outline_patch.set_visible(False)
            hist3 = ax.hist2d(united_df.Long, united_df.Lat, range=[(-5.5, 37), (30, 46)], bins=(500, 200), cmap= cmap, norm= norm)

    fig.suptitle(f'Lightning Density per Month 2010-2021', fontsize= 22)
    fig.tight_layout()
    cbar = fig.colorbar(hist0[3], ax=axes, shrink=0.95)
    cbar.set_label('# of lightnings', fontsize=20, rotation=-90, labelpad=30)
    cbar.ax.tick_params(labelsize=16)
    path = 'C:/Users/karin/Desktop/Work/Python/Lightning mapping/Photos/All_years'
    plt.savefig(path, dpi=100, bbox_inches= 'tight')



if __name__ == '__main__':
    # years = get_years_path()
    # dec_files_dict, jan_files_dict, feb_files_dict = get_all_month_files()
    # # dec_df_dict = get_df_dict(dec_files_dict)
    # # dec_united_df = unite_df(dec_df_dict)
    # # print('finished december')
    # # del dec_df_dict
    # # dec_united_df.to_csv('D:/WWLLN/Dec_all_year.xlsx')
    #
    # # jan_df_dict = get_df_dict(jan_files_dict)
    # # jan_united_df = unite_df(jan_df_dict)
    # # print('finished january')
    # # del jan_df_dict
    # # jan_united_df.to_csv('D:/WWLLN/Jan_all_year.xlsx')
    #
    # feb_df_dict = get_df_dict(feb_files_dict)
    # feb_united_df = unite_df(feb_df_dict)
    # print('finished february')
    # del feb_df_dict
    # feb_united_df.to_csv('D:/WWLLN/Feb_all_year.xlsx')
    #
    # united_df = pd.DataFrame({})
    # united_df = pd.concat([united_df, dec_united_df, jan_united_df, feb_united_df])
    # multiple_med_plot_all_years(dec_united_df, jan_united_df, feb_united_df, united_df)

    fields = ['Long', 'Lat']
    dec_df = pd.read_csv('D:/WWLLN/Summary Graphs/Dec_all_year.xlsx', usecols= fields)
    jan_df = pd.read_csv('D:/WWLLN/Summary Graphs/Jan_all_year.xlsx', usecols=fields)
    feb_df = pd.read_csv('D:/WWLLN/Summary Graphs/Feb_all_year.xlsx', usecols=fields)
    united_df = pd.concat([jan_df, feb_df, dec_df])
    multiple_med_plot_all_years(dec_df, jan_df, feb_df, united_df)





    # year_file_list = get_year_files_list()
    # for year in year_file_list:
    #     year_name = list(year.keys())[0]
    #     months_files_dict = year[year_name]
    #     print(months_files_dict)
    #     months_df_dict = get_months_df_dict(months_files_dict)
    #     united_df = get_united_months_df(months_df_dict)
    #     multiple_med_plot(months_df_dict, united_df, year_name)

    #
    # year_file_list = get_year_files_list()
    # year = year_file_list[0]
    # year_name = list(year.keys())[0]
    # months_files_dict = year[year_name]
    # print(months_files_dict)
    # months_df_dict = get_months_df_dict(months_files_dict)
    # united_df = get_united_months_df(months_df_dict)
    # multiple_med_plot(months_df_dict, united_df, year_name)











# def get_year_df_dict(months_files_dict):
#     dec_df_dict = {}
#     jan_df_dict = {}
#     feb_df_dict = {}
#     for month in months_files_dict:
#         years = list(month.keys())
#         for year in years:
#             year_files = month[year]
#             month_name = year_files[0][14:17]
#             if month_name == 'Dec':
#                 combined_file = pd.DataFrame({})
#                 for file in year_files:
#                     csv_file = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'])
#                     combined_file = pd.concat([combined_file, csv_file])
#                     left_part = combined_file[((combined_file.Long < 0) & (combined_file.Lat < 41))]
#                     middle_part = combined_file[((combined_file.Long > 0) & (combined_file.Long < 28))]
#                     right_part = combined_file[((combined_file.Long > 28) & (combined_file.Lat < 41))]
#                     combined_file = pd.concat([left_part, middle_part, right_part])
#                 dec_df_dict[year] = combined_file
#
#             if month_name == 'Jan':
#                 combined_file = pd.DataFrame({})
#                 for file in year_files:
#                     csv_file = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'])
#                     combined_file = pd.concat([combined_file, csv_file])
#                     left_part = combined_file[((combined_file.Long < 0) & (combined_file.Lat < 41))]
#                     middle_part = combined_file[((combined_file.Long > 0) & (combined_file.Long < 28))]
#                     right_part = combined_file[((combined_file.Long > 28) & (combined_file.Lat < 41))]
#                     combined_file = pd.concat([left_part, middle_part, right_part])
#                 jan_df_dict[year] = combined_file
#
#             if month_name == 'Feb':
#                 combined_file = pd.DataFrame({})
#                 for file in year_files:
#                     csv_file = pd.read_csv(file, delimiter=',', names=['Date', 'Time', 'Lat', 'Long', 'Resid', 'Nsta'])
#                     combined_file = pd.concat([combined_file, csv_file])
#                     left_part = combined_file[((combined_file.Long < 0) & (combined_file.Lat < 41))]
#                     middle_part = combined_file[((combined_file.Long > 0) & (combined_file.Long < 28))]
#                     right_part = combined_file[((combined_file.Long > 28) & (combined_file.Lat < 41))]
#                     combined_file = pd.concat([left_part, middle_part, right_part])
#                 feb_df_dict[year] = combined_file
#     return dec_df_dict, jan_df_dict, feb_df_dict