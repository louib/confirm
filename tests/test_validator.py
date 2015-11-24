from StringIO import StringIO
from ConfigParser import SafeConfigParser
import unittest

from confirm import validator

import yaml


class ValidatorTestCase(unittest.TestCase):

    def test_missing_required_field(self):
        config = "[section]\noption1 = value1"

        confirm = """
        "section":
            "option2":
                "required": true
        """.strip()

        config_parser = SafeConfigParser()
        config_parser.readfp(StringIO(config))

        confirmations = yaml.load(StringIO(confirm))

        self.assertRaises(validator.MissingRequiredOptionException, validator.validate, config_parser, confirmations)

    def test_empty_required_field(self):
        config = "[section]\noption1 ="

        confirm = """
        "section":
            "option1":
                "required": true
        """.strip()

        config_parser = SafeConfigParser()
        config_parser.readfp(StringIO(config))

        confirmations = yaml.load(StringIO(confirm))

        self.assertRaises(validator.MissingRequiredOptionException, validator.validate, config_parser, confirmations)
