# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

import click

from confirm.generator import generate_config_parser
from confirm.generator import generate_documentation
from confirm.generator import generate_schema_file
from confirm.generator import append_existing_values
from confirm.validator import validator_from_config_file
from confirm.utils import load_config_file, load_schema_file


@click.group()
def cli():
    """Simple Python configuration file management."""
    pass


@cli.command(short_help='Validate a configuration against a schema')
@click.argument('schema_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('config_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.option('--deprecation', '-d', is_flag=True, default=False, help='Handles deprecated options / sections as errors.')
def validate(schema_file, config_file, deprecation):
    '''Validate a configuration file against a confirm schema.'''

    result = validator_from_config_file(config_file, schema_file)
    result.validate(error_on_deprecated=deprecation)

    for error in result.errors():
        click.secho('Error   : %s' % error, err=True, fg='red')

    for warning in result.warnings():
        click.secho('Warning : %s' % warning, err=True, fg='yellow')


@cli.command(short_help='Migrate a configuration using a schema')
@click.argument('schema_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('config_file', type=click.Path(exists=True, readable=True, dir_okay=False))
def migrate(schema_file, config_file):
    '''Migrates a configuration file using a confirm schema.'''

    schema = load_schema_file(open(schema_file, 'r'))
    config = load_config_file(config_file, open(config_file, 'r').read())

    config = append_existing_values(schema, config)

    migrated_config = generate_config_parser(config)
    migrated_config.write(sys.stdout)


@cli.command(short_help='Create reST doc from schema')
@click.argument('schema_file', type=click.Path(exists=True, readable=True, dir_okay=False))
def document(schema_file):
    '''Generate reStructuredText documentation from a confirm schema.'''
    schema = load_schema_file(open(schema_file, 'r'))
    documentation = generate_documentation(schema)
    sys.stdout.write(documentation)


@cli.command(short_help='Create conf template from schema')
@click.argument('schema_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.option('--all-options', '-a', is_flag=True, default=False, help='Include all options from the schema.')
def generate(schema_file, all_options):
    '''Generates a template configuration file from a confirm schema.'''
    schema = load_schema_file(open(schema_file, 'r'))
    config_parser = generate_config_parser(schema, include_all=all_options)
    config_parser.write(sys.stdout)


@cli.command(short_help='Initialize schema from existing conf')
@click.argument('config_file', type=click.Path(exists=True, readable=True, dir_okay=False))
def init(config_file):
    '''Initialize a confirm schema from an existing configuration file.'''
    schema = generate_schema_file(open(config_file, 'r').read())
    sys.stdout.write(schema)
