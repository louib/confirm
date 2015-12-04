from StringIO import StringIO
from ConfigParser import SafeConfigParser
import unittest

from confirm import validator

import yaml


def _call_validate(config_string, schema_string, **kwargs):
    """
    Small wrapper to use the standard interface.
    """
    config_parser = SafeConfigParser()
    config_parser.readfp(StringIO(config_string))

    schema = yaml.load(StringIO(schema_string))

    return validator.validate_config(config_parser, schema, **kwargs)


class ValidatorTestCase(unittest.TestCase):

    def test_required_field_in_missing_section(self):
        config = "[sectiona]\noptiona = valuea"

        schema = """
        "sectionb":
            "optionb":
                "required": true
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Missing required section sectionb.", result['error'])

    def test_missing_required_field(self):
        config = "[section]\noption1 = value1"

        schema = """
        "section":
            "option2":
                "required": true
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Missing required option option2 in section section.", result['error'])

    def test_empty_required_field(self):
        config = "[section]\noption1 ="

        schema = """
        "section":
            "option1":
                "required": true
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Missing required option option1 in section section.", result['error'])

    def test_invalid_int(self):
        config = "[section]\noption1 =not an int!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "int"
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Invalid value for type int : not an int!.", result['error'])

    def test_invalid_bool(self):
        config = "[section]\noption1 =not a bool!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "bool"
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Invalid value for type bool : not a bool!.", result['error'])

    def test_invalid_float(self):
        config = "[section]\noption1 =not a float!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "float"
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Invalid value for type float : not a float!.", result['error'])

    def test_invalid_type(self):
        config = "[section]\noption1 =We don't care about the type here."

        schema = """
        "section":
            "option1":
                "required": true
                "type": "invalid"
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Invalid expected type for option option1 : invalid.", result['error'])

    def test_typo_option_warning(self):
        config = "[section]\noption13=14."

        schema = """
        "section":
            "option1":
                "required": false
                "type": "int"
        """.strip()

        result = _call_validate(config, schema, detect_typos=True)
        self.assertIn("Possible typo for option option1 : option13.", result['warning'])

    def test_typo_section_warning(self):
        config = "[section13]\nrandom_option=random_value."

        schema = """
        "section1":
            "option1":
                "required": false
                "type": "int"
        """.strip()

        result = _call_validate(config, schema, detect_typos=True)
        self.assertIn("Possible typo for section section1 : section13.", result['warning'])
