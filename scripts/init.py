# -*- coding: utf-8 -*-
import sys
import argparse
from ConfigParser import SafeConfigParser

import yaml

from confirm.generator import generate_schema_file


parser = argparse.ArgumentParser(description='Initialize a confirm schema from an existing configuration file.')
parser.add_argument('conf', help='Configuration file path.')
args = parser.parse_args()

if __name__ == '__main__':

    config_parser = SafeConfigParser()
    config_parser.read(args.conf)
    config_file_content = open(args.conf, 'r').read()

    schema = generate_schema_file(config_parser, config_file_content)
    sys.stdout.write(yaml.dump(schema, default_flow_style=False))
