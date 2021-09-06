import numpy as np
from joblib import dump
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer, Dropout
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

PREPARED_DATA_PATH = '../data/mail_prep.csv'
FOREST_MODEL_PATH = '../models/random_forest.pkl'
PIPELINE_PATH = '../models/pipeline.pkl'

NN_PATH = '../models/nn.h5'


def scheduler(epochs, lr):
    if lr < 1e-5:
        return lr
    if epochs % 10 == 0:
        return lr / 2
    return lr


def main():
    mail_df = pd.read_csv(PREPARED_DATA_PATH)
    mail_df = shuffle(mail_df)

    mail_labels = mail_df['delivery_time_hours']
    cat_attributes = ['sending_weekday', 'post_office_type']
    num_attributes = ['distance', 'vehicle_travel_time', 'sending_hour']
    ordinal_attributes = ['delivery_type', 'sending_hour_category']

    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler())
    ])
    full_pipeline = ColumnTransformer([
        ('num', num_pipeline, num_attributes),
        ('ord', OrdinalEncoder(), ordinal_attributes),
        ('cat', OneHotEncoder(), cat_attributes),
    ])
    mail_features = mail_df[num_attributes + cat_attributes + ordinal_attributes]
    mail_prepared = full_pipeline.fit_transform(mail_features)
    X_train, X_test, y_train, y_test = train_test_split(mail_prepared, mail_labels, test_size=0.2, random_state=42)
    '''
    forest_reg = RandomForestRegressor()
    forest_reg.fit(X_train, y_train)
    print('training mse:\n' + str(mean_squared_error(y_train, forest_reg.predict(X_train))))
    print('validation mse:\n' + str(mean_squared_error(y_test, forest_reg.predict(X_test))))
    dump(forest_reg, FOREST_MODEL_PATH)
    '''
    model = Sequential([
        Dense(50, activation='relu', kernel_initializer='he_normal', input_shape=(16,)),
        Dropout(0.05),
        Dense(50, activation='relu', kernel_initializer='he_normal'),
        Dropout(0.05),
        Dense(50, activation='relu', kernel_initializer='he_normal'),
        Dropout(0.05),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mae', metrics=['accuracy'])
    model.fit(X_train, y_train, batch_size=32, validation_data=(X_test, y_test), epochs=1000, callbacks=[
        EarlyStopping(patience=10, restore_best_weights=True),
        LearningRateScheduler(scheduler),
    ])
    dump(full_pipeline, PIPELINE_PATH)
    model.save(NN_PATH)


if __name__ == "__main__":
    main()
