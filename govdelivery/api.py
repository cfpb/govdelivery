import base64
import os
import urllib.parse as urlparse
from string import Template

import requests

from govdelivery import xml_payloads, xml_response_parsers

GOVDELIVERY_BASE_URL = 'https://api.govdelivery.com'


def get_full_url_to_call(path, base_url=None):
    return urlparse.urljoin(
        base_url or os.getenv('GOVDELIVERY_BASE_URL') or GOVDELIVERY_BASE_URL,
        path
    )


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


def authenticated_api_call(path, method, payload=None, session=None,
                           base_url=None):
    """
    makes an authenticated call to the govdelivery API
    using the provided path, method, payload, and request.Session

    Returns a request.Response
    """

    url_to_call = get_full_url_to_call(path, base_url)

    session = session or authenticated_session()
    if method.lower() in ['post', 'put']:
        session.headers['content-type'] = 'application/XML'
    client = getattr(session, method.lower())

    response = client(url_to_call, data=payload)
    return response


class GovDelivery(object):
    """
    Higher-level wrapper for the GovDelivery API
    """

    def __init__(self, username=None, password=None, account_code=None,
                 base_url=None):

        self.session = authenticated_session(username, password)
        self.account_code = (
            account_code or os.environ['GOVDELIVERY_ACCOUNT_CODE']
        )

    # TODO: Replace this function with f-strings.
    def translate_path(self, path_template, **kwargs):
        context = kwargs
        context['account_code'] = self.account_code
        template = Template(path_template)
        return template.substitute(**kwargs)

    def call_api(self, path, method='get', payload=None, response_parser=None):
        unparsed_response = authenticated_api_call(
            path,
            method,
            payload,
            self.session
        )

        if not response_parser:
            return unparsed_response

        return response_parser(unparsed_response.text)

    def create_subscriber(self, contact_details, contact_method='email',
                          send_notifications=False, digest_for=0):
        payload = xml_payloads.create_subscriber(
            contact_details,
            contact_method,
            send_notifications,
            digest_for
        )

        path = self.translate_path(
            '/api/account/$account_code/subscribers.xml'
        )
        return self.call_api(path, 'post', payload)

    def get_all_topics(self):
        path = self.translate_path('/api/account/$account_code/topics.xml')
        return self.call_api(
            path,
            'get',
            response_parser=xml_response_parsers.topic_xml_as_dict
        )

    # TODO: Rename method to be more precise
    def get_visible_topics(self):
        path = self.translate_path('/api/account/$account_code/topics.xml')
        return self.call_api(
            path,
            'get',
            response_parser=xml_response_parsers.listed_topic_xml_as_dict
        )

    def get_subscriber_categories(self, contact_details):
        subscriber_id = base64.b64encode(contact_details.encode('utf-8'))
        path = self.translate_path(
            '/api/account/$account_code/'
            'subscribers/$subscriber_id/'
            'categories.xml',
            subscriber_id=subscriber_id
        )
        return self.call_api(path)

    def set_subscriber_categories(self, contact_details, category_codes,
                                  send_notifications=False):
        subscriber_id = base64.b64encode(contact_details.encode('utf-8'))
        path = self.translate_path(
            '/api/account/$account_code/'
            'subscribers/$subscriber_id/'
            'categories.xml',
            subscriber_id=subscriber_id
        )
        payload = xml_payloads.set_subscriber_categories(
            category_codes,
            send_notifications
        )
        return self.call_api(path, 'put', payload)

    def get_subscriber_topics(self, contact_details):
        subscriber_id = base64.b64encode(contact_details.encode('utf-8'))
        path = self.translate_path(
            '/api/account/$account_code/subscribers/$subscriber_id/topics.xml',
            subscriber_id=subscriber_id
        )
        return self.call_api(
            path,
            response_parser=xml_response_parsers.subscriber_topics_as_list
        )

    def set_subscriber_topics(self, contact_details, topic_codes,
                              contact_method='email',
                              send_notifications=False):
        topic_code_set = set(topic_codes)

        path = self.translate_path(
            '/api/account/$account_code/subscriptions.xml'
        )
        payload = xml_payloads.set_subscriber_topics(
            topic_code_set,
            contact_details,
            contact_method,
            send_notifications
        )
        return self.call_api(path, 'post', payload)

    def set_subscriber_answers_to_question(self, contact_details, question_id,
                                           answer_text):
        subscriber_id = base64.b64encode(contact_details.encode('utf-8'))
        question_id_encoded = base64.b64encode(question_id.encode('utf-8'))

        path = self.translate_path(
            '/api/account/$account_code/'
            'subscribers/$subscriber_id/'
            'questions/$question_id_encoded/'
            'responses.xml',
            subscriber_id=subscriber_id,
            question_id_encoded=question_id_encoded
        )

        payload = xml_payloads.free_response_to_question(
            question_id_encoded,
            answer_text
        )
        return self.call_api(path, 'put', payload)

    def set_subscriber_answer_to_select_question(
        self,
        contact_details,
        question_id,
        answer_id
    ):
        subscriber_id = base64.b64encode(contact_details.encode('utf-8'))
        question_id_encoded = base64.b64encode(question_id.encode('utf-8'))
        answer_id_encoded = base64.b64encode(answer_id.encode('utf-8'))

        path = self.translate_path(
            (
                '/api'
                '/account/$account_code'
                '/subscribers/$subscriber_id'
                '/questions/$question_id_encoded'
                '/responses.xml'
            ),
            subscriber_id=subscriber_id,
            question_id_encoded=question_id_encoded,
            answer_id_encoded=answer_id_encoded
        )

        payload = xml_payloads.select_response_to_question(
            question_id_encoded,
            answer_id_encoded
        )
        return self.call_api(path, 'put', payload)
