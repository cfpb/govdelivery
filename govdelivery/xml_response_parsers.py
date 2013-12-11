import xml.etree.ElementTree as ET


def category_xml_as_dict(unparsed_xml, only_listed=False):
    root = ET.fromstring(unparsed_xml)
    code_map = {}
    for topic_tag in root.findall('topic'):
        if topic_tag.find('visibility').text == 'Unlisted':
            continue
        name = topic_tag.find('name').text
        code = topic_tag.find('code').text
        code_map[code] = name

    return code_map


def visible_category_xml_as_dict(unparsed_xml):
    return category_xml_as_dict(unparsed_xml, only_listed=True)
