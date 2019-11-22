import unittest

from govdelivery.tests.utils import load_data
from govdelivery.xml_response_parsers import (
    listed_topic_xml_as_dict,
    subscriber_responses_as_list_of_dicts,
    subscriber_topics_as_list,
    topic_xml_as_dict,
)


class TestTopicListingParsers(unittest.TestCase):
    def test_topic_xml_as_dict(self):
        response_xml = load_data('list_all_topics.xml')
        parsed = topic_xml_as_dict(response_xml)
        self.assertEqual(
            parsed,
            {'XYZ_998': 'Test Unlisted Topic', 'XYZ_999': 'Test Topic'}
        )

    def test_listed_topic_xml_as_dict(self):
        response_xml = load_data('list_all_topics.xml')
        parsed = listed_topic_xml_as_dict(response_xml)
        self.assertEqual(
            parsed,
            {'XYZ_999': 'Test Topic'}
        )


class TestSubscriberTopicsParser(unittest.TestCase):
    def test_subscriber_topics_as_list(self):
        response_xml = load_data('list_subscriber_topics.xml')
        parsed = subscriber_topics_as_list(response_xml)
        self.assertEqual(
            parsed,
            ['XYZ_999']
        )


class TestQuestionResponseParser(unittest.TestCase):
    def test_parse_response(self):
        response_xml = load_data('question_responses.xml')
        parsed = subscriber_responses_as_list_of_dicts(response_xml)
        r1, r2, r3 = parsed

        self.assertIn('question_id', r1)
        self.assertEqual(r1['question_id'], 'MTAwNDk=')
