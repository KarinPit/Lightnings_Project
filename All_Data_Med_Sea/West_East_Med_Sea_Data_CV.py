import numpy as np
import xarray as xr
import pandas as pd
import math
from shapely import geometry
from scipy.interpolate import interp2d


def get_ds_grid():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/info/alk.nc'
    ds = xr.open_dataset(nc_file)
    lat_list = ds.latitude.data.tolist()
    long_list = ds.longitude.data.tolist()
    return long_list, lat_list


def get_ds():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/info/perc_cape.nc'
    ds = xr.open_dataset(nc_file)
    lat_list = ds.latitude.data.tolist()
    long_list = ds.longitude.data.tolist()
    return long_list, lat_list, ds


def get_copernicus_data():
    long_list, lat_list, ds = get_ds()
    pandas_times = ds.time.to_pandas()

    all_data_dict = {}
    all_data_arrays = {}
    for time in pandas_times:
        year = time.year
        month = time.month
        if month in [1, 2, 3]:
            if month == 1:
                month = 'Dec'
            if month == 2:
                month = 'Jan'
            if month == 3:
                month = 'Feb'

            ptimes_list = pandas_times.to_list()
            index = ptimes_list.index(time)
            # stime = ds.talk.isel(time=index)
            stime = ds.cape.isel(time=index)
            np_arr = stime.to_numpy()
            # get the sum of each column(long)
            data = []
            df = pd.DataFrame(np_arr)
            for i in df.columns:
                col_sum = np.nanmean(df[i])
                data.append(col_sum)
            # create df for each month
            df = pd.DataFrame({})
            df['longs'] = long_list
            df['Sum'] = data
            all_data_dict[f'{year}_{month}'] = df
            all_data_arrays[f'{year}_{month}'] = np_arr


    return all_data_dict, all_data_arrays


def get_stats_of_df(df, long_list):
    data = []
    for i in df.columns:
        col_sum = np.nanmean(df[i])
        data.append(col_sum)
    # create df for each month
    df = pd.DataFrame({})
    df['longs'] = long_list
    df['Sum'] = data
    return df


def write_excels(all_data_dict):
    years = set()
    for date in all_data_dict:
        year = date[0:4]
        years.add(year)

    for year in sorted(years):
        writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/CAPE/{year}.xlsx', engine='xlsxwriter')
        for item in all_data_dict:
            if item[0:4] == year:
                month = item[-3:]
                month_df = all_data_dict[item]
                month_df.to_excel(writer, sheet_name=month)
        writer.save()


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


def get_points_inside_med(examp_longs, examp_lats):
    med_poly, majorca_poly, corsica_poly, sardinia_poly, sicily_poly, peleponnese_poly, crete_poly, cyprus_poly, rhodes_poly, kios_lesbos_poly = get_all_polygons()
    longs = []
    lats = []
    for long in examp_longs:
        for lat in examp_lats:
            point = geometry.Point(long, lat)
            if med_poly.contains(point) == False:
                long_index = examp_longs.index(long)
                lat_index = examp_lats.index(lat)
                longs.append(long_index)
                lats.append(lat_index)
            else:
                if majorca_poly.contains(point) or corsica_poly.contains(point) or sardinia_poly.contains(point) or sicily_poly.contains(point) or peleponnese_poly.contains(point) or crete_poly.contains(point) or cyprus_poly.contains(point) or rhodes_poly.contains(point) or kios_lesbos_poly.contains(point):
                    long_index = examp_longs.index(long)
                    lat_index = examp_lats.index(lat)
                    longs.append(long_index)
                    lats.append(lat_index)
    return longs, lats


def get_interp2d(examp_longs, examp_lats, long_list, lat_list, array):
    data = interp2d(long_list, lat_list, array, kind='cubic')
    interp_arr = data(examp_longs, examp_lats)
    return interp_arr


def make_land_mask(array, longs, lats):
    df = pd.DataFrame(array)
    for long, lat in zip(longs, lats):
        df.at[lat, long] = np.nan
    return df


def perc_cape_data():
    ds_longs, ds_lats, ds = get_ds()
    examp_longs, examp_lats = get_ds_grid()
    land_longs, land_lats = get_points_inside_med(examp_longs, examp_lats)

    all_data_dict, all_data_arrays = get_copernicus_data()
    for i in all_data_arrays:
        array = all_data_arrays[i]
        interp_array = get_interp2d(examp_longs, examp_lats, ds_longs, ds_lats, array)
        df = make_land_mask(interp_array, land_longs, land_lats)
        df = get_stats_of_df(df, examp_longs)
        all_data_dict[i] = df
    write_excels(all_data_dict)



def main():
    # all_data_dict, np_arr = get_copernicus_data()
    # write_excels(all_data_dict)
    perc_cape_data()


if __name__ == '__main__':
    main()

















    # years = [str(i.year) for i in pandas_times]
    # years = sorted(set(years))
    # years_data = {}

    # for i in pandas_times:
    #     months_df = {}
    #     for year in years:
    #         current_year = i.year
    #         if current_year == year:
    #             if i.month in [1, 2, 3]:
    #                 # if i.month == 1:
    #                 #     month = 'Dec'
    #                 # if i.month == 2:
    #                 #     month = 'Jan'
    #                 # if i.month == 3:
    #                 #     month = 'Feb'
    #                 # get array of the data
    #                 ptimes_list = pandas_times.to_list()
    #                 index = ptimes_list.index(i)
    #                 stime = ds.talk.isel(time=index)
    #                 np_arr = stime.to_numpy()[0]
    #                 # get the sum of each column(long)
    #                 data = []
    #                 df = pd.DataFrame(np_arr)
    #                 for i in df.columns:
    #                     col_sum = np.nansum(df[i])
    #                     data.append(col_sum)
    #                 # create df for each month
    #                 df = pd.DataFrame({})
    #                 df['longs'] = long_list
    #                 df['Sum'] = data
    #                 months_df['bla'] = df
        # years_data[year] = months_df
        # return years_data










    # writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/{year}.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='dec')
    # writer.save()