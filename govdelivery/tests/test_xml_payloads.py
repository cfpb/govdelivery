import unittest

from govdelivery.xml_payloads import (
    create_subscriber,
    format_phone,
    set_subscriber_categories,
    set_subscriber_topics,
)


class TestXMLPayloadUtils(unittest.TestCase):
    def test_format_phone_removes_plus_one_and_all_non_digits(self):
        phone = '+1 (234) 567-8901'
        self.assertEqual('2345678901', format_phone(phone))

    def test_format_phone_removes_leading_one_and_all_non_digits(self):
        phone = '1 (234) 567-8901'
        self.assertEqual('2345678901', format_phone(phone))


class TestXMLPayloadGenerators(unittest.TestCase):
    def test_create_subscriber_with_email(self):
        contact_details = 'mail@example.com'
        payload = create_subscriber(contact_details)
        self.assertIn('<email>mail@example.com</email>', payload)

    def test_create_subscriber_with_phone(self):
        contact_details = '2345678901'
        contact_method = 'phone'
        payload = create_subscriber(contact_details, contact_method)
        self.assertIn('<phone>2345678901</phone>', payload)

    def test_set_subscriber_categories(self):
        codes = ['XYZ_C1', 'XYZ_C2']
        payload = set_subscriber_categories(codes)
        self.assertIn('<code>XYZ_C1</code>', payload)
        self.assertIn('<code>XYZ_C2</code>', payload)

    def test_set_subscriber_topics_with_email(self):
        contact_details = 'mail@example.com'
        codes = ['XYZ_1', 'XYZ_2']
        payload = set_subscriber_topics(codes, contact_details)
        self.assertIn('<email>mail@example.com</email>', payload)
        self.assertIn('<code>XYZ_1</code>', payload)
        self.assertIn('<code>XYZ_2</code>', payload)

    def test_set_subscriber_topics_with_phone(self):
        contact_details = '2345678901'
        contact_method = 'phone'
        codes = ['XYZ_1', 'XYZ_2']
        payload = set_subscriber_topics(codes, contact_details, contact_method)
        self.assertIn('<phone>2345678901</phone>', payload)
        self.assertIn('<code>XYZ_1</code>', payload)
        self.assertIn('<code>XYZ_2</code>', payload)
