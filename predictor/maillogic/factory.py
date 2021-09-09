import datetime
import numpy as np
from predictor.maillogic.mailRepo import MailRepository
from predictor.maillogic.mail import Mail, DeliveryType


class MailFactory:

    def __init__(self):
        self._sent_mail_repository = MailRepository()
        self._delivered_mail_repository = MailRepository()

    """
        Determine distance, vehicle travel time and check if a mail with mail_id is not in the repo,
        return the new object
    """
    def send_mail(self, delivery_type: type(DeliveryType), mail_id: str, sending_date: datetime.datetime,
                  sending_location: str, destination_location: str, post_office_type) -> Mail:
        pass

    def get(self, mail_id) -> Mail:
        sent = self._sent_mail_repository.get(mail_id)
        if sent is None:
            return self._delivered_mail_repository.get(mail_id)
        return sent

    def get_all(self) -> np.array:
        return np.append(self._sent_mail_repository.get_all(), self._sent_mail_repository.get_all())

    def find_by(self, predicate) -> np.array:
        return np.append(self._sent_mail_repository.find_by(predicate), self._sent_mail_repository.find_by(predicate))

    def deliver(self, delivery_date: datetime.datetime, mail_id) -> None:
        m = self._sent_mail_repository.get(mail_id)
        if m is None:
            raise Exception('Cannot find mail with given id')
        m.deliver_mail(delivery_date)
        self._sent_mail_repository.remove(mail_id)
        self._delivered_mail_repository.add(m)
