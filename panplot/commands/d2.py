import os
import sys
import shutil
import string
import tempfile
import subprocess
import panplot.config
import panplot.templates


class Command(panplot.commands.Plot2D):

    def init(self):

        self.parser = self.get_subparsers().add_parser(
            "d2",
            help="General 2d plot"
        )


        self.init_parsers()

    def init_parsers(self):

        panplot.commands.Plot2D.init(self)

        self.parser.add_argument(
            "-o", "--out",
            help="Output scripts",
            action="store"
        )

        self.parser.add_argument(
            "--gnuplot", "--gp",
            help="Gnuplot backend",
            action="store_true"
        )

        self.parser.add_argument(
            "--matplotlib", "--mpl",
            help="Matplotlib backend",
            action="store_true"
        )

    def get_gnuplot_template(self):
        return panplot.templates.get('gnuplot/2d.j2').render(
            args=self.args
        )

    def get_matplotlib_template(self):
        return panplot.templates.get('matplotlib/2d.j2').render(
            args=self.args
        )

    def main(self):
        if not self.args.gnuplot and not self.args.matplotlib:
            self.args.gnuplot = True
        folder = tempfile.mkdtemp()
        data = [
            os.path.join(folder, "data_%s.txt" % i )
            for i in range(len(self.args.data))
        ]
        self.logger.debug("Tmp folder = %s " % folder)
        self.logger.debug("Tmp data = %s " % data)
        self.logger.debug(self.args.data)
        for i in range(len(self.args.data)):
            with open(data[i], "w+") as fd:
                fd.write(self.args.data[i].read())
        self.args.data = list(map(os.path.basename, data))
        if self.args.gnuplot:
            script = os.path.join(folder, "script.gnuplot")
            open(script, "w+").write(self.get_gnuplot_template())
        elif self.args.matplotlib:
            script = os.path.join(folder, "script.py")
            open(script, "w+").write(self.get_matplotlib_template())
        self.logger.debug("Tmp script = %s " % script)
        if self.args.out:
            shutil.move(folder, self.args.out)
        else:
            os.chdir(folder)
            if self.args.gnuplot:
                subprocess.call(["gnuplot", "-p", script])
            elif self.args.matplotlib:
                subprocess.call([sys.executable, script])
