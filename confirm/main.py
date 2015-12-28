# -*- coding: utf-8 -*-
import argparse
import sys

from confirm.generator import generate_config_parser
from confirm.generator import generate_documentation
from confirm.generator import generate_schema_file
from confirm.generator import append_existing_values
from confirm.validator import validate_config
from confirm.utils import load_config_file, load_schema_file


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
    globals()[command_name](args)


def validate(args):

    schema = load_schema_file(open(args.schema, 'r'))
    config = load_config_file(args.conf, open(args.conf, 'r').read())

    result = validate_config(config, schema, args.detect_typos, error_on_deprecated=args.deprecation)

    for error in result['error']:
        sys.stdout.write('Error : %s\n' % error)

    if args.warnings:
        for warning in result['warning']:
            sys.stdout.write('Warning : %s\n' % warning)

    if args.infos:
        for info in result['info']:
            sys.stdout.write('Info : %s\n' % info)


def migrate(args):

    schema = load_schema_file(open(args.schema, 'r'))
    config = load_config_file(args.conf, open(args.conf, 'r').read())

    config = append_existing_values(schema, config)

    migrated_config = generate_config_parser(config)
    migrated_config.write(sys.stdout)


def document(args):
    schema = load_schema_file(open(args.schema, 'r'))
    documentation = generate_documentation(schema)
    sys.stdout.write(documentation)


def generate(args):
    schema = load_schema_file(open(args.schema, 'r'))
    config_parser = generate_config_parser(schema, include_all=args.include_all)
    config_parser.write(sys.stdout)


def init(args):
    schema = generate_schema_file(open(args.conf, 'r').read())
    sys.stdout.write(schema)
