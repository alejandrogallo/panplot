import os
import re
import subprocess
import panplot.config
import panplot.commands
import click
import logging


logger = logging.getLogger("external")


def get_command_help(path):
    magic_word = '.*panplot-short-help: *(.*)'
    with open(path) as fd:
        for line in fd:
            m = re.match(magic_word, line)
            if m:
                return m.group(1)
    return "No help message available"


def export_variables():
    """Export environment variables so that external script can access to
    the information
    """
    os.environ["PANPLOT_CONFIG_PATH"] = panplot.config.get_config_folder()
    os.environ["PANPLOT_CONFIG_FILE"] = panplot.config.get_config_file()
    os.environ["PANPLOT_SCRIPTS_PATH"] = panplot.config.get_scripts_folder()


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[]
    )
)
@click.argument("flags", nargs=-1)
@click.pass_context
def external_cli(ctx, flags):
    script = ctx.obj
    cmd = [script['path']] + list(flags)
    logger.debug("Calling {}".format(cmd))
    export_variables()
    subprocess.call(cmd)
