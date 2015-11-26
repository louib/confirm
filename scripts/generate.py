# -*- coding: utf-8 -*-
import sys
import argparse
from ConfigParser import SafeConfigParser

import yaml

from confirm.generator import generate_config_parser


parser = argparse.ArgumentParser(description='Generates a template configuration file from a confirm schema.')
parser.add_argument('schema', help='Schema file path.')
args = parser.parse_args()

if __name__ == '__main__':

    schema = yaml.load(open(args.schema, 'r'))
    config_parser = generate_config_parser(schema)
    config_parser.write(sys.stdout)
