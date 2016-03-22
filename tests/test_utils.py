import unittest

import yaml

from confirm import utils


class LoadConfigFileTestCase(unittest.TestCase):

    def test_yaml(self):
        config_file = """
        section:
          option=value
        """
        config_file_path = 'schema.yaml'

        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

    def test_invalid_yaml(self):
        config_file = """
        [[[section]]]
          option=value
        """
        config_file_path = 'schema.yaml'

        self.assertRaises(yaml.YAMLError, utils.load_config_file, config_file_path, config_file)

    def test_infer_yaml(self):
        config_file = """
        section:
          option=value
        """
        config_file_path = 'schema.notyaml'

        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

    def test_extension_case_insensitive(self):
        config_file = """
        section:
          option=value
        """
        config_file_path = 'schema.yaml'
        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

        config_file_path = 'schema.YAML'
        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

        config_file = """[section]\noption=value"""
        config_file_path = 'schema.CONF'
        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

        config_file_path = 'schema.conf'
        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

    def test_ini_interpolation_compatible(self):
        config_file = """[section]\noption=%(value)s %()s %s"""
        config_file_path = 'schema.ini'
        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)

    def test_yaml_interpolation_compatible(self):
        config_file = """
        section:
          option=%(value)s %()s %s
        """
        config_file_path = 'schema.yaml'
        loaded_config = utils.load_config_file(config_file_path, config_file)

        self.assertIn('section', loaded_config)
