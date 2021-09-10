import datetime
import re
import unittest

import numpy as np

from predictor.maillogic import mail
from predictor.maillogic.factory import MailFactory
from predictor.preproessdata import preprocessor


class FactoryCase(unittest.TestCase):
    def setUp(self) -> None:
        self._sending_date = datetime.datetime(2021, 6, 30, 13, 49, 0)
        self._delivery_type = mail.EconomicRegisteredLetter()
        self._distance = 21.37
        self._post_office_type = mail.FUP()
        self._vehicle_travel_time = 3.2
        self._mail_factory = MailFactory()

    def test_sending_without_preprocessor(self):
        mail_id = "0"
        self.assertIsNone(self._mail_factory.get(mail_id))
        new_mail = self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id=mail_id,
                                                sending_date=self._sending_date,
                                                sending_location="Address 0", destination_location="Address 1",
                                                post_office_type=self._post_office_type, distance=self._distance,
                                                vehicle_travel_time=self._vehicle_travel_time)
        self.assertEqual(self._mail_factory.get(mail_id), new_mail)
        self.assertSetEqual(set(self._mail_factory.get_all().tolist()), {new_mail})
        with self.assertRaises(Exception):
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id=mail_id,
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time)
        with self.assertRaises(ValueError):
            self._mail_factory.send_mail(delivery_type=MailFactory(), mail_id="1",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time)
        with self.assertRaises(ValueError):
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id="1",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=MailFactory(), distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time)
        with self.assertRaises(ValueError):
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id="1",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=-1,
                                         vehicle_travel_time=self._vehicle_travel_time)

    def test_deliver(self):
        mail_id = "0"
        new_mail = self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id=mail_id,
                                                sending_date=self._sending_date,
                                                sending_location="Address 0", destination_location="Address 1",
                                                post_office_type=self._post_office_type, distance=self._distance,
                                                vehicle_travel_time=self._vehicle_travel_time)
        delivery_date = datetime.datetime(2021, 6, 30, 19, 49, 0)
        self._mail_factory.deliver(delivery_date, mail_id)
        self.assertTrue(new_mail.is_delivered())
        self.assertEqual(new_mail.get_delivery_date(), delivery_date)

    def test_find_by(self):
        mail_id = "0"
        new_mail = self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id=mail_id,
                                                sending_date=self._sending_date,
                                                sending_location="Address 0", destination_location="Address 1",
                                                post_office_type=self._post_office_type, distance=self._distance,
                                                vehicle_travel_time=self._vehicle_travel_time)

        def regex_predicate(m):
            return re.search("[0-9]", m.get_mail_id())

        def regex_neg_predicate(m):
            return re.search("[a-z]", m.get_mail_id())

        self.assertSetEqual(set(self._mail_factory.find_by(regex_predicate)), {new_mail})
        self.assertSetEqual(set(self._mail_factory.find_by(regex_neg_predicate)), set())

    def test_features_list(self):
        mails = [
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id="0",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time),
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id="1",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time),
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id="2",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time),
            self._mail_factory.send_mail(delivery_type=self._delivery_type, mail_id="3",
                                         sending_date=self._sending_date,
                                         sending_location="Address 0", destination_location="Address 1",
                                         post_office_type=self._post_office_type, distance=self._distance,
                                         vehicle_travel_time=self._vehicle_travel_time),
        ]
        delivery_date = datetime.datetime(2021, 6, 30, 19, 49, 0)
        expected_features = 4 * [
            [
                str(self._distance),
                str(self._sending_date.weekday()),
                str(self._delivery_type),
                str(self._post_office_type),
                str(preprocessor.Preprocessor.get_hour_category(self._sending_date)),
                str(self._vehicle_travel_time),
                str(self._sending_date.hour)
            ]
        ]
        actual_features = [f.tolist() for f in self._mail_factory.get_not_delivered_features()]
        actual_delivered_features = [f.tolist() for f in self._mail_factory.get_delivered_features_and_labels()]
        self.assertListEqual(actual_features, expected_features)
        self.assertListEqual(actual_delivered_features, [])
        for ID in range(4):
            self._mail_factory.deliver(delivery_date, str(ID))
        expected_delivered_features_labels = 4 * [
            [
                str(self._distance),
                str(self._sending_date.weekday()),
                str(self._delivery_type),
                str(self._post_office_type),
                str(preprocessor.Preprocessor.get_hour_category(self._sending_date)),
                str(self._vehicle_travel_time),
                str(self._sending_date.hour),
                '6.0'
            ]
        ]
        actual_features = [f.tolist() for f in self._mail_factory.get_not_delivered_features()]
        actual_delivered_features = [f.tolist() for f in self._mail_factory.get_delivered_features_and_labels()]
        self.assertListEqual(actual_delivered_features, expected_delivered_features_labels)
        self.assertListEqual(actual_features, [])


if __name__ == '__main__':
    unittest.main()
