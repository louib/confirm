"""
Main module for the validation functionalities.
"""
from confirm.utils import config_parser_to_dict


VALID_TYPES = ('int', 'float', 'bool', 'list', 'str')


class ConfirmException(Exception):
    """
    Base exception for confirm module.
    """


class MissingRequiredSectionException(ConfirmException):
    pass


class MissingRequiredOptionException(ConfirmException):
    pass


class TypeValidationException(ConfirmException):
    pass


class InvalidTypeException(ConfirmException):
    pass


def validate_config(config_parser, schema):

    config = config_parser_to_dict(config_parser)

    for section_name in schema:

        section_options = schema[section_name].values()
        section_has_required_option = any(option for option in section_options if option.get('required'))
        if section_has_required_option and not config.get(section_name):
            raise MissingRequiredSectionException("Missing required section %s." % section_name)

        # Section is not required and not present : nothing to validate.
        if not config.get(section_name):
            continue

        validate_section(config, section_name, schema)


def validate_section(config, section_name, schema):

    confirm_section = schema.get(section_name)

    # Required fields validation.
    for option_name in schema[section_name]:
        option_is_required = schema[section_name][option_name].get('required')
        option_is_present = config[section_name].get(option_name)

        if option_is_required and not option_is_present:
            raise MissingRequiredOptionException("Missing required option %s in section %s" % (option_name, section_name))

    # Type validation.
    for option_name in schema[section_name]:

        option_value = config[section_name].get(option_name)
        option_schema = schema[section_name][option_name]
        validate_option_type(option_name, option_value, option_schema)


def validate_option_type(option_name, option_value, option_schema):

    expected_type = option_schema.get('type')

    # No type validation to perform.
    if not expected_type:
        return

    if not expected_type in VALID_TYPES:
        raise InvalidTypeException("Invalid expected type for option %s : %s." % (option_name, option_value))

    try:
        if expected_type == 'int':
            int(option_value)
        elif expected_type == 'bool':
            if not option_value.lower() in ('true', 'false', '1', '0'):
               raise ValueError()
        elif expected_type == 'float':
            float(option_value)
    except ValueError:
        raise TypeValidationException("Invalid value for type %s : %s." % (expected_type, option_value))
