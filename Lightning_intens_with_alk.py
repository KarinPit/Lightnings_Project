import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

nc_file = 'D:/WWLLN-Intensity/Validation CSV/alk.nc'
alk_ds = xr.open_dataset(nc_file)
times = alk_ds.time.to_pandas()
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
        df = pd.DataFrame(np_arr[0])

        df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/{file_name}.csv')
        array_list.append(np_arr)
mean_array = np.mean(array_list, axis=0)
df = pd.DataFrame(mean_array[0])
df.to_csv(f'D:/WWLLN-Intensity/Validation CSV/mean.csv')

lat_list = alk_ds.latitude.data.tolist()
long_list = alk_ds.longitude.data.tolist()
cmap = cm.get_cmap('rainbow')
cmap.set_under('w')
plt.pcolormesh(long_list, lat_list, mean_array[0], cmap= cmap, shading='gouraud')
plt.clim(2.4, 2.8)
cb = plt.colorbar()
cb.set_label('Mol * m^-3', fontsize=14, rotation=90, labelpad=30)
plt.show()























# nc_file = 'D:/WWLLN-Intensity/Validation CSV/alk.nc'
# alk_ds = xr.open_dataset(nc_file)
# times = alk_ds.time.to_pandas()
# months = ['1', '2', '3']
#
# for i in times:
#     if i in months:
#         alk_sample = alk_ds.talk.isel(time=i)
#
# alk_sample = alk_ds.talk.isel(time=0)
# # notice that by specifying longitude = 1 there is no need to create a list
# alk_splong = alk_sample.isel(longitude=1)
# lat_array = alk_splong.latitude.data.tolist()
# alk_splong_data = alk_splong.data.tolist()[0]
# plt.plot(lat_array, alk_splong_data, marker='o', color='blue')
# # plt.show()
#
#










# print(alk_splong_data)
# print(long_array)
# print(lat_array)
# print(len(alk_splong_data), len(long_array), len(lat_array))

# sal_path = 'D:/WWLLN-Intensity/Validation CSV/sal.nc'
# sal_ds = xr.open_dataset(sal_path)
# sal_array = sal_ds.so.isel(time=0)
# salinity = np.array(sal_array).flatten().tolist()
# print(len(salinity))
#
# longs = sal_array.lon.data.tolist()
# lats = sal_array.lat.data.tolist()
# #
#
#
#
# # plt.plot(longs, lats, salinity)
#
#
# # longs = sal_ds.lon.data.tolist()
# # lats = sal_ds.lat.data.tolist()
# # depth = sal_ds.depth.data.tolist()[0]
# # longs_index = [longs.index(i) for i in longs]
# # lats_index = [lats.index(i) for i in lats]
#
#
#
#
#




# for i in sal_array[0]:
#     boo = np.isnan(i).all()
#     if boo == False:
#         for b in i:
#             if np.isnan(b).all() == False:
#                 print(b)


# sal_array = sal_ds.so.isel(time=100)
# time_array = sal_ds['time'].data
# for i in time_array:
#     date = np.datetime64(i, 'M')
#     if date == np.datetime64('2009-12'):
#         time_list = time_array.tolist()
#         i = int(i)
#         index_i = time_list.index(i)
#         sal_array = sal_ds.so.isel(time=index_i)


# temp_path = 'D:/WWLLN-Intensity/Validation CSV/ptemp.nc'
# temp_ds = xr.open_dataset(temp_path)
# temp_array = temp_ds.thetao.isel(time=50)

# temp_array.plot()
# plt.show()





