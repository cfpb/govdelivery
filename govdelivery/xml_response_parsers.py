import xml.etree.ElementTree as ET


def topic_xml_as_dict(unparsed_xml, only_listed=False):
    root = ET.fromstring(unparsed_xml)
    code_map = {}

    for topic_tag in root.findall('topic'):
        if topic_tag.find('visibility').text == 'Unlisted' and only_listed:
            continue
        name = topic_tag.find('name').text
        code = topic_tag.find('code').text
        code_map[code] = name

    return code_map


def listed_topic_xml_as_dict(unparsed_xml):
    return topic_xml_as_dict(unparsed_xml, only_listed=True)


def subscriber_topics_as_list(unparsed_xml):
    root = ET.fromstring(unparsed_xml)
    codes = []

    for topic in root.findall('topic'):
        codes.append(topic.find('to-param').text)

    return codes


# This parser is currently unused.
# TODO: Write corresponding get_subscriber_answers client method.
def subscriber_responses_as_list_of_dicts(unparsed_xml):
    root = ET.fromstring(unparsed_xml)
    responses = []

    for response_tag in root.findall('response'):
        answer_id_tag = response_tag.find('answer-id')

        question_id = response_tag.find('question-id').text

        answer_id = answer_id_tag.text
        answer_id_is_null = answer_id_tag.attrib.get('nil') == 'true'

        answer_text = response_tag.find('question-answer-text').text

        response_dict = {
            'question_id': question_id,
            'answer_id': answer_id,
            'answer_text': answer_text,
            'answer_id_is_null': answer_id_is_null,
        }

        responses.append(response_dict)

    return responses
