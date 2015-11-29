"""
Module for automatic generation of configuration templates.
"""
from ConfigParser import ConfigParser


def generate_config_parser(config):
    """
    Generates a config parser from a configuration dictionary.

    The dictionary contains the merged informations of the schema and,
    optionally, of a source configuration file. Values of the source
    configuration file will be stored in the *value* field of an option.
    """

    # The allow_no_value allows us to output commented lines.
    config_parser = ConfigParser(allow_no_value=True)

    # We want to make sure that the diff is minimal by sticking to
    # a specific order.
    for section_name in sorted(config.keys()):
        for option_name in sorted(config[section_name].keys()):
            option = config[section_name][option_name]

            if option.get('required') or option.get('value') is not None:

                if not config_parser.has_section(section_name):
                    config_parser.add_section(section_name)

                config_parser.set(section_name, '# REQUIRED')
                config_parser.set(section_name, '# ' + option.get('description', 'No description provided.'))

                option_value = _get_value(option)
                config_parser.set(section_name, option_name, option_value)

                config_parser.set(section_name, '')

    return config_parser


def _get_value(option):
    if option.get('value') is not None:
        return str(option.get('value'))
    elif option.get('default'):
        return str(option.get('default'))
    else:
        return 'TO FILL'


def generate_documentation(schema):
    """
    Generates reStructuredText documentation from a Confirm file.

    :param schema: Dictionary representing the Confirm schema.

    :returns: String representing the reStructuredText documentation.
    """

    documentation = "Configuration documentation\n"
    documentation += "---------------------------\n"

    for section_name in schema:
        section_created = False

        for option_name in schema[section_name]:

            option = schema[section_name][option_name]

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


def append_existing_values(schema, config_parser):
    """
    Adds the values of the existing config to the config dictionary.
    """

    config = config_parser_to_dict(config_parser)

    for section_name in config:
        for option_name in config[section_name]:
            option_value = config[section_name][option_name]

            # Note that we must preserve existing values, wether or not they
            # exist in the schema file!
            schema.setdefault(section_name, {}).setdefault(option_name, {})['value'] = option_value

    return schema


def config_parser_to_dict(config_parser):
    """
    Convert a ConfigParser to a dictionary.
    """
    response = {}

    for section in config_parser.sections():
        for option in config_parser.options(section):
            response.setdefault(section, {})[option] = config_parser.get(section, option)

    return response
