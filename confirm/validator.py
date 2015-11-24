"""
Main module for the validation functionalities.
"""


class ConfirmException(Exception):
    """
    Base exception for confirm module.
    """


class MissingRequiredSectionException(ConfirmException):
    pass


class MissingRequiredOptionException(ConfirmException):
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
            raise MissingRequiredOptionException("Missing required option %s in section %s" % (required_option, section))
        elif not config_parser.get(section, required_option):
            raise MissingRequiredOptionException("Missing required option %s in section %s" % (required_option, section))

