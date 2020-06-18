import unittest

from click.testing import CliRunner

from idmtools_cli.cli.config_file import config


class TestConfigFile(unittest.TestCase):

    def test_slugify(self):
        from idmtools_cli.cli.config_file import slugify
        self.assertEqual(slugify("abc"), "ABC")
        self.assertEqual(slugify("abc def"), "ABC_DEF")

    def test_create_command(self):
        runner = CliRunner()
        result = runner.invoke(config, ['--config_path', 'blah', 'create', '--block_name', 'MY_block', '--platform','COMPS'])
        print(result.output)