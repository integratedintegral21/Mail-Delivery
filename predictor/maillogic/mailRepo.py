from ctypes import Union
import numpy as np
from predictor.maillogic import mail


class MailRepository:
    def __init__(self):
        self._mail_list = list()

    def add(self, new_mail: mail.Mail) -> None:
        if self.get(new_mail.get_mail_id()) is not None:
            raise Exception('This mail has already been added')
        self._mail_list.append(new_mail)

    def get(self, mail_id):
        for m in self._mail_list:
            if mail_id == m.get_mail_id():
                return m
        return None

    def get_all(self) -> np.array:
        return np.array(self._mail_list)

    def remove(self, mail_id):
        m = self.get(mail_id)
        if m is not None:
            self._mail_list.remove(m)

    def find_by(self, predicate) -> np.array:
        m_list = []
        for m in self._mail_list:
            if predicate(m):
                m_list.append(m)
        return np.array(m_list)

    def get_features_array(self) -> np.array:
        f_list = [m.get_features_list() for m in self._mail_list]
        return np.array(f_list)

    def get_labels_array(self) -> np.array:
        l_list = [m.get_label() for m in self._mail_list]
        return np.array(l_list)
