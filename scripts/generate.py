# -*- coding: utf-8 -*-
import sys
import argparse

import yaml

from confirm.generator import generate_config_parser


parser = argparse.ArgumentParser(description='Generates a template configuration file from a confirm schema.')
parser.add_argument('schema', help='Schema file path.')
parser.add_argument('-a', '--all', dest='include_all', action="store_true", help='Include all the options from the schema.')
args = parser.parse_args()

if __name__ == '__main__':

    schema = yaml.load(open(args.schema, 'r'))
    config_parser = generate_config_parser(schema, include_all=args.include_all)
    config_parser.write(sys.stdout)
