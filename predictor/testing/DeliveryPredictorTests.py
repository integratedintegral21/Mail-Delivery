import unittest

import pandas as pd
from joblib import load
from predictor.deliverypredictor.predictor import DeliveryPredictor
from tensorflow.keras.models import load_model


class DeliveryPredictorTest(unittest.TestCase):

    MODEL_PATH = '../../models/nn.h5'
    TRANSFORMER_PATH = '../../models/pipeline.pkl'
    PREPARED_DATA_PATH = '../../data/mail_prep.csv'

    RAW_DATA_PATH = '../../data/data.csv'
    ADDRESS_DATA_PATH = '../../data/addresses.csv'

    def setUp(self) -> None:
        self.model = load_model(self.MODEL_PATH)
        self.pipeline = load(self.TRANSFORMER_PATH)
        self.predictor = DeliveryPredictor(self.model, self.pipeline)
        self.mail_df = pd.read_csv(self.PREPARED_DATA_PATH, sep=';')

    def test_constructor(self) -> None:
        self.assertTrue(self.predictor is not None)

    def test_predictions_exceptions(self) -> None:
        incorrect_mail_list = self.mail_df.values[:, 0:-1]
        with self.assertRaises(ValueError):
            self.predictor.predict(incorrect_mail_list)


if __name__ == '__main__':
    unittest.main()
