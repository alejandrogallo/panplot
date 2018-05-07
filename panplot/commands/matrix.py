import os
import sys
import shutil
import string
import tempfile
import subprocess
import panplot.config
import panplot.templates
import panplot.commands.d2

class Command(panplot.commands.d2.Command):

    def init(self):


        self.parser = self.get_subparsers().add_parser(
            "matrix",
            help="Plot a 2d matrix"
        )
        panplot.commands.d2.Command.init_parsers(self)


    def get_gnuplot_template(self):
        raise Exception("Not implemented")
        return panplot.templates.get('gnuplot/matrix.j2').render(
            args=self.args
        )

    def get_matplotlib_template(self):
        return panplot.templates.get('matplotlib/matrix.j2').render(
            args=self.args
        )
