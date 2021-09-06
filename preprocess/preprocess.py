import numpy as np
import pandas as pd
import sklearn.base
from sklearn.base import TransformerMixin
from ast import literal_eval as make_tuple
import datetime

RAW_DATA_PATH = '../data/data.csv'
ADDRESSES_DATA_PATH = '../data/addresses.csv'
PREPARED_DATA_PATH = '../data/mail_prep.csv'


class CoordinatesMergeTransformer(TransformerMixin):
    def __init__(self, addresses_path):
        self.addresses_df = pd.read_csv(addresses_path).dropna()
        self.addresses_df['Coordinates'] = self.addresses_df['Coordinates'].apply(make_tuple)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = pd.merge(df, self.addresses_df, left_on='sending_location', right_on='Address')
        df = pd.merge(df, self.addresses_df, left_on='delivery_location', right_on='Address')
        df.drop(columns=['Address_x', 'Address_y', 'Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)
        df.rename(columns={'Coordinates_x': 'sending_coordinates', 'Coordinates_y': 'delivery_coordinates'},
                  inplace=True)

        df.dropna(inplace=True)

        def get_latitude(coords):
            return coords[0]

        def get_longitude(coords):
            return coords[1]

        sending_latitudes = df['sending_coordinates'].apply(get_latitude)
        sending_longitudes = df['sending_coordinates'].apply(get_longitude)
        delivery_latitudes = df['delivery_coordinates'].apply(get_latitude)
        delivery_longitudes = df['delivery_coordinates'].apply(get_longitude)

        df['sending_latitude'] = np.asarray(sending_latitudes, dtype=float)
        df['sending_longitude'] = np.asarray(sending_longitudes, dtype=float)
        df['delivery_latitude'] = np.asarray(delivery_latitudes, dtype=float)
        df['delivery_longitude'] = np.asarray(delivery_longitudes, dtype=float)
        return df


class DeliveryTypeCleaner(TransformerMixin):
    def transform(self, df: pd.DataFrame):
        return df.replace({
            'List polecony ekonomiczny': 'Economy registered letter',
            'List polecony priorytetowy': 'Priority registered letter',
            'business letter, registered': 'Business registered letter'
        })


class VehicleTransportStrFormat(TransformerMixin):

    def formatter(self, time: str) -> str:
        if time == '0':
            return '0 hr 0 min'
        if not 'min' in time:
            time = time + ' 0 min'
        if not 'hr' in time:
            time = '0 hr ' + time
        return time

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['vehicle_travel_time'] = df['vehicle_travel_time'].apply(self.formatter)
        return df


class FeaturesAdder(TransformerMixin):
    SENDING_COORD_IX = 10
    DELIVERY_COORD_IX = 11
    SENDING_DATE_IX = 0
    DISTANCE_IX = 9

    @staticmethod
    def parse_weekday(date_str: str) -> int:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').weekday()

    @staticmethod
    def get_hour_category(date_str) -> int:
        return int(datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').hour >= 15)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        distances = [float(x[:-2]) if x != "0" else 0.0 for x in df.values[:, self.DISTANCE_IX]]
        df['sending_weekday'] = df['sending_date'].apply(self.parse_weekday)
        df['sending_hour_category'] = df['sending_date'].apply(self.get_hour_category)
        df['distance'] = np.asarray(distances, dtype=float)
        df['sending_date'] = df['sending_date'].apply(lambda str_date: datetime.datetime.strptime(str_date, '%Y-%m-%d '
                                                                                                            '%H:%M:%S'))
        df['delivery_date'] = df['delivery_date'].apply(lambda str_date: datetime.datetime.strptime(str_date, '%Y-%m'
                                                                                                              '-%d '
                                                                                                              '%H:%M:%S'))
        durations = (df['delivery_date'] - df['sending_date'])
        df['delivery_time_hours'] = [d.total_seconds() / 3600 for d in durations]
        df = VehicleTransportStrFormat().transform(df)
        # parse from string
        df['vehicle_travel_time'] = df['vehicle_travel_time'].apply(lambda str_date: datetime.datetime.strptime(str_date, '%H hr %M min'))
        # convert to timedelta
        df['vehicle_travel_time'] = df['vehicle_travel_time'].apply(lambda dt: datetime.timedelta(hours=dt.hour, minutes=dt.minute).total_seconds() / 3660)

        return df


def main(save_path=PREPARED_DATA_PATH, address_path=ADDRESSES_DATA_PATH, raw_path=RAW_DATA_PATH):
    raw_df = pd.read_csv(raw_path, sep=';')
    raw_df = CoordinatesMergeTransformer(address_path).transform(raw_df)
    raw_df = DeliveryTypeCleaner().transform(raw_df)

    raw_df = FeaturesAdder().transform(raw_df)
    mail_df = raw_df[['sending_latitude', 'sending_longitude', 'delivery_latitude', 'delivery_longitude',
                      'distance', 'sending_weekday', 'delivery_type', 'sending_hour_category', 'vehicle_travel_time',
                      'delivery_time_hours']]
    mail_df.to_csv(save_path)
    print(mail_df.corr().to_string())


if __name__ == "__main__":
    main()
