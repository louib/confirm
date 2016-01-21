"""
Main module for the validation functionalities.
"""
from confirm.utils import get_most_probable_typo
from confirm.utils import config_parser_to_dict
from confirm.utils import load_schema_file
from confirm.utils import load_config_file


VALID_TYPES = ('int', 'float', 'bool', 'list', 'str')


def validator_from_config_file(config_file_path, schema_file_path):
    schema = load_schema_file(open(schema_file_path, 'r'))
    config = load_config_file(config_file_path, open(config_file_path, 'r').read())
    return Validation(config, schema)


def validator_from_config_parser(config_parser, schema_file_path):
    schema = load_schema_file(open(schema_file_path, 'r'))
    config = config_parser_to_dict(config_parser)
    return Validation(config, schema)


def validator_from_config(config, schema_file_path):
    schema = load_schema_file(open(schema_file_path, 'r'))
    return Validation(config, schema)


class Validation(object):

    def __init__(self, config, schema):
        self._schema = schema
        self._config = config
        self._errors = []
        self._warnings = []

    def validate(self, error_on_deprecated=False):

        section_names = set(self._schema.keys()) | set(self._config.keys())
        for section_name in section_names:

            if not self._schema.get(section_name):
                self._warnings.append("Section %s is not defined in the schema file." % section_name)
                continue

            section_options = self._schema[section_name].values()
            section_has_required_option = any(option for option in section_options if option.get('required'))
            section_is_deprecated = all(option.get('deprecated') for option in section_options)
            section_is_present = section_name in self._config

            best_match = None
            if not section_is_present:
                # We only detect typos using sections not defined in the schema.
                orphan_sections = set(self._config.keys()) - set(self._schema.keys())
                best_match = get_most_probable_typo(section_name, orphan_sections)

            # Note that if a section is deprecated, we do not perform any further validation!
            if section_is_deprecated and section_is_present:
                if error_on_deprecated:
                    self._errors.append("Deprecated section %s is present!" % section_name)
                else:
                    self._warnings.append("Deprecated section %s is present!" % section_name)

            elif section_has_required_option and not section_is_present:
                if best_match:
                    self._errors.append("Missing required section %s (%s is a possible typo!)." % (section_name, best_match))
                else:
                    self._errors.append("Missing required section %s." % section_name)

            elif not section_has_required_option and not section_is_present:
                if best_match:
                    self._warnings.append("Possible typo for section %s : %s." % (section_name, best_match))

            # Section is present but not required, standard validations.
            elif section_is_present:
                self._validate_section(section_name, error_on_deprecated)

    def is_valid(self):
        return not self._errors

    def errors(self):
        return self._errors

    def warnings(self):
        return self._warnings

    def _validate_section(self, section_name, error_on_deprecated):

        # Required fields validation.
        option_names = set(self._schema.get(section_name, {}).keys()) | set(self._config.get(section_name, {}).keys())
        for option_name in option_names:

            if not self._schema.get(section_name, {}).get(option_name):
                self._warnings.append("Option %s of section %s is not defined in the schema file." % (option_name, section_name))
                continue

            option_is_required = self._schema[section_name][option_name].get('required')
            option_is_deprecated = self._schema[section_name][option_name].get('deprecated')
            option_is_present = self._config[section_name].get(option_name)

            best_match = None
            if not option_is_present:
                # We only detect typos using options not defined in the schema.
                orphan_options = set(self._config[section_name].keys()) - set(self._schema[section_name].keys())
                best_match = get_most_probable_typo(option_name, orphan_options)

            # Note that if an option is deprecated, we do not perform any further validation!
            if option_is_deprecated and option_is_present:
                if error_on_deprecated:
                    self._errors.append("Deprecated option %s is present in section %s!" % (option_name, section_name))
                else:
                    self._warnings.append("Deprecated option %s is present in section %s!" % (option_name, section_name))

            elif option_is_required and not option_is_present:
                if best_match:
                    self._errors.append(
                        "Missing required option %s in section %s "
                        "(%s is a possible typo!)." % (option_name, section_name, best_match)
                    )
                else:
                    self._errors.append("Missing required option %s in section %s." % (option_name, section_name))

            elif not option_is_required and not option_is_present:
                if best_match:
                    self._warnings.append("Possible typo for option %s : %s." % (option_name, best_match))

        # Type validation.
        for option_name in self._schema[section_name]:

            option_value = self._config[section_name].get(option_name)

            if not option_value:
                continue

            option_schema = self._schema[section_name][option_name]
            self._validate_option_type(option_name, option_value, option_schema)

    def _validate_option_type(self, option_name, option_value, option_schema):

        expected_type = option_schema.get('type')

        # No type validation to perform.
        if not expected_type:
            return

        if expected_type not in VALID_TYPES:
            self._errors.append("Invalid expected type for option %s : %s." % (option_name, expected_type))
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
            self._errors.append("Invalid value for type %s : %s." % (expected_type, option_value))
