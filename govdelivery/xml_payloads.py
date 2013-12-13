from string import Template


def create_email_subscriber(email_address,
                            send_notifications=False,
                            digest_for=0):

    send_notifications = str(send_notifications).lower()
    subscriber_template = """<subscriber>
    <email>$email_address</email>
    <send-notifications type='boolean'>$send_notifications</send-notifications>
    <digest-for>$digest_for</digest-for>
  </subscriber>"""

    template = Template(subscriber_template)

    return template.substitute(locals())


def set_subscriber_categories(codes, send_notifications=False):
    send_notifications = str(send_notifications).lower()

    categories_xml = ""
    for code in codes:
        categories_xml += """  <category>
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


def set_subscriber_topics(codes, send_notifications=False):
    send_notifications = str(send_notifications).lower()

    topics_xml = ""
    for code in codes:
        topics_xml += """  <topic>
                <code>%s</code>
                      </topic>
                      """ % code

    xml_template = """<subscriber>
    <send-notifications type='boolean'>$send_notifications</send-notifications>
    <topics type='array'>
        $topics_xml
    </topics>
  </subscriber>"""

    template = Template(xml_template)

    return template.substitute(locals())
