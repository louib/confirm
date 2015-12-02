# -*- coding: utf-8 -*-
import sys
import argparse

import yaml

from confirm.generator import generate_documentation


parser = argparse.ArgumentParser(description='Generate reStructuredText documentation from a confirm schema.')
parser.add_argument('schema', help='Schema file path.')
args = parser.parse_args()

if __name__ == '__main__':

    schema = yaml.load(open(args.schema, 'r'))
    documentation = generate_documentation(schema)
    sys.stdout.write(documentation)
