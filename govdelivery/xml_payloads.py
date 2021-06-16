import re
import warnings
from string import Template


def format_phone(phone):
    warnings.warn(
        'The phone number formatter will be deprecated in a future release of '
        'govdelivery. Going forward, please ensure that your application '
        'passes phone numbers in the format that the GovDelivery API requires '
        '(a ten-digit string with no punctuation).',
        DeprecationWarning
    )

    # if phone starts with + or 1, strip those characters
    phone = phone.lstrip('+1')
    # strip all other non-digit characters
    phone = re.sub(r'\D', '', phone)

    return phone


def create_subscriber(contact_details,
                      contact_method='email',
                      send_notifications=False,
                      digest_for=0):
    send_notifications = str(send_notifications).lower()

    country_code = ''
    if contact_method == 'phone':
        # Note: Currently only supports U.S. phone numbers
        contact_details = format_phone(contact_details)
        country_code = '<country-code>1</country-code>'

    subscriber_template = """<subscriber>
    <$contact_method>$contact_details</$contact_method>
    $country_code
    <send-notifications type='boolean'>$send_notifications</send-notifications>
    <digest-for>$digest_for</digest-for>
</subscriber>"""

    template = Template(subscriber_template)

    return template.substitute(locals())


def set_subscriber_categories(codes, send_notifications=False):
    send_notifications = str(send_notifications).lower()

    categories_xml = ''
    for code in codes:
        categories_xml += """
        <category>
            <code>%s</code>
        </category>
""" % code

    xml_template = """<subscriber>
    <send-notifications type='boolean'>$send_notifications</send-notifications>
    <categories type='array'>
        $categories_xml
    </categories>
</subscriber>"""

    template = Template(xml_template)
    return template.substitute(locals())


def set_subscriber_topics(codes,
                          contact_details,
                          contact_method='email',
                          send_notifications=False):
    send_notifications = str(send_notifications).lower()

    country_code = ''
    if contact_method == 'phone':
        # Note: Currently only supports U.S. phone numbers
        contact_details = format_phone(contact_details)
        country_code = '<country-code>1</country-code>'

    topics_xml = ''
    for code in codes:
        topics_xml += """
        <topic>
            <code>%s</code>
        </topic>
""" % code

    xml_template = """<subscriber>
    <$contact_method>$contact_details</$contact_method>
    $country_code
    <send-notifications type='boolean'>$send_notifications</send-notifications>
    <topics type='array'>
        $topics_xml
    </topics>
</subscriber>"""

    template = Template(xml_template)
    return template.substitute(locals())


def free_response_to_question(question_id, answer_text):
    xml_template = """<responses type="array">
    <response>
        <question-answer-text>$answer_text</question-answer-text>
        <question-id>$question_id</question-id>
        <answer-id nil="true"></answer-id>
    </response>
</responses>
"""

    template = Template(xml_template)
    return template.substitute(locals())


def select_response_to_question(question_id, answer_id):
    xml_template = """<responses type="array">
    <response>
        <question-id>$question_id</question-id>
        <answer-id>$answer_id</answer-id>
    </response>
</responses>
"""

    template = Template(xml_template)
    return template.substitute(locals())
