import os
import unittest

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
