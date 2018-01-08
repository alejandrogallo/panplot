import os
import sys


def get_dir():
    """Get directory where templates are stored
    :returns: Path to the directory

    """
    return os.path.dirname(__file__)


def get(name):
    """Get template by name
    :returns: Jinja2 template

    """
    import jinja2
    filepath = os.path.join(get_dir(), name)
    with open(filepath) as fd:
        return jinja2.Template(fd.read())
