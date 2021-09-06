import numpy as np
from joblib import dump
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

PREPARED_DATA_PATH = '../data/mail_prep.csv'
FOREST_MODEL_PATH = '../models/random_forest.pkl'
PIPELINE_PATH = '../models/pipeline.pkl'


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
    cat_attributes = ['sending_weekday', 'delivery_type']
    num_attributes = ['distance', 'vehicle_travel_time']
    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler())
    ])
    full_pipeline = ColumnTransformer([
        ('num', num_pipeline, num_attributes),
        ('cat', OneHotEncoder(), cat_attributes)
    ])
    mail_features = mail_df[num_attributes + cat_attributes]
    mail_prepared = full_pipeline.fit_transform(mail_features).toarray()
    sending_hours_categories = mail_df['sending_hour_category'].to_numpy()
    mail_prepared = np.append(mail_prepared, np.c_[sending_hours_categories], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(mail_prepared, mail_labels, test_size=0.2, random_state=42)
    '''
    forest_reg = RandomForestRegressor()
    forest_reg.fit(X_train, y_train)
    print('training mse:\n' + str(mean_squared_error(y_train, forest_reg.predict(X_train))))
    print('validation mse:\n' + str(mean_squared_error(y_test, forest_reg.predict(X_test))))
    dump(forest_reg, FOREST_MODEL_PATH)
    dump(full_pipeline, PIPELINE_PATH)
    '''
    model = Sequential([
        InputLayer(input_shape=(15,)),
        Dense(50, activation='relu'),
        Dense(50, activation='relu'),
        Dense(50, activation='relu'),
        Dense(50, activation='relu'),
        Dense(50, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=1000, callbacks=[
        EarlyStopping(patience=10),
        LearningRateScheduler(scheduler)
    ])


if __name__ == "__main__":
    main()
