import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


sal_path = 'D:/WWLLN-Intensity/Validation CSV/sal.nc'
sal_ds = xr.open_dataset(sal_path)
sal_array = sal_ds.so.isel(time=100)
time_array = sal_ds['time'].data

for i in time_array:
    date = np.datetime64(i, 'M')
    if date == np.datetime64('2009-12'):
        time_list = time_array.tolist()
        i = int(i)
        index_i = time_list.index(i)
        sal_array = sal_ds.so.isel(time=index_i)


# temp_path = 'D:/WWLLN-Intensity/Validation CSV/ptemp.nc'
# temp_ds = xr.open_dataset(temp_path)
# temp_array = temp_ds.thetao.isel(time=50)

# temp_array.plot()
# plt.show()





