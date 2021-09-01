import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from ast import literal_eval as make_tuple
import datetime
from sklearn.utils import shuffle
from sklearn.feature_selection import SelectorMixin

RAW_DATA_PATH = '../data/data.csv'
ADDRESSES_DATA_PATH = '../data/addresses.csv'
PREPARED_DATA_PATH = '../data/mail_prep.csv'


class SelectMailFeaturesTransformer(SelectorMixin):
    SENDING_COORD_IX = 10
    DELIVERY_COORD_IX = 11
    DISTANCE_IX = 9
    SENDING_DATE_IX = 0
    DELIVERY_TYPE_IX = 4

    def _get_support_mask(self):
        mask = np.zeros((12,))
        mask[[self.SENDING_DATE_IX, self.DELIVERY_COORD_IX, self.DISTANCE_IX, self.SENDING_DATE_IX,
              self.DELIVERY_TYPE_IX]] = 1
        return mask

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def get_latitude(coords):
            return coords[0]

        def get_longitude(coords):
            return coords[1]

        sending_latitudes = [get_latitude(x) for x in X[:, self.SENDING_COORD_IX]]
        sending_longitudes = [get_longitude(x) for x in X[:, self.SENDING_COORD_IX]]
        delivery_latitudes = [get_latitude(x) for x in X[:, self.DELIVERY_COORD_IX]]
        delivery_longitudes = [get_longitude(x) for x in X[:, self.DELIVERY_COORD_IX]]

        sending_weekdays = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday()
                            for x in X[:, self.SENDING_DATE_IX]]
        sending_hour_category = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour >= 15
                                 for x in X[:, self.SENDING_DATE_IX]]

        distances = [float(x[:-2]) if x != "0" else 0.0 for x in X[:, self.DISTANCE_IX]]
        return np.c_[sending_latitudes, sending_longitudes, delivery_latitudes, delivery_longitudes, distances,
                     sending_weekdays, X[:, self.DELIVERY_TYPE_IX], sending_hour_category]


def add_categories(df: pd.DataFrame) -> np.ndarray:
    ordinal_encoder = OneHotEncoder()
    mail_cat = df[['delivery_type']]
    mail_cat_encoded = ordinal_encoder.fit_transform(mail_cat).toarray()
    return mail_cat_encoded


def main(save_path=PREPARED_DATA_PATH, address_path=ADDRESSES_DATA_PATH, raw_path=RAW_DATA_PATH):
    raw_df = pd.read_csv(raw_path, sep=';')

    addresses_df = pd.read_csv(address_path).dropna()
    addresses_df['Coordinates'] = addresses_df['Coordinates'].apply(make_tuple)

    raw_df = pd.merge(raw_df, addresses_df, left_on='sending_location', right_on='Address')
    raw_df = pd.merge(raw_df, addresses_df, left_on='delivery_location', right_on='Address')
    raw_df.drop(columns=['Address_x', 'Address_y', 'Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)
    raw_df.rename(columns={'Coordinates_x': 'sending_coordinates', 'Coordinates_y': 'delivery_coordinates'},
                  inplace=True)

    raw_df.dropna(inplace=True)
    raw_df = shuffle(raw_df)
    mail_labels = np.array(raw_df['delivery_time'].tolist())
    features_selector = SelectMailFeaturesTransformer()
    selected_features = features_selector.fit_transform(raw_df.values)
    mail_df = pd.DataFrame(data={
        'sending_latitude': np.asarray(selected_features[:, 0], dtype=float),
        'sending_longitude': np.asarray(selected_features[:, 1], dtype=float),
        'delivery_latitude': np.asarray(selected_features[:, 2], dtype=float),
        'delivery_longitude': np.asarray(selected_features[:, 3], dtype=float),
        'distance': np.asarray(selected_features[:, 4], dtype=float),
        'sending_weekday': np.asarray(selected_features[:, 5], dtype=int),
        'delivery_type': selected_features[:, 6],
        'sending_hour_category': np.asarray(selected_features[:, 7], dtype=int),
        'delivery_time': mail_labels
    })
    mail_df.to_csv(save_path)


if __name__ == "__main__":
    main()
