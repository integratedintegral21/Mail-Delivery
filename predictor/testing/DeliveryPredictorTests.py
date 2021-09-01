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

    def test_constructor(self) -> None:
        self.assertTrue(self.predictor is not None)

    def test_predictions(self) -> None:
        mail_df = pd.read_csv(self.PREPARED_DATA_PATH)
        mail_list = mail_df.values[:, 1:-1]
        delivery_boundaries = self.predictor.predict(mail_list)


if __name__ == '__main__':
    unittest.main()
