from StringIO import StringIO
from ConfigParser import SafeConfigParser
import unittest

from confirm import generator

import yaml


class GenerateConfigParserTestCase(unittest.TestCase):

    def test_empty_config(self):
        config_parser = generator.generate_config_parser({})
        self.assertFalse(len(config_parser.sections()))

    def test_required(self):
        config = {"section":
                     {"option":
                         {"required": True}
                     }
                 }
        config_parser = generator.generate_config_parser(config)
        options = config_parser.options('section')
        self.assertIn('option', options)
        self.assertIn('# required', options)

        value = config_parser.get('section', 'option')
        self.assertEqual(value, 'TO FILL')

    def test_required_default(self):
        config = {"section":
                     {"option":
                         {"required": True, "default": 12}
                     }
                 }
        config_parser = generator.generate_config_parser(config)
        value = config_parser.get('section', 'option')
        self.assertEqual(value, '12')

    def test_required_default(self):
        config = {"section":
                     {"option":
                         {"required": True, "default": 12, "value": 25}
                     }
                 }
        config_parser = generator.generate_config_parser(config)
        options = config_parser.options('section')
        self.assertIn('option', options)
        self.assertIn('# required', options)

        value = config_parser.get('section', 'option')
        self.assertEqual(value, '25', "We should use the existing value instead of the default!")

    def test_required_no_default_no_value(self):
        config = {"section":
                     {"option":
                         {"required": True}
                     }
                 }
        config_parser = generator.generate_config_parser(config)
        options = config_parser.options('section')
        self.assertIn('option', options)
        self.assertIn('# required', options)

        value = config_parser.get('section', 'option')
        self.assertEqual(value, 'TO FILL')

    def test_options(self):
        config = {"section":
                     {"optiona":
                         {"required": True, "default": 'DA',  "value": 'VA'},
                      "optionb":
                         {"required": True, "default": 'DB'}
                     }
                 }

        config_parser = generator.generate_config_parser(config)
        options = config_parser.options('section')

        self.assertIn('optiona', options)
        value = config_parser.get('section', 'optiona')
        self.assertEqual(value, 'VA')

        self.assertIn('optionb', options)
        value = config_parser.get('section', 'optionb')
        self.assertEqual(value, 'DB')

    def test_generate_include_all(self):
        config = {"section":
                     {"optiona":
                         {"required": True, "default": 'DA',  "value": 'VA'},
                      "optionb":
                         {"default": 'DB'}
                     }
                 }

        config_parser = generator.generate_config_parser(config)
        options = config_parser.options('section')
        self.assertNotIn('optionb', options)

        config_parser = generator.generate_config_parser(config, include_all=True)
        options = config_parser.options('section')
        self.assertIn('optionb', options)

        value = config_parser.get('section', 'optionb')
        self.assertEqual(value, 'DB')


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
