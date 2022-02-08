import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

nc_file = 'D:/WWLLN-Intensity/Validation CSV/alk.nc'
alk_ds = xr.open_dataset(nc_file)
alk_sample = alk_ds.talk.isel(time=0)
alk_splong = alk_sample.isel(longitude=1)
alk_splong_data = alk_splong.data.tolist()[0]
long_array = alk_splong.data.tolist()[0]
lat_array = alk_splong.latitude.data.tolist()














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





