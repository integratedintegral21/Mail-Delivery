import pandas as pd
import numpy as np


MAIL_DATA_PATH = 'data2.csv'
ROUTES_FILE_PATH = 'routes.csv'


def get_distinct_routes(mail_df):
    locations_df = mail_df[['sending_location', 'delivery_location']]
    routes = pd.Series([(x[0], x[1]) for x in locations_df.to_numpy()])
    distinct_routes = routes.unique()
    return distinct_routes


def split_routes_into_columns(routes_df: pd.DataFrame) -> pd.DataFrame:
    sending_locations = routes_df['route'].apply(lambda x: x[0])
    delivery_locations = routes_df['route'].apply(lambda x: x[1])
    routes_df['sending_location'] = sending_locations
    routes_df['delivery_location'] = delivery_locations
    routes_df.drop(columns=['route'], inplace=True)
    return routes_df


def main():
    mail_df = pd.read_csv(MAIL_DATA_PATH, sep=';')
    print('Read ' + str(len(mail_df)) + ' mails')
    mail_df = mail_df[mail_df['delivery_location'] != 'nie doszedl']
    print('Parsed ' + str(len(mail_df)) + ' routes')
    distinct_routes = get_distinct_routes(mail_df)
    routes_df = pd.DataFrame(data={'route': distinct_routes})
    routes_df = split_routes_into_columns(routes_df)
    print('Found ' + str(len(routes_df)) + ' distinct routes')
    routes_df.to_csv(ROUTES_FILE_PATH, sep=';')


if __name__ == "__main__":
    main()
