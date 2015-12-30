"""
Main module for the validation functionalities.
"""
from confirm.utils import get_most_probable_typo


VALID_TYPES = ('int', 'float', 'bool', 'list', 'str')


def validate_config(config, schema, error_on_deprecated=False):

    result = {
        'error': [],
        'warning': [],
    }

    section_names = set(schema.keys()) | set(config.keys())
    for section_name in section_names:

        if not schema.get(section_name):
            result['warning'].append("Section %s is not defined in the schema file." % section_name)
            continue

        section_options = schema[section_name].values()
        section_has_required_option = any(option for option in section_options if option.get('required'))
        section_is_deprecated = all(option.get('deprecated') for option in section_options)
        section_is_present = section_name in config

        best_match = None
        if not section_is_present:
            # We only detect typos using sections not defined in the schema.
            orphan_sections = set(config.keys()) - set(schema.keys())
            best_match = get_most_probable_typo(section_name, orphan_sections)

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
            validate_section(config, section_name, schema, error_on_deprecated, result)

    return result


def validate_section(config, section_name, schema, error_on_deprecated, result):

    # Required fields validation.
    option_names = set(schema.get(section_name, {}).keys()) | set(config.get(section_name, {}).keys())
    for option_name in option_names:

        if not schema.get(section_name, {}).get(option_name):
            result['warning'].append("Option %s of section %s is not defined in the schema file." % (option_name, section_name))
            continue

        option_is_required = schema[section_name][option_name].get('required')
        option_is_deprecated = schema[section_name][option_name].get('deprecated')
        option_is_present = config[section_name].get(option_name)

        best_match = None
        if not option_is_present:
            # We only detect typos using options not defined in the schema.
            orphan_options = set(config[section_name].keys()) - set(schema[section_name].keys())
            best_match = get_most_probable_typo(option_name, orphan_options)

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
        config[section_name][option_name] = get_typed_option_value(option_name, option_value, option_schema, result)
        check_custom_validation(option_name, option_value, option_schema, result)


def check_custom_validation(option_name, option_value, option_schema, result):

    custom_validation = option_schema.get('validation')
    if not custom_validation:
        return

    validation_function = eval("lambda x : " + custom_validation)
    is_valid_option_value = validation_function(option_value)

    if not is_valid_option_value:
        result['error'].append("Invalid option value for option %s : %s." % (option_name, option_value))


def get_typed_option_value(option_name, option_value, option_schema, result):

    expected_type = option_schema.get('type')
    value = None

    # No type validation to perform.
    if not expected_type:
        return

    if expected_type not in VALID_TYPES:
        result['error'].append("Invalid expected type for option %s : %s." % (option_name, expected_type))
        return

    try:
        if expected_type == 'int':
            value = int(option_value)
        elif expected_type == 'bool':
            if not option_value.lower() in ('true', 'false', '1', '0'):
                raise ValueError()
            if option_value.lower() in ('true', '1'):
                value = True
            else:
                value = False
        elif expected_type == 'float':
            value = float(option_value)
    except ValueError:
        result['error'].append("Invalid value for type %s : %s." % (expected_type, option_value))

    return value
