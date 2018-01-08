import os
import re
import argparse
import subprocess
import panplot.config
import panplot.commands


class Command(panplot.commands.Command):

    def init(self, path):
        self.script_path = path

        self.parser = self.get_subparsers().add_parser(
            self.get_command_name(),
            add_help=False,
            help=self.get_command_help()
        )

        self.parser.add_argument(
            "-h", "--help",
            action="store_true"
        )

        self.parser.add_argument(
            "args",
            help="Arguments",
            nargs=argparse.REMAINDER,
            action="store"
        )

    def get_command_name(self):
        m = re.match(r"^.*panplot-(.*)$", self.script_path)
        return m.group(1) if m else None

    def get_command_help(self):
        magic_word = panplot.config.get("scripts-short-help-regex")
        with open(self.script_path) as fd:
            for line in fd:
                m = re.match(magic_word, line)
                if m:
                    return m.group(1)
        return "No help message available"

    def export_variables(self):
        """Export environment variables so that external script can access to
        the information
        """
        os.environ["PANPLOT_CONFIG_PATH"] = panplot.config.get_config_folder()
        os.environ["PANPLOT_CONFIG_FILE"] = panplot.config.get_config_file()
        os.environ["PANPLOT_SCRIPTS_PATH"] = panplot.config.get_scripts_folder()
        os.environ["PANPLOT_VERBOSE"] = "-v" if self.args.verbose else ""

    def main(self):
        if self.args.help:
            self.args.args = ['-h'] + self.args.args
        self.export_variables()
        subprocess.call([self.script_path] + self.args.args)
