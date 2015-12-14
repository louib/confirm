# -*- coding: utf-8 -*-
import argparse
import sys
from ConfigParser import SafeConfigParser

import yaml

from confirm.generator import generate_config_parser
from confirm.generator import generate_documentation
from confirm.generator import generate_schema_file
from confirm.generator import append_existing_values
from confirm.validator import validate_config


PARSERS = {}

PARSERS['validate'] = argparse.ArgumentParser(description='Validate a configuration file against a confirm schema.', prog="confirm validate")
PARSERS['validate'].add_argument('schema', help='Schema file path.')
PARSERS['validate'].add_argument('conf', help='Configuration file path.')
PARSERS['validate'].add_argument('-t', '--typos', action="store_true", dest="detect_typos", help='Turn on typos detection.')
PARSERS['validate'].add_argument('-w', '--warnings', action="store_true", dest="warnings", help='Show warnings.')
PARSERS['validate'].add_argument('-i', '--infos', action="store_true", dest="infos", help='Show infos.')
PARSERS['validate'].add_argument('-d', '--deprecation', action="store_true", dest="deprecation", help='Handles deprecated options / sections as errors.')

PARSERS['migrate'] = argparse.ArgumentParser(description='Migrates a configuration file using a confirm schema.', prog="confirm migrate")
PARSERS['migrate'].add_argument('schema', help='Schema file path.')
PARSERS['migrate'].add_argument('conf', help='Configuration file path.')

PARSERS['document'] = argparse.ArgumentParser(description='Generate reStructuredText documentation from a confirm schema.', prog="confirm document")
PARSERS['document'].add_argument('schema', help='Schema file path.')

PARSERS['generate'] = argparse.ArgumentParser(description='Generates a template configuration file from a confirm schema.', prog="confirm generate")
PARSERS['generate'].add_argument('schema', help='Schema file path.')
PARSERS['generate'].add_argument('-a', '--all', dest='include_all', action="store_true", help='Include all the options from the schema.')

PARSERS['init'] = argparse.ArgumentParser(description='Initialize a confirm schema from an existing configuration file.', prog="confirm init")
PARSERS['init'].add_argument('conf', help='Configuration file path.')


MAIN_HELP = """
usage: confirm <command> [<args>]

The possible confirm commands are:
   validate   Validate a configuration file against a confirm schema.
   migrate    Migrates a configuration file using a confirm schema.
   document   Generate reStructuredText documentation from a confirm schema.
   generate   Generates a template configuration file from a confirm schema.
   init       Initialize a confirm schema from an existing configuration file.
"""


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(MAIN_HELP.lstrip('\n'))
        sys.exit(1)

    command_name = sys.argv[1]

    # Removing the command name from the CLI arguments.
    sys.argv = sys.argv[:1] + sys.argv[2:]

    if command_name not in PARSERS:
        sys.stderr.write(MAIN_HELP.lstrip('\n'))
        sys.exit(1)

    args = PARSERS[command_name].parse_args()
    locals()[command_name](args)


def validate(args):

    schema = yaml.load(open(args.schema, 'r'))
    config_parser = SafeConfigParser()
    config_parser.read(args.conf)
    result = validate_config(config_parser, schema, args.detect_typos, error_on_deprecated=args.deprecation)

    for error in result['error']:
        sys.stdout.write('Error : %s\n' % error)

    if args.warnings:
        for warning in result['warning']:
            sys.stdout.write('Warning : %s\n' % warning)

    if args.infos:
        for info in result['info']:
            sys.stdout.write('Info : %s\n' % info)


def migrate(args):
    schema = yaml.load(open(args.schema, 'r'))
    config_parser = SafeConfigParser()
    config_parser.read(args.conf)

    config = append_existing_values(schema, config_parser)
    migrated_config = generate_config_parser(config)

    migrated_config.write(sys.stdout)


def document(args):
    schema = yaml.load(open(args.schema, 'r'))
    documentation = generate_documentation(schema)
    sys.stdout.write(documentation)


def generate(args):
    schema = yaml.load(open(args.schema, 'r'))
    config_parser = generate_config_parser(schema, include_all=args.include_all)
    config_parser.write(sys.stdout)


def init(args):
    config_parser = SafeConfigParser()
    config_parser.read(args.conf)
    config_file_content = open(args.conf, 'r').read()

    schema = generate_schema_file(config_parser, config_file_content)
    sys.stdout.write(yaml.dump(schema, default_flow_style=False))
