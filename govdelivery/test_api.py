import os
import unittest
import xml.etree.ElementTree as ET

from . import api

dummy_username = "foo"
dummy_password = "bar"


def require_env_vars(varnames):
    for varname in varnames:
        assert varname in os.environ, "%s must be in os.environ" % varname


def require_auth_vars():
    require_env_vars(['GOVDELIVERY_USER',
                      'GOVDELIVERY_PASSWORD',
                      'GOVDELIVERY_ACCOUNT_CODE'])


def _create_topic():
    """ Create a test topic and return [TOPIC_CODE] """
    account_code = os.environ['GOVDELIVERY_ACCOUNT_CODE']
    payload = """
        <topic>
            <name>Test Topic 2</name>
            <short-name>Test Topic 2</short-name>
        </topic>
        """
    path = ''.join([
        '/api/account/',
        account_code,
        '/topics.xml'])
    response = api.authenticated_api_call(path, 'post', payload)
    root = ET.fromstring(response.text)
    codes = []
    codes.append(root.find('to-param').text)
    return codes


def _delete_topic(codes):
    """ Delete topic with TOPIC_CODE """
    account_code = os.environ['GOVDELIVERY_ACCOUNT_CODE']
    path = ''.join([
        '/api/account/',
        account_code,
        '/topics/'])
    for code in codes:
        response = api.authenticated_api_call(path + code + '.xml', 'delete')


class TestAuthentication(unittest.TestCase):

    def test_authenticated_api_call(self):
        require_auth_vars()
        account_code = os.environ['GOVDELIVERY_ACCOUNT_CODE']
        list_categories_path = ''.join([
            '/api/account/',
            account_code,
            '/categories.xml'])
        response = api.authenticated_api_call(list_categories_path,
                                              'get')
        assert(response.status_code == 200)
        assert('<categories type="array">' in response.text)

    def test_set_subscriber_topics(self):
        """ Test set_subscriber_topics """
        gd = api.GovDelivery()
        codes = _create_topic()
        response = gd.set_subscriber_topics('test@example.com', codes)
        assert(response.status_code == 200)
        response = gd.get_subscriber_topics('test@example.com')
        for code in codes:
            assert(code in response)
        _delete_topic(codes)
