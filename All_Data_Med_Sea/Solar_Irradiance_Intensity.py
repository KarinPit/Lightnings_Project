import pandas as pd
import matplotlib.pyplot as plt


def get_all_years_data_excel(df):
    years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    writer = pd.ExcelWriter(f'D:/WWLLN-Intensity/Validation CSV/Irradiance/Yearly_Solar_Irradiance.xlsx', engine='xlsxwriter')

    df['date_yyyymmdd'] = df.date_yyyymmdd.astype(str)
    df['Date_YYYY'] = df['date_yyyymmdd'].str[:4]
    df['Date_MM'] = df['date_yyyymmdd'].str[4:6]
    df['Date_DD'] = df['date_yyyymmdd'].str[6:8]
    for year in years:
        year_df = df[df.Date_YYYY.str.contains(year)]
        dec_df = year_df[df.Date_MM.str.contains("12")]
        next_year = str(int(year) + 1)
        year_df = df[df.Date_YYYY.str.contains(next_year)]
        jan_df = year_df[df.Date_MM.str.contains("01")]
        feb_df = year_df[df.Date_MM.str.contains("02")]
        united_df = pd.concat([dec_df, jan_df, feb_df])
        united_df.to_excel(writer, sheet_name=year)
    writer.save()


def get_all_years_data_plot(df):
    years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    df['date_yyyymmdd'] = df.date_yyyymmdd.astype(str)
    df['Date_YYYY'] = df['date_yyyymmdd'].str[:4]
    df['Date_MM'] = df['date_yyyymmdd'].str[4:6]
    df['Date_DD'] = df['date_yyyymmdd'].str[6:8]
    print(df)
    # for year in years:
    #     year_df = df[df.Date_YYYY.str.contains(year)]
    #     plt.plot(year_df.Date_MMDD, year_df.tsi_1au)
    #     # plt.ylim(1000, 1500)
    #     plt.title(year)
    #     plt.show()


def main():
    fields = ['date_yyyymmdd', 'tsi_1au', 'tsi_true_earth']
    names = ['date_yyyymmdd', 'date_jdn', 'avg_measurement_date_jdn', 'std_dev_measurement_date', 'tsi_1au', 'instrument_accuracy_1au', 'instrument_precision_1au', 'solar_standard_deviation_1au', 'measurement_uncertainty_1au', 'tsi_true_earth', 'instrument_accuracy_true_earth', 'instrument_precision_true_earth', 'solar_standard_deviation_true_earth', 'measurement_uncertainty_true_earth', 'provisional_flag']
    raw_df = pd.read_csv('D:/WWLLN-Intensity/Validation CSV/Irradiance/colorado_solar_data.txt', delimiter=',', names=names, usecols=fields)
    print(raw_df)
    # get_all_years_data_excel(raw_df)
    # get_all_years_data_plot(raw_df)


if __name__ == '__main__':
    main()