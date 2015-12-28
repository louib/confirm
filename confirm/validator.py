"""
Main module for the validation functionalities.
"""
from confirm.utils import get_most_probable_typo


VALID_TYPES = ('int', 'float', 'bool', 'list', 'str')


def validate_config(config, schema, detect_typos=False, error_on_deprecated=False):

    result = {
        'error': [],
        'warning': [],
        'info': []
    }

    for section_name in schema:

        section_options = schema[section_name].values()
        section_has_required_option = any(option for option in section_options if option.get('required'))
        section_is_deprecated = all(option.get('deprecated') for option in section_options)
        section_is_present = config.get(section_name)

        best_match = None
        if detect_typos and not section_is_present:
            best_match = get_most_probable_typo(section_name, config.keys())

        # Note that if a section is deprecated, we do not perform any further validation!
        if section_is_deprecated and section_is_present:
            if error_on_deprecated:
                result['error'].append("Deprecated section %s is present!" % section_name)
            else:
                result['warning'].append("Deprecated section %s is present!" % section_name)

        elif section_has_required_option and not section_is_present:
            if best_match:
                result['error'].append("Missing required section %s (%s is a possible typo!)." % (section_name, best_match))
            else:
                result['error'].append("Missing required section %s." % section_name)

        elif not section_has_required_option and not section_is_present:
            if best_match:
                result['warning'].append("Possible typo for section %s : %s." % (section_name, best_match))

        # Section is present but not required, standard validations.
        elif section_is_present:
            validate_section(config, section_name, schema, detect_typos, error_on_deprecated, result)

    return result


def validate_section(config, section_name, schema, detect_typos, error_on_deprecated, result):

    # Required fields validation.
    for option_name in schema[section_name]:
        option_is_required = schema[section_name][option_name].get('required')
        option_is_deprecated = schema[section_name][option_name].get('deprecated')
        option_is_present = config[section_name].get(option_name)

        best_match = None
        if detect_typos and not option_is_present:
            best_match = get_most_probable_typo(option_name, config[section_name].keys())

        # Note that if an option is deprecated, we do not perform any further validation!
        if option_is_deprecated and option_is_present:
            if error_on_deprecated:
                result['error'].append("Deprecated option %s is present in section %s!" % (option_name, section_name))
            else:
                result['warning'].append("Deprecated option %s is present in section %s!" % (option_name, section_name))

        elif option_is_required and not option_is_present:
            if best_match:
                result['error'].append(
                    "Missing required option %s in section %s "
                    "(%s is a possible typo!)." % (option_name, section_name, best_match)
                )
            else:
                result['error'].append("Missing required option %s in section %s." % (option_name, section_name))

        elif not option_is_required and not option_is_present:
            if best_match:
                result['warning'].append("Possible typo for option %s : %s." % (option_name, best_match))

    # Type validation.
    for option_name in schema[section_name]:

        option_value = config[section_name].get(option_name)

        if not option_value:
            continue

        option_schema = schema[section_name][option_name]
        validate_option_type(option_name, option_value, option_schema, result)


def validate_option_type(option_name, option_value, option_schema, result):

    expected_type = option_schema.get('type')

    # No type validation to perform.
    if not expected_type:
        return

    if expected_type not in VALID_TYPES:
        result['error'].append("Invalid expected type for option %s : %s." % (option_name, expected_type))
        return

    try:
        if expected_type == 'int':
            int(option_value)
        elif expected_type == 'bool':
            if not option_value.lower() in ('true', 'false', '1', '0'):
                raise ValueError()
        elif expected_type == 'float':
            float(option_value)
    except ValueError:
        result['error'].append("Invalid value for type %s : %s." % (expected_type, option_value))
