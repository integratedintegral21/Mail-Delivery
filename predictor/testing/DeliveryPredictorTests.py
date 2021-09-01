import unittest

import pandas as pd
from joblib import load
from ..deliverypredictor.predictor import DeliveryPredictor


class DeliveryPredictorTest(unittest.TestCase):

    MODEL_PATH = 'models/random_forest.pkl'
    TRANSFORMER_PATH = 'models/pipeline.pkl'
    PREPARED_DATA_PATH = 'data/mail_prep.csv'

    RAW_DATA_PATH = 'data/data.csv'
    ADDRESS_DATA_PATH = 'data/addresses.csv'

    def setUp(self) -> None:
        self.model = load(self.MODEL_PATH)
        self.pipeline = load(self.TRANSFORMER_PATH)
        self.predictor = DeliveryPredictor(self.model, self.pipeline)
        self.mail_df = pd.read_csv(self.PREPARED_DATA_PATH)

    def test_constructor(self) -> None:
        self.assertTrue(self.predictor is not None)

    def test_predictions(self) -> None:
        mail_list = self.mail_df.values[:, 1:-1]
        delivery_boundaries = self.predictor.predict(mail_list)
        for boundary in delivery_boundaries:
            with self.subTest(boundary=boundary):
                self.assertGreaterEqual(boundary[0], 1)
                if boundary[1] == 2:
                    self.assertEqual(boundary[0], 1)
                else:
                    self.assertEqual(boundary[1], boundary[0] + 2)

    def test_predictions_exceptions(self) -> None:
        incorrect_mail_list = self.mail_df.values[:, 0:-1]
        with self.assertRaises(ValueError):
            self.predictor.predict(incorrect_mail_list)


if __name__ == '__main__':
    unittest.main()
