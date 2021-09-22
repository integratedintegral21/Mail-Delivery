import pandas as pd


MAIL_DATA_PATH = 'data2.csv'
ROUTES_DATA_PATH = 'routes_with_distance.csv'
MERGED_DATA_PATH = 'mail_with_distances.csv'


def clear_routes_df(routes_df: pd.DataFrame) -> pd.DataFrame:
    # reject unknown distances
    routes_df.drop(columns='Unnamed: 0', inplace=True)
    # swap distance and vehicle travel time colmns
    routes_df = routes_df.reindex(columns=['sending_location', 'delivery_location', 'vehicle_travel_time', 'distance'])
    routes_df = routes_df[routes_df['distance'] != '-1']
    routes_df['distance'] = routes_df['distance'].apply(lambda x: x if x == '0' or x[-2:] == 'km' else '0')
    return routes_df


def main():
    routes_df = pd.read_csv(ROUTES_DATA_PATH, sep=';')
    mail_df = pd.read_csv(MAIL_DATA_PATH, sep=';')

    print("Read " + str(len(routes_df)) + " routes")
    routes_df = clear_routes_df(routes_df)
    print("Found " + str(len(routes_df)) + " valid routes")

    print("Read " + str(len(mail_df)) + " mails")
    mail_df = mail_df[mail_df['delivery_date'] != 'nie doszedl']
    print("Found " + str(len(mail_df)) + " delivered mails")

    mails_with_distance = pd.merge(mail_df, routes_df, left_on=['sending_location', 'delivery_location'],
                                   right_on=['sending_location', 'delivery_location'])
    print(mails_with_distance.columns)
    mails_with_distance.to_csv(MERGED_DATA_PATH, sep=';', index=False)


if __name__ == "__main__":
    main()
