import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd


sal_path = 'D:/WWLLN-Intensity/Validation CSV/sal.nc'
sal_ds = xr.open_dataset(sal_path)
sal_array = sal_ds.so.isel(time=100)

temp_path = 'D:/WWLLN-Intensity/Validation CSV/ptemp.nc'
temp_ds = xr.open_dataset(temp_path)
temp_array = temp_ds.thetao.isel(time=50)

# temp_array.plot()
# plt.show()





