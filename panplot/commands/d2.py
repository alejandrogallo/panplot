import os
import sys
import shutil
import string
import tempfile
import subprocess
import panplot.config
import panplot.templates
import click
import logging


@click.command()
@click.help_option('-h', '--help')
@click.argument(
    "files",
    nargs=-1,
    type=click.Path(),
    #type=click.FilePath
)
@click.option(
    "--xl", "--xlabel",
    help="X label",
    default="x"
)
@click.option(
    "--yl", "--ylabel",
    help="Y label",
    default="y"
)
@click.option(
    "--title",
    help="Y label",
    default=""
)
@click.option(
    "--delimiter", "-d",
    help="Delimiter between the data points",
    default=" "
)
@click.option(
    "--cols",
    help="Columns to use",
    type=(int,int),
    default=(1,2)
)
@click.option(
    "--hlines",
    help="Draw horizontal lines at y values",
    #nargs="*",
    type=list,
    default=[]
)
@click.option(
    "--vlines",
    help="Draw vertical lines at x values",
    #nargs="*",
    type=list,
    default=[]
)
@click.option(
    "--legend",
    help="Legend for the different datasets plotted",
    #nargs="*",
    type=list,
    default=[]
)
@click.option(
    "--lines/--no-lines",
    help="Whether to connect the dots",
)
@click.option(
    "--points/--no-points",
    help="Whether to show the dots",
    default=True
)
@click.option(
    "--grid", "-g",
    help="Show a grid",
)
@click.option(
    "--fmt",
    help="Output format for the plot",
)
@click.option(
    "-o", "--out",
    help="Output scripts",
)
@click.option(
    "--gnuplot", "--gp",
    help="Gnuplot backend",
    default=False,
    is_flag=True
)
@click.option(
    "--matplotlib", "--mpl",
    help="Matplotlib backend",
    default=False,
    is_flag=True
)
def cli(
        files,
        xlabel,
        ylabel,
        title,
        delimiter,
        cols,
        hlines,
        vlines,
        legend,
        lines,
        points,
        grid,
        fmt,
        out,
        gp,
        mpl
        ):
    """Create a general 2d plot"""
    logger = logging.getLogger('2d:cli')
    if not gp and not mpl:
        gp = True
    folder = tempfile.mkdtemp()
    data = [
        os.path.join(folder, "data_%s.txt" % i )
        for i in range(len(files))
    ]
    logger.debug("Tmp folder = %s " % folder)
    logger.debug("Tmp data = %s " % data)
    logger.debug(data)
    for i in range(len(data)):
        with open(data[i], "w+") as fd:
            with open(files[i]) as ffd:
                fd.write(ffd.read())
    data = list(map(os.path.basename, data))
    if gp:
        script = os.path.join(folder, "script.gnuplot")
        open(script, "w+").write(
            panplot.templates.get('gnuplot/2d.j2').render(
                **locals()
            )
        )
    elif mpl:
        script = os.path.join(folder, "script.py")
        open(script, "w+").write(
            panplot.templates.get('matplotlib/2d.j2').render(
                **locals()
            )
        )
    logger.debug("Tmp script = %s " % script)
    if out:
        shutil.move(folder, out)
    else:
        os.chdir(folder)
        if gp:
            subprocess.call(["gnuplot", "-p", script])
        elif mpl:
            subprocess.call([sys.executable, script])
