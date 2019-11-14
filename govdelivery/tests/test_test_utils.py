import unittest

from govdelivery.tests.utils import load_data


class TestLoadData(unittest.TestCase):
    def test_load_data(self):
        self.assertEqual(
            load_data('list_subscriber_topics.xml'),
            """<?xml version="1.0" encoding="UTF-8"?>
<topics type="array">
    <topic>
        <to-param>XYZ_999</to-param>
        <link rel="self" href="/api/account/XYZ/topics/XYZ_999"/>
        <topic-uri>/api/account/XYZ/topics/XYZ_999.xml</topic-uri>
    </topic>
</topics>
"""
        )
