"""
Main module for the validation functionalities.
"""

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


def validate(config_parser, schema):
    for section_name in schema:
        validate_section(config_parser, section_name, schema)


def validate_section(config_parser, section, schema):

    confirm_section = schema.get(section)

    # Nothing to validate.
    if not confirm_section:
        return

    # Required fields validation.
    required_options = [option for option in confirm_section if confirm_section[option].get('required')]

    if required_options and not config_parser.has_section(section):
        raise MissingRequiredSectionException("Missing required section %s." % section)

    defined_options = [option for option, value in config_parser.items(section)]
    for required_option in required_options:
        if required_option not in defined_options:
            raise MissingRequiredOptionException("Missing required option %s in section %s" % (required_option, section))
        elif not config_parser.get(section, required_option):
            raise MissingRequiredOptionException("Missing required option %s in section %s" % (required_option, section))

    # Type validation.
    for section_name in config_parser.sections():
        for option_name in config_parser.options(section_name):
            schema_validations = schema.get(section_name, {}).get(option_name, {})

            expected_type = schema_validations.get('type')
            option_value = config_parser.get(section_name, option_name)

            if not expected_type in VALID_TYPES:
                raise InvalidTypeException("Invalid expected type for option %s : %s." % (option_name, option_value))

            try:
                if expected_type == 'int':
                    config_parser.getint(section_name, option_name)
                elif expected_type == 'bool':
                    config_parser.getboolean(section_name, option_name)
                elif expected_type == 'float':
                    config_parser.getfloat(section_name, option_name)
            except ValueError:
                raise TypeValidationException("Invalid value for type %s : %s." % (expected_type, option_value))
