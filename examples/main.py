import pandas as pd
from predictor.deliverypredictor import predictor
from joblib import load
from sklearn.utils import shuffle
from tensorflow.keras.models import load_model

'''
    TODO:
    
    predictor/deliverypredictor/predictor.py modify predict method
    model saved in models/nn.h5
    pipeline saved in models/pipeline.pkl
'''


def main():
    model = load_model('../models/nn.h5')
    pipeline = load('../models/pipeline.pkl')
    delivery_predictor = predictor.DeliveryPredictor(model, pipeline)
    mail_prep_df = pd.read_csv('../data/mail_prep.csv')
    mail_prep_df = shuffle(mail_prep_df)
    sample = mail_prep_df.values[:10, 1:-1]
    predictions = delivery_predictor.predict(sample)
    print(predictions)


if __name__ == "__main__":
    main()