import unittest
import codecs

from os import path

from . import xml_response_parsers

testdata_dir = path.join(path.dirname(__file__), 'testdata')

def load_data(filename):
    full_path = path.join(testdata_dir, filename)
    f = codecs.open(full_path, encoding="utf8")
    return f.read()

class TestQuestionResponseParser(unittest.TestCase):

    def test_parse_response(self):
        response_xml = load_data('question_responses.xml')
        parsed = xml_response_parsers.subscriber_responses_as_list_of_dicts(response_xml)
        r1, r2, r3 = parsed 
        assert('question_id' in r1)
        assert(r1['question_id'] == 'MTAwNDk=')
