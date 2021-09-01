import pandas as pd
from predictor.deliverypredictor import predictor
from joblib import load


def main():
    model = load('../models/random_forest.pkl')
    pipeline = load('../models/pipeline.pkl')
    delivery_predictor = predictor.DeliveryPredictor(model, pipeline)
    sample = pd.read_csv('../data/mail_prep.csv').values[:10, 1:-1]
    predictions = delivery_predictor.predict(sample)
    print(predictions)


if __name__ == "__main__":
    main()