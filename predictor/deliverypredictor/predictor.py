import datetime

import numpy as np
import pandas as pd
import sklearn.base
from sklearn.compose import ColumnTransformer


class DeliveryPredictor:
    FEATURES_COUNT = 7

    def __init__(self, model, pipeline: ColumnTransformer):
        self.model = model
        self.pipeline = pipeline

    '''
        mail_data: [[sending_latitude,sending_longitude,delivery_latitude,
        delivery_longitude,distance,sending_weekday,delivery_type,sending_hour_category], ...]
    '''

    def predict(self, mail_data: np.array) -> [(int, int)]:
        try:
            if len(mail_data.shape) != 2 or mail_data.shape[1] != self.FEATURES_COUNT:
                raise ValueError('mail_data expected to be a 2-dimensional and shaped (*, ' + str(self.FEATURES_COUNT) +
                                 ')')
            mail_df = pd.DataFrame({
                'distance': np.asarray(mail_data[:, 0], dtype=float),
                'vehicle_travel_time': np.asarray(mail_data[:, 5], dtype=float),
                'sending_hour': np.asarray(mail_data[:, 6], dtype=int),
                'sending_weekday': np.asarray(mail_data[:, 1], dtype=int),
                'post_office_type': np.asarray(mail_data[:, 3], dtype=object),
                'delivery_type': np.asarray(mail_data[:, 2], dtype=object),
                'sending_hour_category': np.asarray(mail_data[:, 4], dtype=int),
            })
            mail_prepared = self.pipeline.transform(mail_df)
            predictions = self.model.predict(mail_prepared)
            return predictions

        except ValueError as e:
            raise e
