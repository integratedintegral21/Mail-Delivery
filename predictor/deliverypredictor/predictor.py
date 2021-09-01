import numpy as np
import pandas as pd
import sklearn.base
from sklearn.compose import ColumnTransformer


class DeliveryPredictor:
    FEATURES_COUNT = 8

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
                'sending_latitude': np.asarray(mail_data[:, 0], dtype=float),
                'sending_longitude': np.asarray(mail_data[:, 1], dtype=float),
                'delivery_latitude': np.asarray(mail_data[:, 2], dtype=float),
                'delivery_longitude': np.asarray(mail_data[:, 3], dtype=float),
                'distance': np.asarray(mail_data[:, 4], dtype=float),
                'sending_weekday': np.asarray(mail_data[:, 5], dtype=int),
                'delivery_type': mail_data[:, 6],
            })
            mail_prepared = self.pipeline.transform(mail_df)
            mail_prepared = np.append(mail_prepared, np.c_[mail_data[:, 7]], axis=1)
            predictions = [max(round(p), 1) for p in self.model.predict(mail_prepared)]
            delivery_time_boundaries = [(max(p - 1, 1), p + 1) for p in predictions]
            return delivery_time_boundaries

        except ValueError as e:
            raise e
