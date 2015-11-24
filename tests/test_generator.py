from StringIO import StringIO
from ConfigParser import SafeConfigParser
import unittest

from confirm import generator

import yaml


class GenerateDocumentationTestCase(unittest.TestCase):

    def test_basic_case(self):
        confirm = """
        "section":
            "option":
                "required": true
                "description": "This is a description."
        """.strip()

        schema = yaml.load(StringIO(confirm))
        documentation = generator.generate_documentation(schema)

        expected_documentation = (
                                  "Configuration documentation\n---------------------------\n\n"
                                  "section\n=======\n\n"
                                  "option\n======\n** This option is required! **\nThis is a description.\n"
                                 )

        self.assertEqual(documentation, expected_documentation)

    def test_option_with_type(self):
        confirm = """
        "section":
            "option":
                "required": true
                "type": "bool"
        """.strip()

        schema = yaml.load(StringIO(confirm))
        documentation = generator.generate_documentation(schema)

        expected_documentation = (
                                  "Configuration documentation\n---------------------------\n\n"
                                  "section\n=======\n\n"
                                  "option\n======\n** This option is required! **\n*Type : bool.*\n"
                                 )

        self.assertEqual(documentation, expected_documentation)
