import datetime
from enum import Enum


class Mail:
    def __init__(self, delivery_type, mail_id, sending_date: datetime.datetime, sending_location: str,
                 destination_location: str, post_office_type):
        self.delivery_type = delivery_type
        self.mail_id = mail_id
        self.sending_date = sending_date
        self.sending_location = sending_location
        self.destination_location = destination_location
        self.post_office_type = post_office_type
        self.delivery_date = None
        self.is_delivered = False

    def deliver_mail(self, delivery_date: datetime.datetime):
        try:
            if delivery_date < self.sending_date:
                raise ValueError('Delivery date must be later than sending date')
        except ValueError as e:
            print(e.__str__())
            raise e
        self.delivery_date = delivery_date
        self.is_delivered = True

    def get_distance(self):
        raise NotImplementedError

    def get_vehicle_transport_time(self):
        raise NotImplementedError

