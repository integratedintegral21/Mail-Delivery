import datetime
import unittest
from predictor.maillogic import mail


class MailTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._distance = 21.37

        self._delivery_type_0 = mail.EconomicRegisteredLetter()
        self._delivery_type_1 = mail.PriorityRegisteredLetter()

        self._mail_id = 0

        self._sending_date_0 = datetime.datetime(2021, 6, 29, 13, 49, 0)
        self._sending_date_1 = datetime.datetime(2021, 6, 29, 15, 0, 0)

        self._post_office_type_0 = mail.FUP()
        self._post_office_type_1 = mail.UP()
        self._post_office_type_2 = mail.AP()
        self._post_office_type_3 = mail.PP()

        self._vehicle_travel_time = 3.2

        self._delivery_date_0 = datetime.datetime(2021, 6, 30, 13, 49, 0)
        self._delivery_date_1 = datetime.datetime(2021, 6, 29, 19, 0, 0)

        mail_0 = mail.Mail(self._delivery_type_0, self._mail_id, self._sending_date_0,
                           'Address 1', 'Address 2', self._post_office_type_0, self._distance
                           , self._vehicle_travel_time)
        mail_1 = mail.Mail(self._delivery_type_1, self._mail_id, self._sending_date_1,
                           'Address 1', 'Address 2', self._post_office_type_1, self._distance
                           , self._vehicle_travel_time)
        mail_2 = mail.Mail(self._delivery_type_1, self._mail_id, self._sending_date_1,
                           'Address 1', 'Address 2', self._post_office_type_2, self._distance
                           , self._vehicle_travel_time)
        mail_3 = mail.Mail(self._delivery_type_1, self._mail_id, self._sending_date_1,
                           'Address 1', 'Address 2', self._post_office_type_3, self._distance
                           , self._vehicle_travel_time)
        self._mails = [
            mail_0,
            mail_1,
            mail_2,
            mail_3
        ]

    def test_constructor(self):
        expected_features = {
            self._mails[0]: [self._distance, self._sending_date_0.weekday(), "Economic Registered Letter", "FUP", 0,
                             self._vehicle_travel_time, self._sending_date_0.hour],
            self._mails[1]: [self._distance, self._sending_date_1.weekday(), "Priority Registered Letter", "UP", 1,
                             self._vehicle_travel_time, self._sending_date_1.hour],
            self._mails[2]: [self._distance, self._sending_date_1.weekday(), "Priority Registered Letter", "AP", 1,
                             self._vehicle_travel_time, self._sending_date_1.hour],
            self._mails[3]: [self._distance, self._sending_date_1.weekday(), "Priority Registered Letter", "PP", 1,
                             self._vehicle_travel_time, self._sending_date_1.hour],
        }

        for m, expected_f in expected_features.items():
            actual_features = m.get_features_list()
            with self.subTest():
                self.assertListEqual(expected_f, actual_features)

        for m in self._mails:
            with self.subTest():
                self.assertFalse(m.is_delivered())
                self.assertIsNone(m.get_label())

    def test_delivery(self):
        expected_labels = {
            self._mails[0]: 5 + 11 / 60,
            self._mails[1]: 4.,
            self._mails[2]: 4.,
            self._mails[3]: 4.
        }
        for m in self._mails:
            with self.assertRaises(ValueError):
                m.deliver_mail(datetime.datetime(2020, 6, 29, 15, 0, 0))
            with self.subTest():
                m.deliver_mail(self._delivery_date_1)
            with self.assertRaises(Exception):
                m.deliver_mail(self._delivery_date_1)

        for m, label in expected_labels.items():
            self.assertEqual(m.get_label(), label)


if __name__ == '__main__':
    unittest.main()
