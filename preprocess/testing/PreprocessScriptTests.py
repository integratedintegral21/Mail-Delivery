import unittest
import pandas as pd
from preprocess import preprocess
import os
import numpy as np


class PreprocessScriptTestCase(unittest.TestCase):
    RAW_DATA_PATH = '../../data/data.csv'
    ADDRESSES_DATA_PATH = '../../data/addresses.csv'
    MAIL_PREP_DST = 'tmp/mail_prep.csv'

    TEST_RAW_DATA_PATH = 'test_cases/test_raw.csv'
    TEST_ADDRESSES_DATA_PATH = 'test_cases/test_addresses.csv'
    TEST_PREP_PATH = 'tmp/test_mail_prep.csv'

    EXPECTED_COLUMNS = ['sending_latitude', 'sending_longitude', 'delivery_latitude', 'delivery_longitude', 'distance',
                        'sending_weekday', 'delivery_type', 'sending_hour_category', 'delivery_time_hours']
    EXPECTED_TYPES = {'sending_latitude': np.float,
                      'sending_longitude': np.float,
                      'delivery_latitude': np.float,
                      'delivery_longitude': np.float,
                      'distance': np.int,
                      'sending_weekday': np.int,
                      'delivery_type': np.object,
                      'sending_hour_category': np.int,
                      'delivery_time_hours': np.int
                      }

    EXPECTED_DELIVERY_TIMES = [
        48 + 9 / 60,
        42 + 54 / 60,
        20 + 3 / 60,
        19 + 9 / 60,
        18 + 55 / 60,
        116 + 53 / 60,
        22 + 21 / 60,
        19 + 27 / 60,
        21 + 35 / 60,
        114 + 10 / 60,
    ]

    def setUp(self) -> None:
        preprocess.main(self.MAIL_PREP_DST, self.ADDRESSES_DATA_PATH, self.RAW_DATA_PATH)
        preprocess.main(self.TEST_PREP_PATH, self.TEST_ADDRESSES_DATA_PATH, self.TEST_RAW_DATA_PATH)
        self.mail_prep = pd.read_csv(self.MAIL_PREP_DST)
        self.test_mail_prep = pd.read_csv(self.TEST_PREP_PATH)

    def tearDown(self) -> None:
        os.remove(self.MAIL_PREP_DST)
        os.remove(self.TEST_PREP_PATH)

    def test_features_presence(self):
        for ft in self.EXPECTED_COLUMNS:
            with self.subTest(msg=ft):
                self.assertIn(ft, self.mail_prep.columns)

    def test_features_types(self):
        for (col_name, col_type) in self.EXPECTED_TYPES.items():
            converted = np.asarray(self.mail_prep[col_name], dtype=col_type)
            with self.subTest():
                self.assertEqual(converted.dtype, col_type)

    def test_delivery_time(self):
        actual_delivery_times = self.test_mail_prep['delivery_time_hours']
        self.assertListEqual(self.test_mail_prep['delivery_time_hours'], self.EXPECTED_DELIVERY_TIMES)


if __name__ == '__main__':
    unittest.main()
