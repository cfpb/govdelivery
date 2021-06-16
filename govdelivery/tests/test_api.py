import base64
import unittest
from unittest.mock import patch

import responses
from requests.models import Response

from govdelivery.api import (
    GovDelivery,
    authenticated_session,
    get_full_url_to_call,
)
from govdelivery.tests.utils import load_data
from govdelivery.xml_response_parsers import topic_xml_as_dict


class TestClientUtilities(unittest.TestCase):
    @patch('os.getenv', return_value=None)
    def test_get_full_url_to_call_with_default_base_url(self, _):
        self.assertEqual(
            get_full_url_to_call('/foo/bar'),
            'https://api.govdelivery.com/foo/bar'
        )

    @patch('os.getenv', return_value='https://envvar.govdelivery.com')
    def test_get_full_url_to_call_with_env_var_defined_base_url(self, _):
        self.assertEqual(
            get_full_url_to_call('/foo/bar'),
            'https://envvar.govdelivery.com/foo/bar'
        )

    def test_get_full_url_to_call_with_passed_base_url(self):
        self.assertEqual(
            get_full_url_to_call(
                '/foo/bar',
                base_url='https://passed.govdelivery.com'
            ),
            'https://passed.govdelivery.com/foo/bar'
        )

    def test_authenticated_session(self):
        session = authenticated_session('username', 'password')
        self.assertEqual(session.auth, ('username', 'password'))

    def test_authenticated_api_call(self):
        # There is no meaningful way to directly test this method, and it
        # should get covered anyway by testing the other methods that call it.
        pass


class TestGovDelivery(unittest.TestCase):
    def setUp(self):
        self.gd = GovDelivery(
            username='abc@xyz.123',
            password='mycatsname',
            account_code='XYZ'
        )

    def test_translate_path(self):
        path = self.gd.translate_path('/api/account/$account_code/topics.xml')
        self.assertEqual(path, '/api/account/XYZ/topics.xml')

    @responses.activate
    def test_call_api_no_parser_returns_unparsed(self):
        path = self.gd.translate_path('/api/account/$account_code/topics.xml')
        mockResponseBody = load_data('list_all_topics.xml')
        responses.add(
            responses.GET,
            get_full_url_to_call(path),
            body=mockResponseBody,
            status=200
        )
        response = self.gd.call_api(path, 'get')
        self.assertIsInstance(response, Response)

    @responses.activate
    def test_call_api_with_parser_returns_parsed(self):
        path = self.gd.translate_path('/api/account/$account_code/topics.xml')
        mockResponseBody = load_data('list_all_topics.xml')
        responses.add(
            responses.GET,
            get_full_url_to_call(path),
            body=mockResponseBody,
            status=200
        )
        parsed_response = self.gd.call_api(
            path,
            'get',
            response_parser=topic_xml_as_dict
        )
        self.assertEqual(
            parsed_response,
            {'XYZ_998': 'Test Unlisted Topic', 'XYZ_999': 'Test Topic'}
        )

    @responses.activate
    def test_get_all_topics(self):
        path = self.gd.translate_path('/api/account/$account_code/topics.xml')
        mockResponseBody = load_data('list_all_topics.xml')
        responses.add(
            responses.GET,
            get_full_url_to_call(path),
            body=mockResponseBody,
            status=200
        )
        response = self.gd.get_all_topics()
        self.assertEqual(
            response,
            {'XYZ_998': 'Test Unlisted Topic', 'XYZ_999': 'Test Topic'}
        )

    @responses.activate
    def test_get_visible_topics(self):
        path = self.gd.translate_path('/api/account/$account_code/topics.xml')
        mockResponseBody = load_data('list_all_topics.xml')
        responses.add(
            responses.GET,
            get_full_url_to_call(path),
            body=mockResponseBody,
            status=200
        )
        response = self.gd.get_visible_topics()
        self.assertEqual(response, {'XYZ_999': 'Test Topic'})

    @responses.activate
    def test_get_subscriber_topics(self):
        email = 'test@example.com'
        subscriber_id = base64.b64encode(email.encode('utf-8'))
        path = self.gd.translate_path(
            '/api/account/$account_code/subscribers/$subscriber_id/topics.xml',
            subscriber_id=subscriber_id
        )
        mockResponseBody = load_data('list_subscriber_topics.xml')
        responses.add(
            responses.GET,
            get_full_url_to_call(path),
            body=mockResponseBody,
            status=200
        )
        response = self.gd.get_subscriber_topics('test@example.com')
        self.assertIn('XYZ_999', response)
