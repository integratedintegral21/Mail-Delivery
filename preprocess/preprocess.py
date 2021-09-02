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
        return df


class FeaturesAdder(TransformerMixin):
    SENDING_COORD_IX = 10
    DELIVERY_COORD_IX = 11
    SENDING_DATE_IX = 0
    DISTANCE_IX = 9

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        def get_latitude(coords):
            return coords[0]

        def get_longitude(coords):
            return coords[1]

        sending_latitudes = [get_latitude(x) for x in df.values[:, self.SENDING_COORD_IX]]
        sending_longitudes = [get_longitude(x) for x in df.values[:, self.SENDING_COORD_IX]]
        delivery_latitudes = [get_latitude(x) for x in df.values[:, self.DELIVERY_COORD_IX]]
        delivery_longitudes = [get_longitude(x) for x in df.values[:, self.DELIVERY_COORD_IX]]
        sending_weekdays = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday()
                            for x in df.values[:, self.SENDING_DATE_IX]]
        sending_hour_categories = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour >= 15
                                 for x in df.values[:, self.SENDING_DATE_IX]]

        distances = [float(x[:-2]) if x != "0" else 0.0 for x in df.values[:, self.DISTANCE_IX]]
        df['sending_latitude'] = np.asarray(sending_latitudes, dtype=float)
        df['sending_longitude'] = np.asarray(sending_longitudes, dtype=float)
        df['delivery_latitude'] = np.asarray(delivery_latitudes, dtype=float)
        df['delivery_longitude'] = np.asarray(delivery_longitudes, dtype=float)
        df['sending_weekday'] = np.asarray(sending_weekdays, dtype=int)
        df['sending_hour_category'] = np.asarray(sending_hour_categories, dtype=int)
        df['distance'] = np.asarray(distances, dtype=int)

        return df


def main(save_path=PREPARED_DATA_PATH, address_path=ADDRESSES_DATA_PATH, raw_path=RAW_DATA_PATH):
    raw_df = pd.read_csv(raw_path, sep=';')
    raw_df = CoordinatesMergeTransformer(address_path).transform(raw_df)

    raw_df = FeaturesAdder().transform(raw_df)
    mail_df = raw_df[['sending_latitude', 'sending_longitude', 'delivery_latitude', 'delivery_longitude', 'distance',
                      'sending_weekday', 'delivery_type', 'sending_hour_category', 'delivery_time']]
    mail_df.to_csv(save_path)


if __name__ == "__main__":
    main()
