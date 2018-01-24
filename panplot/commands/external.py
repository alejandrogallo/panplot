import os
import re
import argparse
import subprocess
import panplot.config
import panplot.commands


class Command(panplot.commands.Command):

    def init(self, path):

        self._external = True

        self.script_path = path

        self.parser = self.get_subparsers().add_parser(
            self.get_command_name(),
            add_help=False,
            help=self.get_command_help()
        )

        self.parser.add_argument(
            'args',
            help="Arguments",
            default='',
            nargs=argparse.REMAINDER,
            action="store"
        )

    def get_command_name(self):
        m = re.match(r"^.*panplot-(.*)$", self.script_path)
        return m.group(1) if m else None

    def get_command_help(self):
        magic_word = ".*panplot-short-help: *(.*)"
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
        self.logger.debug("Exporting variables")
        self.export_variables()
        # We have to get from the first argument due to the limitation of
        # argparse that REMAINDER needs a non-flag argument first to work.
        # see panplot.command.patch_external_input_args and
        # https://stackoverflow.com/questions/43219022/using-argparse-remainder-at-beginning-of-parser-sub-parser
        cmd = [self.script_path] + self.args.args[1:]
        self.logger.debug("Calling {}".format(cmd))
        subprocess.call(cmd)
