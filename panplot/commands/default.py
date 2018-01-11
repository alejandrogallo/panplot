import string
import os
import panplot.config
import panplot.commands
import logging


class Command(panplot.commands.Command):

    def init(self):

        self.default_parser.add_argument(
            "-v",
            "--verbose",
            help="Make the output verbose (equivalent to --log DEBUG)",
            default=False,
            action="store_true"
        )

        self.default_parser.add_argument(
            "--log",
            help="Logging level",
            choices=[
                "INFO",
                "DEBUG",
                "WARNING",
                "ERROR",
                "CRITICAL"
                ],
            action="store",
            default="INFO"
        )

    def main(self):
        self.set_args(panplot.commands.get_args())
        log_format = '%(levelname)s:%(name)s:%(message)s'
        if self.args.verbose:
            self.args.log = "DEBUG"
            log_format = '%(relativeCreated)d-'+log_format
        logging.basicConfig(
            level=getattr(logging, self.args.log),
            format=log_format
        )

        commands = panplot.commands.get_commands()

        if self.args.command:
            if self.args.command in commands.keys():
                commands[self.args.command].set_args(self.args)
                commands[self.args.command].main()
