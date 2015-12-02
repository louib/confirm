# -*- coding: utf-8 -*-
import argparse
import sys
from ConfigParser import SafeConfigParser

import yaml

from confirm.validator import validate_config

parser = argparse.ArgumentParser(description='Validate a configuration file against a confirm schema.')
parser.add_argument('schema', help='Schema file path.')
parser.add_argument('conf', help='Configuration file path.')
parser.add_argument('-t', '--typos', action="store_true", dest="detect_typos", help='Turn on typos detection.')
parser.add_argument('-w', '--warnings', action="store_true", dest="warnings", help='Show warnings.')
parser.add_argument('-i', '--infos', action="store_true", dest="infos", help='Show infos.')
args = parser.parse_args()

if __name__ == '__main__':

    schema = yaml.load(open(args.schema, 'r'))
    config_parser = SafeConfigParser()
    config_parser.read(args.conf)
    result = validate_config(config_parser, schema, args.detect_typos)

    for error in result['error']:
        sys.stdout.write('Error : %s\n' % error)

    if args.warnings:
        for warning in result['warning']:
            sys.stdout.write('Warning : %s\n' % warning)

    if args.infos:
        for info in result['info']:
            sys.stdout.write('Info : %s\n' % info)
