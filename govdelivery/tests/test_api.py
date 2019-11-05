import base64
import os
import unittest

import responses
from requests.models import Response

from govdelivery.api import (
    authenticated_session, get_full_url_to_call, GovDelivery
)
from govdelivery.tests.utils import load_data
from govdelivery.xml_response_parsers import topic_xml_as_dict


class TestClientUtilities(unittest.TestCase):
    def test_get_full_url_to_call(self):
        # Store and unset existing GOVDELIVERY_BASE_URL env var, if it is set.
        if os.environ.get('GOVDELIVERY_BASE_URL'):
            current_govdelivery_base = os.environ['GOVDELIVERY_BASE_URL']
            del os.environ['GOVDELIVERY_BASE_URL']

        url_to_call = get_full_url_to_call('/path')
        self.assertEqual(url_to_call, 'https://api.govdelivery.com/path')

        url_to_call = get_full_url_to_call(
            '/path',
            'https://passed-base.govdelivery.com'
        )
        self.assertEqual(
            url_to_call,
            'https://passed-base.govdelivery.com/path'
        )

        os.environ['GOVDELIVERY_BASE_URL'] = 'https://env-base.govdelivery.com'
        url_to_call = get_full_url_to_call('/path')
        self.assertEqual(url_to_call, 'https://env-base.govdelivery.com/path')

        try:
            # Was current_govdelivery_base assigned earlier?
            current_govdelivery_base
        except NameError:
            # No: delete the temporary GOVDELIVERY_BASE_URL env var.
            del os.environ['GOVDELIVERY_BASE_URL']
        else:
            # Yes: Reassign GOVDELIVERY_BASE_URL to what it started out as.
            os.environ['GOVDELIVERY_BASE_URL'] = current_govdelivery_base

    def test_authenticated_session(self):
        session = authenticated_session('username', 'password')
        self.assertEqual(session.auth, ('username', 'password'))

    def test_authenticated_api_call(self):
        # There is no meaningful way to directly test this method, and it
        # should get covered anyway by testing the other methods that call it.
        pass


class TestGovDelivery(unittest.TestCase):
    def setUp(self):
        self.gd = GovDelivery()
        self.gd.account_code = 'XYZ'

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
        subscriber_id = base64.b64encode('test@example.com')
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
