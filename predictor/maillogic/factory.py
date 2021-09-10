import datetime
import numpy as np
from predictor.maillogic.mailRepo import MailRepository
from predictor.maillogic.mail import Mail, DeliveryType, PostOfficeType
from predictor.preproessdata import preprocessor


class MailFactory:

    def __init__(self):
        self._sent_mail_repository = MailRepository()
        self._delivered_mail_repository = MailRepository()

    """
        Determine distance, vehicle travel time (if not given) and check if a mail with mail_id is not in the repo,
        return the new object
    """
    def send_mail(self, delivery_type: type(DeliveryType), mail_id: str, sending_date: datetime.datetime,
                  sending_location: str, destination_location: str, post_office_type: type(PostOfficeType),
                  distance=None, vehicle_travel_time=None) -> Mail:
        if distance is None or vehicle_travel_time is None:
            distance = preprocessor.Preprocessor.get_distance(sending_location, destination_location)
            vehicle_travel_time = preprocessor.Preprocessor.get_vehicle_transport_time_hours(sending_location,
                                                                                             destination_location)
        if not issubclass(type(delivery_type), DeliveryType):
            raise ValueError('Delivery type incorrect (must inherit from DeliveryType)')
        if self._sent_mail_repository.get(mail_id) or self._delivered_mail_repository.get(mail_id):
            raise Exception('The mail with given id has already been sent')
        if not issubclass(type(post_office_type), PostOfficeType):
            raise ValueError('Post office type incorrect (must inherit from PostOfficeType')
        if distance < 0:
            raise ValueError('Distance must be a non-negative number')
        new_mail = Mail(delivery_type, mail_id, sending_date, sending_location, destination_location, post_office_type,
                        distance, vehicle_travel_time)
        self._sent_mail_repository.add(new_mail)
        return new_mail

    def get(self, mail_id) -> Mail:
        sent = self._sent_mail_repository.get(mail_id)
        if sent is None:
            return self._delivered_mail_repository.get(mail_id)
        return sent

    def get_all(self) -> np.array:
        return np.append(self._sent_mail_repository.get_all(), self._delivered_mail_repository.get_all())

    def find_by(self, predicate) -> np.array:
        return np.append(self._sent_mail_repository.find_by(predicate),
                         self._delivered_mail_repository.find_by(predicate))

    def deliver(self, delivery_date: datetime.datetime, mail_id) -> None:
        m = self._sent_mail_repository.get(mail_id)
        if m is None:
            raise Exception('Cannot find mail with given id')
        if delivery_date < m.get_sending_date():
            raise Exception('Given delivery date ')
        m.deliver_mail(delivery_date)
        self._sent_mail_repository.remove(mail_id)
        self._delivered_mail_repository.add(m)

    def get_not_delivered_features(self) -> np.array:
        return self._sent_mail_repository.get_features_array()

    def get_delivered_features_and_labels(self) -> np.array:
        delivered_f = self._delivered_mail_repository.get_features_array()
        if len(delivered_f) > 0:
            delivered_labels = np.array(np.c_[self._delivered_mail_repository.get_labels_array()])
            return np.append(delivered_f, delivered_labels, axis=1)
        return []
