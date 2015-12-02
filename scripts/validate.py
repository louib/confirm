# -*- coding: utf-8 -*-
import argparse
from ConfigParser import SafeConfigParser

import yaml

from confirm.validator import validate_config

parser = argparse.ArgumentParser(description='Validate a configuration file against a confirm schema.')
parser.add_argument('schema', help='Schema file path.')
parser.add_argument('conf', help='Configuration file path.')
args = parser.parse_args()

if __name__ == '__main__':

    schema = yaml.load(open(args.schema, 'r'))
    config_parser = SafeConfigParser()
    config_parser.read(args.conf)
    validate_config(config_parser, schema)
