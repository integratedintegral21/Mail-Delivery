import datetime
from geopy.geocoders import Nominatim

LOC_USER_AGENT = "Google Maps"


class Preprocessor:
    ALLOWED_DELIVERY_TYPES = [
        'Economy registered letter',
        'Priority registered letter',
                              ]

    DEFAULT_DELIVERY_TYPE = 'List polecony ekonomiczny'

    @staticmethod
    def get_address_coordinates(address: str) -> (float, float):
        try:
            geolocator = Nominatim(user_agent=LOC_USER_AGENT)
            location = geolocator.geocode(address)
            print(address + ' ' + str(location.latitude) + ' ' + str(location.longitude))
        except Exception as e:
            print(e.__str__())
            return None

        if location is None:
            return None
        return location.latitude, location.longitude

    @staticmethod
    def get_hour_category(dt: datetime.datetime) -> int:
        return dt.hour >= 15

    @staticmethod
    def get_vehicle_transport_time(location1: str, location2: str) -> datetime.time:
        raise NotImplementedError
