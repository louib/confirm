"""
Module for automatic generation of configuration templates.
"""
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import ConfigParser as SafeConfigParser

from confirm import utils


def _get_included_schema_sections_options(config, include_all):

    # We want to make sure that the diff is minimal by sticking to
    # a specific order.
    for section_name in sorted(config.keys()):
        for option_name in sorted(config[section_name].keys()):

            option = config[section_name][option_name]
            if _include_in_config(option) or include_all:
                yield section_name, option_name


def generate_config_parser(config, include_all=False):
    """
    Generates a config parser from a configuration dictionary.

    The dictionary contains the merged informations of the schema and,
    optionally, of a source configuration file. Values of the source
    configuration file will be stored in the *value* field of an option.
    """

    # The allow_no_value allows us to output commented lines.
    config_parser = SafeConfigParser(allow_no_value=True)
    for section_name, option_name in _get_included_schema_sections_options(config, include_all):

        if not config_parser.has_section(section_name):
            config_parser.add_section(section_name)

        option = config[section_name][option_name]

        if option.get('required'):
            config_parser.set(section_name, '# REQUIRED')

        config_parser.set(section_name, '# ' + option.get('description', 'No description provided.'))

        if option.get('deprecated'):
            config_parser.set(section_name, '# DEPRECATED')

        option_value = _get_value(option)
        config_parser.set(section_name, option_name, option_value)

        config_parser.set(section_name, '')

    return config_parser


def _include_in_config(option):
    # We include an option if it is required, or if
    # it was already specified in the original configuration file.
    return option.get('required') or option.get('value') is not None


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

    documentation_title = "Configuration documentation"
    documentation = documentation_title + "\n"
    documentation += "=" * len(documentation_title) + '\n'

    for section_name in schema:
        section_created = False

        for option_name in schema[section_name]:

            option = schema[section_name][option_name]

            if not section_created:
                documentation += '\n'
                documentation += section_name + '\n'
                documentation += '-' * len(section_name) + '\n'
                section_created = True

            documentation += '\n'
            documentation += option_name + '\n'
            documentation += '~' * len(option_name) + '\n'

            if option.get('required'):

                documentation += "** This option is required! **\n"

            if option.get('type'):

                documentation += '*Type : %s.*\n' % option.get('type')

            if option.get('description'):

                documentation += option.get('description') + '\n'

            if option.get('default'):

                documentation += 'The default value is %s.\n' % option.get('default')

            if option.get('deprecated'):

                documentation += "** This option is deprecated! **\n"

    return documentation


def append_existing_values(schema, config):
    """
    Adds the values of the existing config to the config dictionary.
    """

    for section_name in config:
        for option_name in config[section_name]:
            option_value = config[section_name][option_name]

            # Note that we must preserve existing values, wether or not they
            # exist in the schema file!
            schema.setdefault(section_name, {}).setdefault(option_name, {})['value'] = option_value

    return schema


def generate_schema_file(config_file):
    """
    Generates a basic confirm schema file from a configuration file.
    """

    config = utils.load_config_from_ini_file(config_file)
    schema = {}

    for section_name in config:
        for option_name in config[section_name]:
            schema.setdefault(section_name, {}).setdefault(option_name, {})
            schema[section_name][option_name]['description'] = 'No description provided.'

    return utils.dump_schema_file(schema)
