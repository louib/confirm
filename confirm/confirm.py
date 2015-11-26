# -*- coding: utf-8 -*-
import sys
import json
import argparse
from ConfigParser import SafeConfigParser

import yaml

from validator import validate
from generator import generate_config_parser
from generator import generate_documentation
from generator import append_existing_values


parser = argparse.ArgumentParser(description='Simple Python configuration file validation.')
parser.add_argument('command', type=str, choices=['generate', 'validate', 'migrate', 'document'], help='Command to execute.')
parser.add_argument('-c', '--conf', dest='conf', help='Configuration file path.')
parser.add_argument('-s', '--schema', dest='schema', help='Schema file path.')

args = parser.parse_args()

if __name__ == '__main__':

    schema = yaml.load(open(args.schema, 'r'))
    if args.command == 'generate':
        config_parser = generate_config_parser(schema)
        config_parser.write(open('/dev/stdout', 'w'))
    elif args.command == 'document':
        documentation = generate_documentation(schema)
        sys.stdout.write(documentation)
    elif args.command == 'migrate':
        config_parser = SafeConfigParser()
        config_parser.read(args.conf)
        config = append_existing_values(schema, config_parser)
        migrated_config = generate_config_parser(config)
        migrated_config.write(open('/dev/stdout', 'w'))
    elif args.command == 'validate':
        config_parser = SafeConfigParser()
        config_parser.read(args.conf)
        validate(config_parser, schema)
