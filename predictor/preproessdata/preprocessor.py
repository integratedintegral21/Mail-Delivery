from preprocess.saveCoordinates import get_coordinates
import datetime


class Preprocessor:
    ALLOWED_DELIVERY_TYPES = ['List polecony priorytetowy', 'List polecony ekonomiczny',
                              'Economy registered letter',
                              'Przesyłka firmowa polecona zamiejscowa',
                              'business letter, registered', 'Priority registered letter',
                              'Przesyłka firmowa polecona miejscowa',
                              'Przesyłka firmowa polecona zamiejscowa priorytetowa']

    DEFAULT_DELIVERY_TYPE = 'List polecony ekonomiczny'

    @staticmethod
    def get_address_coordinates(address: str) -> (float, float):
        return get_coordinates(address)

    @staticmethod
    def get_hour_category(dt: datetime.datetime) -> int:
        return dt.hour >= 15

    @staticmethod
    def get_vehicle_transport_time(location1: str, location2: str) -> datetime.time:
        pass
