from subprocess import call
from subprocess import Popen, PIPE
import logging
import os
import re
import panplot.config
import panplot.commands

logger = logging.getLogger("utils")



def get_arg(arg, default=None):
    try:
        val = getattr(panplot.commands.get_args(), arg)
    except AttributeError:
        try:
            val = os.environ["PANPLOT_"+arg.upper()]
        except KeyError:
            val = default
    return val


def which(program):
    # source
    # stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None
