import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from predictor.preproessdata import preprocessor


RAW_DATA_PATH = '../data/data.csv'
ADDRESS_DATA_PATH = '../data/addresses.csv'


def get_coordinates(address: str) -> (np.float, np.float):
    return preprocessor.Preprocessor.get_address_coordinates(address)


def get_and_save_coordinates(addresses: pd.Series, filename: str) -> None:
    cities = addresses.apply(lambda address: address.split(' ')[1] + ', Poland')
    coordinates = cities.apply(get_coordinates)
    addresses_df = pd.DataFrame({'Address': addresses, 'Coordinates': coordinates})
    addresses_df.to_csv(filename)


def main():
    raw_df = pd.read_csv(RAW_DATA_PATH, sep=';')
    addresses = pd.Series(raw_df['delivery_location'].append(raw_df['sending_location']).unique())
    get_and_save_coordinates(addresses, ADDRESS_DATA_PATH)


if __name__ == "__main__":
    main()