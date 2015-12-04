from difflib import get_close_matches


DEFAULT_TYPO_RATIO = 0.7


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
