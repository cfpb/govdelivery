import os
import base64
import requests
import urlparse
from string import Template

from . import xml_payloads
from . import xml_response_parsers


def authenticated_session(username=None, password=None):
    """
    Returns a request.Session with the Authorization
    headers set.
    """

    # allow credentials to come from os.environ
    # TODO: A sensible exception for when the variables don't exist
    # and haven't been passed to the function

    username = username or os.environ['GOVDELIVERY_USER']
    password = password or os.environ['GOVDELIVERY_PASSWORD']

    session = requests.Session()
    session.auth = (username, password)

    return session


def authenticated_api_call(path, method,
                           payload=None,
                           session=None, base_url=None):
    """
    makes an authenticated call to the govdelivery API
    using the provided path, method, payload, and request.Session

    Returns a request.Response
    """

    base_url = base_url or os.environ.get(
        'GOVDELIVERY_BASE_URL',
        'https://api.govdelivery.com')

    url_to_call = urlparse.urljoin(
        base_url,
        path)

    session = session or authenticated_session()
    if method.lower() in ['post','put']:
        session.headers['content-type'] = 'application/XML'
    client = getattr(session, method.lower())

    response = client(url_to_call, data=payload)
    return response


class GovDelivery(object):
    """
    Higher-level wrapper for the GovDelivery API
    """

    def __init__(self,
                 username=None,
                 password=None, account_code=None, base_url=None):

        self.session = authenticated_session(username, password)
        self.account_code = account_code or os.environ['GOVDELIVERY_ACCOUNT_CODE']

    def translate_path(self, path_template, **kwargs):
        context = kwargs
        context['account_code'] = self.account_code
        template = Template(path_template)
        return template.substitute(**kwargs)

    def call_api(self, path, method="get", payload=None, response_parser=None):
        unparsed_response = authenticated_api_call(path, method, payload, self.session)

        if not response_parser:
            return unparsed_response

        return response_parser(unparsed_response.text)

    def create_subscriber(self, email_address, send_notifications=False, digest_for=0):
        payload = xml_payloads.create_email_subscriber(email_address, send_notifications, digest_for)
        path = self.translate_path('/api/account/$account_code/subscribers.xml')
        return self.call_api(path, "post", payload)

    def get_all_topics(self):
        path = self.translate_path('/api/account/$account_code/topics.xml')
        return self.call_api(path, "get", response_parser=xml_response_parsers.listed_category_xml_as_dict)

    def get_visible_topics(self):
        path = self.translate_path('/api/account/$account_code/topics.xml')
        return self.call_api(path, "get", response_parser=xml_response_parsers.visible_category_xml_as_dict)

    def get_subscriber_categories(self, email_address):
        subscriber_id = base64.b64encode(email_address)
        path = self.translate_path('/api/account/$account_code/subscribers/$subscriber_id/categories.xml', subscriber_id=subscriber_id)
        return self.call_api(path)

    def set_subscriber_categories(self, email_address, category_codes):
        subscriber_id = base64.b64encode(email_address)
        path = self.translate_path('/api/account/$account_code/subscribers/$subscriber_id/categories.xml', subscriber_id=subscriber_id)
        payload = xml_payloads.set_subscriber_categories(category_codes)
        return self.call_api(path, "put", payload)

    def get_subscriber_topics(self, email_address):
        subscriber_id = base64.b64encode(email_address)
        path = self.translate_path('/api/account/$account_code/subscribers/$subscriber_id/topics.xml', subscriber_id=subscriber_id)
        return self.call_api(path)

    def set_subscriber_topics(self, email_address, topic_codes):
        subscriber_id = base64.b64encode(email_address)
        path = self.translate_path('/api/account/$account_code/subscribers/$subscriber_id/topics.xml', subscriber_id=subscriber_id)
        payload = xml_payloads.set_subscriber_topics(topic_codes)
        return self.call_api(path, "put", payload)
