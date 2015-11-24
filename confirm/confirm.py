# -*- coding: utf-8 -*-
import sys
import json
import yaml
from ConfigParser import SafeConfigParser


VALID_OPTIONS = ('required', 'default', 'validator', 'description')
VALID_BOOLEAN_VALUES = ('True', 'False', '1', '0')


class ConfirmException(Exception):
    """
    Base exception for confirm module.
    """

class MissingRequiredSectionException(ConfirmException):
    pass


def validate(config_parser, confirmations):
    for section in config_parser.sections():
        validate_section(config_parser, section, confirmations)

    # TODO : Add validation for missing sections!.


def validate_section(config_parser, section, confirmations):

    confirm_section = confirmations.get(section)

    # Nothing to validate.
    if not confirm_section:
        return

    defined_options = [option for option, value in config_parser.items(section)]
    required_options = [option for option in confirm_section if confirm_section[option].get('required')]
    for required_option in required_options:
        if required_option not in defined_options:
            raise MissingRequiredSectionException("Missing required option %s in section %s" % (required_option, section))


if __name__ == '__main__':
    config_parser = SafeConfigParser()
    config_parser.read(sys.argv[1])

    confirm_file_path = sys.argv[2]
    if confirm_file_path.endswith('json'):
        confirmations = json.load(open(confirm_file_path, 'r'))
    elif confirm_file_path.endswith('yaml'):
        confirmations = yaml.load(open(confirm_file_path, 'r'))
    else:
        raise Exception("Invalid confirm file extension : %s." % confirm_file_path.rsplit('.')[-1])

    validate(config_parser, confirmations)
