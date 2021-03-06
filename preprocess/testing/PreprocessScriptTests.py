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

    EXPECTED_COLUMNS = ['distance', 'sending_weekday', 'delivery_type', 'post_office_type',
                        'sending_hour_category', 'vehicle_travel_time', 'sending_hour', 'delivery_time_hours'
                        ]

    EXPECTED_TYPES = {
        'distance': np.float,
        'sending_weekday': np.int,
        'delivery_type': np.object,
        'sending_hour_category': np.int,
        'delivery_time_hours': np.int,
        'post_office_type': np.object,
        'vehicle_travel_time': np.float
    }

    EXPECTED_DELIVERY_TIMES = [
        24 + 9 / 60,
        42 + 53 / 60,
        20 + 3 / 60,
        19 + 9 / 60,
        18 + 55 / 60,
        116 + 53 / 60,
        22 + 21 / 60,
        19 + 27 / 60,
        21 + 35 / 60,
        114 + 10 / 60,
    ]

    EXPECTED_SENDING_HOURS = [
        14,
        14,
        15,
        15,
        15,
        15,
        15,
        15,
        15,
        15,
    ]

    EXPECTED_POST_OFFICE_TYPE = [
        "FUP",
        "FUP",
        "FUP",
        "FUP",
        "FUP",
        "UP",
        "UP",
        "UP",
        "UP",
        "UP",
    ]

    EXPECTED_WEEKDAYS = 10 * [2]

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
        for i in range(len(actual_delivery_times)):
            with self.subTest():
                self.assertAlmostEqual(actual_delivery_times[i], self.EXPECTED_DELIVERY_TIMES[i], 1)

    def test_sending_hour(self):
        actual_sending_hours = self.test_mail_prep['sending_hour'].to_list()
        self.assertListEqual(self.EXPECTED_SENDING_HOURS, actual_sending_hours)

    def test_sending_hour_category(self):
        actual_sending_hour_categories = self.test_mail_prep['sending_hour_category'].to_list()
        expected_sending_hour_category = [h >= 15 for h in self.EXPECTED_SENDING_HOURS]
        self.assertListEqual(expected_sending_hour_category, actual_sending_hour_categories)

    def test_post_office_category(self):
        actual_post_office_types = self.test_mail_prep['post_office_type'].to_list()
        self.assertListEqual(self.EXPECTED_POST_OFFICE_TYPE, actual_post_office_types)

    def test_sending_weekday(self):
        actual_weekdays = self.test_mail_prep['sending_weekday'].to_list()
        self.assertListEqual(self.EXPECTED_WEEKDAYS, actual_weekdays)


if __name__ == '__main__':
    unittest.main()
