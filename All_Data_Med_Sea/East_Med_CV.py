import numpy as np
import xarray as xr
import pandas as pd
import math
from shapely import geometry
from scipy.interpolate import interp2d


def get_ds():
    nc_file = 'D:/WWLLN-Intensity/Validation CSV/info/perc_cape.nc'
    ds = xr.open_dataset(nc_file)
    lat_list = ds.latitude.data.tolist()
    long_list = ds.longitude.data.tolist()
    # lat_list = ds.lat.data.tolist()
    # long_list = ds.lon.data.tolist()
    return long_list, lat_list, ds


# def get_ds():
#     nc_file = 'D:/WWLLN-Intensity/Validation CSV/info/perc_cape.nc'
#     ds = xr.open_dataset(nc_file)
#     lat_list = ds.latitude.data.tolist()
#     long_list = ds.longitude.data.tolist()
#     return long_list, lat_list, ds


def get_copernicus_array():
    long_list, lat_list, ds = get_ds()
    pandas_times = ds.time.to_pandas()

    all_data_array = {}
    for time in pandas_times:
        year = time.year
        month = time.month
        # if month in [1, 2, 3]:
        if month in [12, 1, 2]:
            if month == 12:
                month = 'Dec'
            if month == 1:
                month = 'Jan'
            if month == 2:
                month = 'Feb'

            ptimes_list = pandas_times.to_list()
            index = ptimes_list.index(time)
            stime = ds.cape.isel(time=index)
            array = stime.to_numpy()
            all_data_array[f'{year}_{month}'] = array
    return all_data_array


def get_copernicus_data():
    long_list, lat_list, ds = get_ds()
    pandas_times = ds.time.to_pandas()

    all_data_dict = {}
    for time in pandas_times:
        year = time.year
        month = time.month
        # if month in [1, 2, 3]:
        if month in [12, 1, 2]:
            if month == 12:
                month = 'Dec'
            if month == 1:
                month = 'Jan'
            if month == 2:
                month = 'Feb'

            ptimes_list = pandas_times.to_list()
            index = ptimes_list.index(time)
            stime = ds.tp.isel(time=index)
            # stime = ds.cape.isel(time=index)
            # df1 = pd.DataFrame(stime)
            # df1 = df1[df1.columns[152:]]
            # df_array = df1.to_numpy()
            # df = pd.DataFrame({})
            # df[f'{month}_Mean_Values'] = [np.nanmean(df_array)]
            # all_data_dict[f'{year}_{month}'] = df
            # df = pd.DataFrame(stime[0])
            # df = df[df.columns[901:]]
            # count = len(df)
            # area_size = 837088.74  # squared km
            # average_count = count / area_size
            # df_list = df.to_numpy()
            # mean_val = np.nanmean(df_list)
            # df = pd.DataFrame({})
            # df[f'{month}_Mean_Values'] = [mean_val]
            # all_data_dict[f'{year}_{month}'] = df
    return all_data_dict


def write_excels(all_data_dict):
    years = set()
    for date in all_data_dict:
        year = date[0:4]
        years.add(year)

    writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/All_Data_CV.xlsx', engine='xlsxwriter')
    for year in sorted(years):
        df = pd.DataFrame({})
        for item in all_data_dict:
            if item[0:4] == year:
                month = item[-3:]
                month_df = all_data_dict[item]
                df = pd.concat([df, month_df], axis=1)
        df.to_excel(writer, sheet_name=year)
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


def make_land_mask(array, longs, lats):
    df = pd.DataFrame(array)
    for long, lat in zip(longs, lats):
        df.at[lat, long] = np.nan
    return df


def perc_cape_data():
    ds_longs, ds_lats, ds = get_ds()
    land_longs, land_lats = get_points_inside_med(ds_longs, ds_lats)
    all_data_array = get_copernicus_array()
    all_data_dict = {}
    for i in all_data_array:
        array = all_data_array[i]
        df = make_land_mask(array, land_longs, land_lats)
        df = df[df.columns[152:]]
        df_array = df.to_numpy()
        mean = np.nanmean(df_array)
        df = pd.DataFrame({})
        df[i] = [mean]
        all_data_dict[i] = df

    # all_data_dict = get_copernicus_data()
    years = set()
    for date in all_data_dict:
        year = date[0:4]
        years.add(year)

    writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/all_med_sea_data_intens/East_Med_Data/All_Data_CAPE.xlsx', engine='xlsxwriter')
    for year in sorted(years):
        df = pd.DataFrame({})
        for item in all_data_dict:
            if item[0:4] == year:
                month = item[-3:]
                month_df = all_data_dict[item]
                df = pd.concat([df, month_df], axis=1)
        df.to_excel(writer, sheet_name=year)
    writer.save()


def main():
    # all_data_dict = get_copernicus_data()
    # write_excels(all_data_dict)
    perc_cape_data()


if __name__ == '__main__':
    main()
