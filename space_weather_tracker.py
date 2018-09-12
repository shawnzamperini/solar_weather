import pandas as pd
import numpy as np
import urllib.request
import datetime

class SpaceWeatherTracker:
    """
    A tracker that gets average values of a specified day for:
      - Kp index (max/min/average)
      - Proton flux (average): >10, >50, >100 MeV
      - X-ray flux (average): 0.5-4.0, >4.0 ang
      - Neutron count (average): (station choice)
      - S, R, G threat levels
    """

    def __init__(self, year, month, day):
        self.year  = year
        self.month = month
        self.day   = day
        self.date  = datetime.date(self.year, self.month, self.day)
        self.kp_stats    = {}
        self.pflux_stats = {}
        self.xray_stats  = {}
        self.neutron_stats = {}

    def get_Kp(self):
        # Load the webpage with the last 30 days of Kp data into a Dataframe.
        kp_url = 'http://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt'
        self.kp_df = pd.read_csv(kp_url, skiprows=12, sep='\s+',
                            usecols=[0,1,2]+list(range(21,30)),
                            names=['Year', 'Month', 'Day', 'A', 'K1', 'K2',
                                   'K3', 'K4', 'K5', 'K6', 'K7', 'K8'],
                            parse_dates={'Date':[0,1,2]})
        self.kp_df.set_index('Date', inplace=True)

        # Drop the last row (i.e. today) since it isn't complete.
        self.kp_df.drop(self.kp_df.index[-1], inplace=True)
        self.kp_df = self.kp_df.astype('float64')

        # Get the statistics of the desired date.
        self.kp_stats['min']  = self.kp_df.loc[self.date].min()
        self.kp_stats['max']  = self.kp_df.loc[self.date].max()
        self.kp_stats['mean'] = self.kp_df.loc[self.date].mean()

    def get_pflux(self):

        # Put the date in the format that the url uses, and load the data into
        # a Dataframe.
        date_str = self.date.strftime('%Y%m%d')
        pflux_url = 'ftp://ftp.swpc.noaa.gov/pub/lists/particle/' + date_str +\
                    '_Gp_part_5m.txt'
        pflux_df = pd.read_csv(pflux_url, skiprows=26, sep='\s+',
                               usecols=[0,1,2,3,8,10,11],
                               names=['y', 'm', 'd', 's', '>10 MeV', '>50 MeV',
                                      '>100 MeV'],
                               parse_dates={'Time':[0,1,2,3]})
        pflux_df.set_index('Time', inplace=True)

        # Get the statistics of the desired data, replacing all negatives
        # with nan (bad data).
        pflux_df[pflux_df[['>10 MeV', '>50 MeV', '>100 MeV']] < 0] = np.nan
        self.pflux_stats['>10 MeV']  = pflux_df['>10 MeV'].mean()
        self.pflux_stats['>50 MeV']  = pflux_df['>50 MeV'].mean()
        self.pflux_stats['>100 MeV'] = pflux_df['>100 MeV'].mean()

    def get_xray(self, print_url=False):

        # Load the xray url with the correct numbers for the date put in.
        # To do: Make if statement for months that aren't 1-30 days.
        #xray_url = 'https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2018/09/goes15/csv/g15_xrs_1m_20180901_20180930.csv'
        xray_url = 'https://satdat.ngdc.noaa.gov/sem/goes/data/avg/' + \
                    self.date.strftime('%Y') + '/' + self.date.strftime('%m') \
                    + '/goes15/csv/g15_xrs_1m_2018' + self.date.strftime('%m') \
                    + '01_2018' + self.date.strftime('%m') + '30.csv'
        if print_url:
            print("X-ray URL: " + xray_url)
        self.xray_df = pd.read_csv(xray_url,
                                   skiprows=136 + int(datetime.datetime.now().day),
                                   sep=',',
                                   usecols=[0,3,6],
                                   names=['t', '0.5-4.0 A', '1.0-8.0 A'],
                                   parse_dates={'Time':[0]})
        self.xray_df.set_index('Time', inplace=True)

        # Replace nagatives with np.nan (bad data).
        self.xray_df[self.xray_df[['0.5-4.0 A', '1.0-8.0 A']] < 0] = np.nan

        # Get the statistics of the desired data.
        desired_date = self.date.strftime('%Y-%m-%d')
        self.xray_stats['0.5-4.0 A'] = self.xray_df[desired_date]['0.5-4.0 A'].mean()
        self.xray_stats['1.0-8.0 A'] = self.xray_df[desired_date]['1.0-8.0 A'].mean()

    def get_neutrons(self):
        # Files are in format sopo_YYMMDD_neutrons.txt.
        date_fmt = self.date.strftime('%y%m%d')
        neutron_file = '/mnt/c/Users/Shawn/Google Drive/School/Tennessee/' + \
                       'Fall 2018/NE 512/neutron_ascii_files/sopo_' + \
                       date_fmt +'_neutrons.txt'
        self.neutron_df = pd.read_csv(neutron_file, skiprows=25, sep=';',
                                      names=['Date', 'Data'])
        self.neutron_stats['mean'] = self.neutron_df['Data'].mean()
