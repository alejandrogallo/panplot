import os
import logging
import sys
import panplot.config

logger = logging.getLogger('templates')

def get_dir():
    """Get directory where templates are stored
    :returns: Path to the directory

    """
    return [
        os.path.dirname(__file__),
        panplot.config.get_templates_folder()
    ]


def get(name):
    """Get template by name
    :returns: Jinja2 template

    """
    import jinja2
    for d in get_dir():
        filepath = os.path.join(d, name)
        if not os.path.exists(filepath):
            continue
        with open(filepath) as fd:
            return jinja2.Template(fd.read())
    logger.exception('No template {} found'.format(name))

