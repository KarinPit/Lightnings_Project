import pandas as pd
import os
import xarray as xr


def main():
    tsi_list = []
    main_dir = 'D:/Solar Irradiance/Daily_TSI'
    files = os.listdir(main_dir)
    tsi_list = []
    time_list = []

    for file in files:
        full_path = main_dir + '/' + file
        nc_file = xr.open_dataset(full_path)
        time = nc_file.time
        if file == '18820101_e18821231':
            for i in range(334, 365):
                dec_tsi = nc_file.TSI.isel(time=i).to_numpy()
                day = time[i].to_pandas()
                day = str(day)[0:10]
                tsi_list.append(dec_tsi)
                time_list.append(day)
        else:
            for i in range(0, 60):
                jan_feb_tsi = nc_file.TSI.isel(time=i).to_numpy()
                day = time[i].to_pandas()
                day = str(day)[0:10]
                if '-03-' not in day:
                    tsi_list.append(jan_feb_tsi)
                    time_list.append(day)
            for i in range(334, 365):
                dec_tsi = nc_file.TSI.isel(time=i).to_numpy()
                day = time[i].to_pandas()
                day = str(day)[0:10]
                tsi_list.append(dec_tsi)
                time_list.append(day)

    df = pd.DataFrame({})
    df['Date'] = time_list
    df['Daily_TSI'] = tsi_list
    print(df)
    df.to_csv('D:/Solar Irradiance/Daily_TSI/All_TSI.csv')
    # df = pd.read_csv('D:/Solar Irradiance/Daily_TSI/All_TSI.csv')
    # print(df)


if __name__ == '__main__':
    main()





































# def main():
#     tsi_list = []
#     main_dir = 'D:/Solar Irradiance'
#     files = os.listdir(main_dir)
#     for file in files:
#         full_path = main_dir + '/' + file
#         nc_file = xr.open_dataset(full_path)
#         time = nc_file.time.to_numpy()
#         if file == '188212_c20170717.nc':
#             tsi = nc_file.TSI.isel(time=11).to_numpy()
#             tup = (time[11], tsi)
#             tsi_list.append(tup)
#         else:
#             tsi_j = nc_file.TSI.isel(time=0).to_numpy()
#             tsi_f = nc_file.TSI.isel(time=1).to_numpy()
#             tsi_d = nc_file.TSI.isel(time=11).to_numpy()
#             j_tup = (time[0], tsi_j)
#             f_tup = (time[1], tsi_f)
#             d_tup = (time[11], tsi_d)
#             tsi_list.append(j_tup)
#             tsi_list.append(f_tup)
#             tsi_list.append(d_tup)
#
#     n = 3
#     x = [tsi_list[i:i + n] for i in range(0, len(tsi_list), n)]
#     years = []
#     means = []
#
#     for i in x:
#         year_tsi = []
#         time_str = str(i[0][0])[0:4]
#         for tsi in i:
#             tsi_val = float(tsi[1])
#             year_tsi.append(tsi_val)
#         year_mean_tsi = np.mean(year_tsi)
#         # print(time_str, year_mean_tsi)
#         years.append(time_str)
#         means.append(year_mean_tsi)
#     df = pd.DataFrame({})
#     df['Years'] = years
#     df['Mean_TSI'] = means
#     df.to_csv('D:/Solar Irradiance/Yearly_TSI.csv')
#
#
#
# if __name__ == '__main__':
#     main()

    # import pandas as pd
    # import os
    # import xarray as xr
    # import numpy as np
    #
    #
    # def main():
    #     tsi_list = []
    #     main_dir = 'D:/Solar Irradiance'
    #     files = os.listdir(main_dir)
    #     for file in files:
    #         full_path = main_dir + '/' + file
    #         nc_file = xr.open_dataset(full_path)
    #         time = nc_file.time.to_numpy()
    #         if file == '188212_c20170717.nc':
    #             tsi = nc_file.TSI.isel(time=11).to_numpy()
    #             tup = (time[11], tsi)
    #             tsi_list.append(tup)
    #         else:
    #             tsi_j = nc_file.TSI.isel(time=0).to_numpy()
    #             tsi_f = nc_file.TSI.isel(time=1).to_numpy()
    #             tsi_d = nc_file.TSI.isel(time=11).to_numpy()
    #             j_tup = (time[0], tsi_j)
    #             f_tup = (time[1], tsi_f)
    #             d_tup = (time[11], tsi_d)
    #             tsi_list.append(j_tup)
    #             tsi_list.append(f_tup)
    #             tsi_list.append(d_tup)
    #
    #     n = 3
    #     x = [tsi_list[i:i + n] for i in range(0, len(tsi_list), n)]
    #     years = []
    #     means = []
    #
    #     for i in x:
    #         year_tsi = []
    #         time_str = str(i[0][0])[0:4]
    #         for tsi in i:
    #             tsi_val = float(tsi[1])
    #             year_tsi.append(tsi_val)
    #         year_mean_tsi = np.mean(year_tsi)
    #         # print(time_str, year_mean_tsi)
    #         years.append(time_str)
    #         means.append(year_mean_tsi)
    #     df = pd.DataFrame({})
    #     df['Years'] = years
    #     df['Mean_TSI'] = means
    #     df.to_csv('D:/Solar Irradiance/Yearly_TSI.csv')
    #
    #
    # if __name__ == '__main__':
    #     main()


# import requests
# from bs4 import BeautifulSoup
# import urllib
#
#
# def get_url_paths(url, ext='', params={}):
#     response = requests.get(url, params=params)
#     if response.ok:
#         response_text = response.text
#     else:
#         return response.raise_for_status()
#     soup = BeautifulSoup(response_text, 'html.parser')
#     parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
#     return parent
#
#
# def main():
#     url = 'https://www.ncei.noaa.gov/data/total-solar-irradiance/access/daily/'
#     ext = 'nc'
#     result = get_url_paths(url, ext)
#
#     for file in result:
#         f_name = file[-31:-13]
#         urllib.request.urlretrieve(file, f'D:/Solar Irradiance/Daily_TSI/{f_name}')
#
#
# if __name__ == '__main__':
#     main()