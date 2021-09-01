from joblib import dump
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

PREPARED_DATA_PATH = '../data/mail_prep.csv'
FOREST_MODEL_PATH = '../models/random_forest.pkl'
PIPELINE_PATH = '../models/pipeline.pkl'


def main():
    mail_df = pd.read_csv(PREPARED_DATA_PATH)
    mail_labels = mail_df['delivery_time']
    cat_attributes = ['delivery_type', 'sending_weekday']
    num_attributes = ['sending_latitude', 'sending_longitude', 'delivery_latitude', 'delivery_longitude', 'distance']
    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler())
    ])
    full_pipeline = ColumnTransformer([
        ('num', num_pipeline, num_attributes),
        ('cat', OneHotEncoder(), cat_attributes)
    ])
    mail_prepared = full_pipeline.fit_transform(mail_df[cat_attributes + num_attributes])
    X_train, X_test, y_train, y_test = train_test_split(mail_prepared, mail_labels, test_size=0.2, random_state=42)
    forest_reg = RandomForestRegressor()
    forest_reg.fit(X_train, y_train)
    print('validation mse:\n' + str(mean_squared_error(y_test, forest_reg.predict(X_test))))
    dump(forest_reg, FOREST_MODEL_PATH)
    dump(full_pipeline, PIPELINE_PATH)


if __name__ == "__main__":
    main()
