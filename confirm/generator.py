"""
Module for automatic generation of configuration templates.
"""
from ConfigParser import ConfigParser


def generate(confirm_file):
    """
    Generates a configuration template from a Confirm file.

    :param confirm_file_path: Dictionary representing the Confirm validations..

    :returns: String representing a template .INI file.
    """
    config_parser = ConfigParser(allow_no_value=True)
    for section_name in confirm_file:
        for option_name in confirm_file[section_name]:
            option = confirm_file[section_name][option_name]
            if option.get('required'):
                if not config_parser.has_section(section_name):
                    config_parser.add_section(section_name)

                config_parser.set(section_name, '# REQUIRED')
                config_parser.set(section_name, '# ' + option.get('description', 'No description provided.'))
                if option.get('default'):
                    config_parser.set(section_name, option_name, option.get('default'))
                else:
                    config_parser.set(section_name, option_name, 'TO FILL')
            config_parser.set(section_name, '')

    return config_parser

def generate_documentation(confirm_file):
    """
    Generates reStructuredText documentation from a Confirm file.

    :param confirm_file_path: Dictionary representing the Confirm validations..

    :returns: String representing the reStructuredText documentation.
    """

    documentation = "Configuration documentation\n"
    documentation += "---------------------------\n"

    for section_name in confirm_file:
        section_created = False

        for option_name in confirm_file[section_name]:

            option = confirm_file[section_name][option_name]

            if not section_created:
                documentation += '\n'
                documentation += section_name + '\n'
                documentation += '=' * len(section_name) + '\n'
                section_created = True

            documentation += '\n'
            documentation += option_name + '\n'
            documentation += '=' * len(option_name) + '\n'

            if option.get('required'):

                documentation += "** This option is required! **\n"

            if option.get('type'):

                documentation += '*Type : %s.*\n' % option.get('type')

            if option.get('description'):

                documentation += option.get('description') + '\n'

            if option.get('default'):

                documentation += 'The default value is %s.\n' % option.get('default')

    return documentation
