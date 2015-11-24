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
