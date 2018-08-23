import os
import panplot
import panplot.config
import logging
import click
import panplot.cli


@click.group(
    cls=panplot.cli.MultiCommand,
    invoke_without_command=True
)
@click.help_option('--help', '-h')
@click.version_option(version=panplot.__version__)
@click.option(
    "-v",
    "--verbose",
    help="Make the output verbose (equivalent to --log DEBUG)",
    default=False,
    is_flag=True
)
@click.option(
    "--log",
    help="Logging level",
    type=click.Choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO"
)
def run(
        verbose,
        log
        ):
    log_format = '%(levelname)s:%(name)s:%(message)s'
    if verbose:
        log = "DEBUG"
        log_format = '%(relativeCreated)d-'+log_format
    logging.basicConfig(
        level=getattr(logging, log),
        format=log_format
    )
