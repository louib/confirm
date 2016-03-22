from difflib import get_close_matches
try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import ConfigParser
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import yaml


DEFAULT_TYPO_RATIO = 0.7
INI_FILE_EXTENSIONS = [".conf", ".ini"]


def config_parser_to_dict(config_parser):
    """
    Convert a ConfigParser to a dictionary.
    """
    response = {}

    for section in config_parser.sections():
        for option in config_parser.options(section):
            response.setdefault(section, {})[option] = config_parser.get(section, option)

    return response


def get_most_probable_typo(schema_name, actual_options):
    matches = get_close_matches(schema_name, actual_options, n=1, cutoff=DEFAULT_TYPO_RATIO)

    if matches:
        return matches[0]


def load_config_file(config_file_path, config_file):
    """
    Loads a config file, whether it is a yaml file or a .INI file.

    :param config_file_path: Path of the configuration file, used to infer the file format.
    :returns: Dictionary representation of the configuration file.
    """

    if config_file_path.lower().endswith(".yaml"):
        return yaml.load(config_file)

    if any(config_file_path.lower().endswith(extension) for extension in INI_FILE_EXTENSIONS):
        return load_config_from_ini_file(config_file)

    # At this point we have to guess the format of the configuration file.
    try:
        return yaml.load(config_file)
    except yaml.YAMLError:
        pass

    try:
        return load_config_from_ini_file(config_file)
    except:
        pass

    raise Exception("Could not load configuration file!")


def load_config_from_ini_file(ini_file_content):
    ini_file_buffer = StringIO(ini_file_content)

    try:
        config_parser = ConfigParser(interpolation=None)
    except NameError:
        config_parser = RawConfigParser()

    config_parser.readfp(ini_file_buffer)
    return config_parser_to_dict(config_parser)


def load_schema_file(schema_file):
    return yaml.load(schema_file)


def dump_schema_file(schema):
    return yaml.dump(schema, default_flow_style=False)
