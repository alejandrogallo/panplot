import os
import sys
import shutil
import string
import tempfile
import subprocess
import panplot.config


class P2d(panplot.commands.Plot2D):

    def init(self):

        self.parser = self.get_subparsers().add_parser(
            "p2d",
            help="2d plot"
        )

        panplot.commands.Plot2D.init(self)

        self.parser.add_argument(
            "-o", "--out",
            help="Output scripts",
            action="store_true"
        )

        self.parser.add_argument(
            "--gnuplot",
            help="Gnuplot backend",
            action="store_true"
        )

    def get_gunplot_template(self):
        return string.Template("""\
#! /usr/bin/env gnuplot
# created by panplot https://github.com/alejandrogallo/panplot

# set terminal unknown;

set xlabel "$xlabel";
set ylabel "$ylabel";
set title "$title";

plot "data.txt" u 1:2;

""").safe_substitute(**vars(self.args))

    def main(self):
        folder = tempfile.mkdtemp()
        data = os.path.join(folder, "data.txt")
        script = os.path.join(folder, "script.gnuplot")
        self.logger.debug("Tmp folder = %s " % folder)
        self.logger.debug("Tmp data = %s " % data)
        self.logger.debug("Tmp script = %s " % script)
        open(data, "w+").write(self.args.data.read())
        open(script, "w+").write(self.get_gunplot_template())
        if self.args.out:
            shutil.move(folder, self.args.out)
        else:
            os.chdir(folder)
            subprocess.call(["gnuplot", "-p", script])
