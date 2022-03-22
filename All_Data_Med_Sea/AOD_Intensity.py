import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    fields = ['Month', 'AOD_500nm', 'NUM_POINTS[AOD_500nm]', 'NUM_DAYS[AOD_500nm]']
    names = ['Month', 'AOD_1640nm', 'AOD_1020nm', 'AOD_870nm', 'AOD_865nm', 'AOD_779nm', 'AOD_675nm', 'AOD_667nm', 'AOD_620nm', 'AOD_560nm', 'AOD_555nm', 'AOD_551nm', 'AOD_532nm', 'AOD_531nm', 'AOD_510nm', 'AOD_500nm', 'AOD_490nm', 'AOD_443nm', 'AOD_440nm', 'AOD_412nm', 'AOD_400nm', 'AOD_380nm', 'AOD_340nm', 'Precipitable_Water(cm)', 'AOD_681nm', 'AOD_709nm', 'AOD_Empty_1', 'AOD_Empty_2', 'AOD_Empty_3', 'AOD_Empty_4', 'AOD_Empty_5', '440-870_Angstrom_Exponent', '380-500_Angstrom_Exponent', '440-675_Angstrom_Exponent', '500-870_Angstrom_Exponent', '340-440_Angstrom_Exponent', '440-675_Angstrom_Exponent[Polar]', 'NUM_DAYS[AOD_1640nm]', 'NUM_DAYS[AOD_1020nm]', 'NUM_DAYS[AOD_870nm]', 'NUM_DAYS[AOD_865nm]', 'NUM_DAYS[AOD_779nm]', 'NUM_DAYS[AOD_675nm]', 'NUM_DAYS[AOD_667nm]', 'NUM_DAYS[AOD_620nm]', 'NUM_DAYS[AOD_560nm]', 'NUM_DAYS[AOD_555nm]', 'NUM_DAYS[AOD_551nm]', 'NUM_DAYS[AOD_532nm]', 'NUM_DAYS[AOD_531nm]', 'NUM_DAYS[AOD_510nm]', 'NUM_DAYS[AOD_500nm]', 'NUM_DAYS[AOD_490nm]', 'NUM_DAYS[AOD_443nm]', 'NUM_DAYS[AOD_440nm]', 'NUM_DAYS[AOD_412nm]', 'NUM_DAYS[AOD_400nm]', 'NUM_DAYS[AOD_380nm]', 'NUM_DAYS[AOD_340nm]', 'NUM_DAYS[Precipitable_Water(cm)]', 'NUM_DAYS[AOD_681nm]', 'NUM_DAYS[AOD_709nm]', 'NUM_DAYS[AOD_Empty]_1', 'NUM_DAYS[AOD_Empty]_2', 'NUM_DAYS[AOD_Empty]_3', 'NUM_DAYS[AOD_Empty]_4', 'NUM_DAYS[AOD_Empty]_5', 'NUM_DAYS[440-870_Angstrom_Exponent]', 'NUM_DAYS[380-500_Angstrom_Exponent]', 'NUM_DAYS[440-675_Angstrom_Exponent]', 'NUM_DAYS[500-870_Angstrom_Exponent]', 'NUM_DAYS[340-440_Angstrom_Exponent]', 'NUM_DAYS[440-675_Angstrom_Exponent[Polar]]', 'NUM_POINTS[AOD_1640nm]', 'NUM_POINTS[AOD_1020nm]', 'NUM_POINTS[AOD_870nm]', 'NUM_POINTS[AOD_865nm]', 'NUM_POINTS[AOD_779nm]', 'NUM_POINTS[AOD_675nm]', 'NUM_POINTS[AOD_667nm]', 'NUM_POINTS[AOD_620nm]', 'NUM_POINTS[AOD_560nm]', 'NUM_POINTS[AOD_555nm]', 'NUM_POINTS[AOD_551nm]', 'NUM_POINTS[AOD_532nm]', 'NUM_POINTS[AOD_531nm]', 'NUM_POINTS[AOD_510nm]', 'NUM_POINTS[AOD_500nm]', 'NUM_POINTS[AOD_490nm]', 'NUM_POINTS[AOD_443nm]', 'NUM_POINTS[AOD_440nm]', 'NUM_POINTS[AOD_412nm]', 'NUM_POINTS[AOD_400nm]', 'NUM_POINTS[AOD_380nm]', 'NUM_POINTS[AOD_340nm]', 'NUM_POINTS[Precipitable_Water(cm)]', 'NUM_POINTS[AOD_681nm]', 'NUM_POINTS[AOD_709nm]', 'NUM_POINTS[AOD_Empty]_1', 'NUM_POINTS[AOD_Empty]_2', 'NUM_POINTS[AOD_Empty]_3', 'NUM_POINTS[AOD_Empty]_4', 'NUM_POINTS[AOD_Empty]_5', 'NUM_POINTS[440-870_Angstrom_Exponent]', 'NUM_POINTS[380-500_Angstrom_Exponent]', 'NUM_POINTS[440-675_Angstrom_Exponent]', 'NUM_POINTS[500-870_Angstrom_Exponent]', 'NUM_POINTS[340-440_Angstrom_Exponent]', 'NUM_POINTS[440-675_Angstrom_Exponent[Polar]]', 'Data_Quality_Level', 'Latitude(degrees)', 'Longitude(degrees)', 'Elevation(meters)']
    df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/Aerosol/2010_2022_CUT-Tepak.txt', delimiter=',', names=names, usecols=fields)
    df = df.replace(to_replace=-999.0, value=np.nan)
    df = df[df['Month'].str.contains("DEC|JAN|FEB")==True]
    df.to_csv('D:/WWLLN-Intensity/Validation CSV/Aerosol/2010_2022_CUT-Tepak.csv')
    # plt.plot(df.Month, df.AOD_500nm)
    # plt.show()


if __name__ == '__main__':
    main()






















    # fields = ['Date(dd:mm:yyyy)', 'Time(hh:mm:ss)', 'AOD_500nm']
    # names = ['Date(dd:mm:yyyy)', 'Time(hh:mm:ss)', 'Day_of_Year', 'Day_of_Year(Fraction)', 'AOD_1640nm', 'AOD_1020nm', 'AOD_870nm', 'AOD_865nm', 'AOD_779nm', 'AOD_675nm', 'AOD_667nm', 'AOD_620nm', 'AOD_560nm', 'AOD_555nm', 'AOD_551nm', 'AOD_532nm', 'AOD_531nm', 'AOD_510nm', 'AOD_500nm', 'AOD_490nm', 'AOD_443nm', 'AOD_440nm', 'AOD_412nm', 'AOD_400nm', 'AOD_380nm', 'AOD_340nm', 'Precipitable_Water(cm)', 'AOD_681nm', 'AOD_709nm', 'AOD_Empty_1', 'AOD_Empty_2', 'AOD_Empty_3', 'AOD_Empty_4', 'AOD_Empty_5', 'Triplet_Variability_1640', 'Triplet_Variability_1020', 'Triplet_Variability_870', 'Triplet_Variability_865', 'Triplet_Variability_779', 'Triplet_Variability_675', 'Triplet_Variability_667', 'Triplet_Variability_620', 'Triplet_Variability_560', 'Triplet_Variability_555', 'Triplet_Variability_551', 'Triplet_Variability_532', 'Triplet_Variability_531', 'Triplet_Variability_510', 'Triplet_Variability_500', 'Triplet_Variability_490', 'Triplet_Variability_443', 'Triplet_Variability_440', 'Triplet_Variability_412', 'Triplet_Variability_400', 'Triplet_Variability_380', 'Triplet_Variability_340', 'Triplet_Variability_Precipitable_Water(cm)', 'Triplet_Variability_681', 'Triplet_Variability_709', 'Triplet_Variability_AOD_Empty_1', 'Triplet_Variability_AOD_Empty_2', 'Triplet_Variability_AOD_Empty_3', 'Triplet_Variability_AOD_Empty_4', 'Triplet_Variability_AOD_Empty_5', '440-870_Angstrom_Exponent', '380-500_Angstrom_Exponent', '440-675_Angstrom_Exponent', '500-870_Angstrom_Exponent', '340-440_Angstrom_Exponent', '440-675_Angstrom_Exponent[Polar]', 'Data_Quality_Level', 'AERONET_Instrument_Number', 'AERONET_Site_Name', 'Site_Latitude(Degrees)', 'Site_Longitude(Degrees)', 'Site_Elevation(m)', 'Solar_Zenith_Angle(Degrees)', 'Optical_Air_Mass', 'Sensor_Temperature(Degrees_C)', 'Ozone(Dobson)', 'NO2(Dobson)', 'Last_Date_Processed', 'Number_of_Wavelengths', 'Exact_Wavelengths_of_AOD(um)_1640nm', 'Exact_Wavelengths_of_AOD(um)_1020nm', 'Exact_Wavelengths_of_AOD(um)_870nm', 'Exact_Wavelengths_of_AOD(um)_865nm', 'Exact_Wavelengths_of_AOD(um)_779nm', 'Exact_Wavelengths_of_AOD(um)_675nm', 'Exact_Wavelengths_of_AOD(um)_667nm', 'Exact_Wavelengths_of_AOD(um)_620nm', 'Exact_Wavelengths_of_AOD(um)_560nm', 'Exact_Wavelengths_of_AOD(um)_555nm', 'Exact_Wavelengths_of_AOD(um)_551nm', 'Exact_Wavelengths_of_AOD(um)_532nm', 'Exact_Wavelengths_of_AOD(um)_531nm', 'Exact_Wavelengths_of_AOD(um)_510nm', 'Exact_Wavelengths_of_AOD(um)_500nm', 'Exact_Wavelengths_of_AOD(um)_490nm', 'Exact_Wavelengths_of_AOD(um)_443nm', 'Exact_Wavelengths_of_AOD(um)_440nm', 'Exact_Wavelengths_of_AOD(um)_412nm', 'Exact_Wavelengths_of_AOD(um)_400nm', 'Exact_Wavelengths_of_AOD(um)_380nm', 'Exact_Wavelengths_of_AOD(um)_340nm', 'Exact_Wavelengths_of_PW(um)_935nm', 'Exact_Wavelengths_of_AOD(um)_681nm', 'Exact_Wavelengths_of_AOD(um)_709nm', 'Exact_Wavelengths_of_AOD(um)_Empty_1', 'Exact_Wavelengths_of_AOD(um)_Empty_2', 'Exact_Wavelengths_of_AOD(um)_Empty_3', 'Exact_Wavelengths_of_AOD(um)_Empty_4', 'Exact_Wavelengths_of_AOD(um)_Empty_5']
    # df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/Aerosol/migal.txt', delimiter=',', names=names, usecols=fields)
    # df = df.replace(to_replace=-999.0, value=np.nan)
    # plt.plot(df['Date(dd:mm:yyyy)'], df.AOD_500nm)
