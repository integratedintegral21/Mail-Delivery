import datetime
from abc import ABC
from abc import abstractmethod
from predictor.preproessdata import preprocessor


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances


class DeliveryType(ABC, metaclass=Singleton):
    @abstractmethod
    def __str__(self):
        pass


class EconomicRegisteredLetter(DeliveryType, metaclass=Singleton):
    def __str__(self):
        return "Economic Registered Letter"


class PriorityRegisteredLetter(DeliveryType, metaclass=Singleton):
    def __str__(self):
        return "Priority Registered Letter"


class PostOfficeType(ABC, metaclass=Singleton):
    @abstractmethod
    def __str__(self):
        pass


class FUP(PostOfficeType, metaclass=Singleton):
    def __str__(self):
        return "FUP"


class UP(PostOfficeType, metaclass=Singleton):
    def __str__(self):
        return "UP"


class AP(PostOfficeType, metaclass=Singleton):
    def __str__(self):
        return "AP"


class PP(PostOfficeType, metaclass=Singleton):
    def __str__(self):
        return "PP"


class Mail:
    def __init__(self, delivery_type: DeliveryType, mail_id, sending_date: datetime.datetime, sending_location: str,
                 destination_location: str, post_office_type, distance: float,
                 vehicle_transport_time: float, sending_hour_category: int):
        self._delivery_type = delivery_type
        self._mail_id = mail_id
        self._sending_date = sending_date
        self._sending_location = sending_location
        self._destination_location = destination_location
        self._post_office_type = post_office_type
        self._delivery_date = None
        self._is_delivered = False
        self._distance = distance
        self._vehicle_transport_time = vehicle_transport_time

    def deliver_mail(self, delivery_date: datetime.datetime) -> None:
        if delivery_date < self._sending_date:
            raise ValueError('Delivery date must be later than sending date')
        self._delivery_date = delivery_date
        self._is_delivered = True

    def is_delivered(self) -> bool:
        return self._is_delivered

    def get_features_list(self) -> list:
        return [
            self._distance,
            self._sending_date.weekday(),
            self._delivery_date.__str__(),
            self._post_office_type.__str__(),
            preprocessor.Preprocessor.get_hour_category(self._sending_date),
            self._vehicle_transport_time,
            self._sending_date.hour
                ]

    def get_label(self):
        if self.is_delivered():
            return preprocessor.Preprocessor.get_delivery_time_hours(self._sending_date, self._delivery_date)
