import pandas as pd
from predictor.deliverypredictor import predictor
from joblib import load
from sklearn.utils import shuffle

'''
    TODO:
    
    w preprocess/preprocess.py w klasie FeaturesAdder (metoda transform) dodaj czas dostarczenia w godzinach (label; 
    roznica pomiędzy czasem dostarczenia a czasem wysłania. Zapisz tabelkę w data/mail_prep.csv
    
    w nowym skrypcie w train/ dodaj trenowanie sieci neuronowej i zapisz w models/
'''


def main():
    model = load('../models/random_forest.pkl')
    pipeline = load('../models/pipeline.pkl')
    delivery_predictor = predictor.DeliveryPredictor(model, pipeline)
    mail_prep_df = pd.read_csv('../data/mail_prep.csv')
    mail_prep_df = shuffle(mail_prep_df)
    sample = mail_prep_df.values[:10, 1:-1]
    predictions = delivery_predictor.predict(sample)
    print(predictions)


if __name__ == "__main__":
    main()