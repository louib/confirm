from StringIO import StringIO
from ConfigParser import SafeConfigParser
import unittest

from confirm import validator

import yaml


def _call_validate(config_string, schema_string):
    """
    Small wrapper to use the standard interface.
    """
    config_parser = SafeConfigParser()
    config_parser.readfp(StringIO(config_string))

    schema = yaml.load(StringIO(schema_string))

    validator.validate(config_parser, schema)


class ValidatorTestCase(unittest.TestCase):

    def test_missing_required_field(self):
        config = "[section]\noption1 = value1"

        schema = """
        "section":
            "option2":
                "required": true
        """.strip()

        self.assertRaises(validator.MissingRequiredOptionException, _call_validate, config, schema)

    def test_empty_required_field(self):
        config = "[section]\noption1 ="

        schema = """
        "section":
            "option1":
                "required": true
        """.strip()

        self.assertRaises(validator.MissingRequiredOptionException, _call_validate, config, schema)

    def test_invalid_int(self):
        config = "[section]\noption1 =not an int!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "int"
        """.strip()

        self.assertRaises(validator.TypeValidationException, _call_validate, config, schema)

    def test_invalid_bool(self):
        config = "[section]\noption1 =not a bool!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "bool"
        """.strip()

        self.assertRaises(validator.TypeValidationException, _call_validate, config, schema)

    def test_invalid_float(self):
        config = "[section]\noption1 =not a float!"

        schema = """
        "section":
            "option1":
                "required": true
                "type": "float"
        """.strip()

        self.assertRaises(validator.TypeValidationException, _call_validate, config, schema)

    def test_invalid_type(self):
        config = "[section]\noption1 =We don't care about the type here."

        schema = """
        "section":
            "option1":
                "required": true
                "type": "invalid"
        """.strip()

        self.assertRaises(validator.InvalidTypeException, _call_validate, config, schema)
