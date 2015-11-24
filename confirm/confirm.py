# -*- coding: utf-8 -*-
import sys
import json
import yaml
from validator import validate
from ConfigParser import SafeConfigParser


VALID_OPTIONS = ('required', 'default', 'validator', 'description')
VALID_BOOLEAN_VALUES = ('True', 'False', '1', '0')


if __name__ == '__main__':
    config_parser = SafeConfigParser()
    config_parser.read(sys.argv[1])

    confirm_file_path = sys.argv[2]
    if confirm_file_path.endswith('json'):
        confirmations = json.load(open(confirm_file_path, 'r'))
    elif confirm_file_path.endswith('yaml'):
        confirmations = yaml.load(open(confirm_file_path, 'r'))
    else:
        raise Exception("Invalid confirm file extension : %s." % confirm_file_path.rsplit('.')[-1])

    validate(config_parser, confirmations)
