import re
import unittest
import datetime

from predictor.maillogic import mail
from predictor.maillogic.mailRepo import MailRepository
from predictor.maillogic.mail import Mail


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._repository = MailRepository()
        self._sending_date = datetime.datetime(2021, 6, 30, 13, 49, 0)
        self._delivery_type = mail.EconomicRegisteredLetter()
        self._distance = 21.37
        self._post_office_type = mail.FUP()
        self._vehicle_travel_time = 3.2
        self._mails = [
            Mail(self._delivery_type, "0", self._sending_date,
                 'Address 1', 'Address 2', self._post_office_type, self._distance
                 , self._vehicle_travel_time),
            Mail(self._delivery_type, "1", self._sending_date,
                 'Address 1', 'Address 2', self._post_office_type, self._distance
                 , self._vehicle_travel_time),
            Mail(self._delivery_type, "2", self._sending_date,
                 'Address 1', 'Address 2', self._post_office_type, self._distance
                 , self._vehicle_travel_time),
            Mail(self._delivery_type, "3", self._sending_date,
                 'Address 1', 'Address 2', self._post_office_type, self._distance
                 , self._vehicle_travel_time)
        ]

    def test_add_remove(self):
        for m in self._mails:
            self._repository.add(m)
        for ID in range(4):
            self.assertEqual(self._repository.get(str(ID)), self._mails[ID])
            with self.subTest():
                self.assertEqual(self._repository.get(str(ID)), self._mails[ID])
        with self.assertRaises(Exception):
            self._repository.add(self._mails[0])
        self.assertSetEqual(set(self._repository.get_all()), set(self._mails))

        for ID in range(4):
            self._repository.remove(str(ID))
        self.assertListEqual(self._repository.get_all().tolist(), [])

    def test_find_by(self):
        for m in self._mails:
            self._repository.add(m)

        def regex_predicate(m):
            return re.search("[0-9]", m.get_mail_id())

        def regex_neg_predicate(m):
            return re.search("[a-z]", m.get_mail_id())

        self.assertSetEqual(set(self._repository.find_by(regex_predicate)), set(self._mails))
        self.assertListEqual(self._repository.find_by(regex_neg_predicate).tolist(), [])


if __name__ == '__main__':
    unittest.main()
