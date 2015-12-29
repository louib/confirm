try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import ConfigParser as SafeConfigParser
import unittest

from confirm import validator
from confirm.utils import load_config_file

import yaml


def _call_validate(config_string, schema_string, **kwargs):
    """
    Small wrapper to use the standard interface.
    """
    config_parser = SafeConfigParser()
    config_parser.readfp(StringIO(config_string))

    schema = yaml.load(StringIO(schema_string))
    config = load_config_file('.ini', config_string)

    return validator.validate_config(config, schema, **kwargs)


class ValidatorTestCase(unittest.TestCase):

    def test_required_field_in_missing_section(self):
        config = "[sectiona]\noptiona = valuea"

        schema = """
        "sectionb":
            "optionb":
                "required": true
        "sectiona":
            "optiona":
                "type": "int"
        """

        result = _call_validate(config, schema)
        self.assertIn("Missing required section sectionb.", result['error'])

    def test_missing_required_field(self):
        config = "[section]\noption1 = value1"

        schema = """
        "section":
            "option2":
                "required": true
            "option1":
                "description": "This is a description."
        """

        result = _call_validate(config, schema)
        self.assertIn("Missing required option option2 in section section.", result['error'])

    def test_empty_required_field(self):
        config = "[section]\noption1 ="

        schema = """
        "section":
            "option1":
                "required": true
        """

        result = _call_validate(config, schema)
        self.assertIn("Missing required option option1 in section section.", result['error'])

    def test_invalid_int(self):
        config = "[section]\noption1 =not an int!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "int"
        """

        result = _call_validate(config, schema)
        self.assertIn("Invalid value for type int : not an int!.", result['error'])

    def test_invalid_bool(self):
        config = "[section]\noption1 =not a bool!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "bool"
        """

        result = _call_validate(config, schema)
        self.assertIn("Invalid value for type bool : not a bool!.", result['error'])

    def test_invalid_float(self):
        config = "[section]\noption1 =not a float!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "float"
        """

        result = _call_validate(config, schema)
        self.assertIn("Invalid value for type float : not a float!.", result['error'])

    def test_invalid_type(self):
        config = "[section]\noption1 =We don't care about the type here."

        schema = """
        "section":
            "option1":
                "required": true
                "type": "invalid"
        """

        result = _call_validate(config, schema)
        self.assertIn("Invalid expected type for option option1 : invalid.", result['error'])

    def test_typo_option_warning(self):
        config = "[section]\noption13=14."

        schema = """
        "section":
            "option1":
                "required": false
                "type": "int"
        """

        result = _call_validate(config, schema)
        self.assertIn("Possible typo for option option1 : option13.", result['warning'])

    def test_typo_section_warning(self):
        config = "[section13]\nrandom_option=random_value."

        schema = """
        "section1":
            "option1":
                "required": false
                "type": "int"
        """

        result = _call_validate(config, schema)
        self.assertIn("Possible typo for section section1 : section13.", result['warning'])

    def test_deprecated_section(self):
        config = "[section1]\nrandom_option=random_value."

        schema = """
        "section1":
            "option1":
                "deprecated": true
                "required": false
                "type": "int"
        """

        result = _call_validate(config, schema)
        self.assertIn("Deprecated section section1 is present!", result['warning'])

        result = _call_validate(config, schema, error_on_deprecated=True)
        self.assertIn("Deprecated section section1 is present!", result['error'])

    def test_deprecated_option(self):
        config = "[section1]\noption1=random_value."

        schema = """
        "section1":
            "option1":
                "deprecated": true
                "required": false
                "type": "str"
            "option2":
                "deprecated": false
                "required": false
                "type": "int"
        """

        result = _call_validate(config, schema)
        self.assertIn("Deprecated option option1 is present in section section1!", result['warning'])

        result = _call_validate(config, schema, error_on_deprecated=True)
        self.assertIn("Deprecated option option1 is present in section section1!", result['error'])

    def test_undefined_section(self):
        config = "[section1]\noption1=random_value\n[section2]\noption=value"

        schema = """
        "section1":
            "option1":
                "required": false
                "type": "str"
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Section section2 is not defined in the schema file.", result['warning'])

    def test_undefined_option(self):
        config = "[section1]\noption1=random_value\noption2=random_value2"

        schema = """
        "section1":
            "option1":
                "required": false
                "type": "str"
        """.strip()

        result = _call_validate(config, schema)
        self.assertIn("Option option2 of section section1 is not defined in the schema file.", result['warning'])
