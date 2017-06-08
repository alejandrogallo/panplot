
import os
import configparser
import panplot.utils
import logging

logger = logging.getLogger("config")

CONFIGURATION = None
DEFAULT_MODE = "document"


def get_config_folder():
    return os.path.join(
        os.path.expanduser("~"), ".panplot"
    )


def get_cache_folder():
    return os.path.join(
        get_config_folder(), "cache"
    )


def get_config_file():
    return os.path.join(
        get_config_folder(), "config"
    )


def get_scripts_folder():
    return os.path.join(
        get_config_folder(), "scripts"
    )


def get_configuration():
    global CONFIGURATION
    if CONFIGURATION is None:
        CONFIGURATION = Configuration()
    return CONFIGURATION


class Configuration(configparser.ConfigParser):

    default_info = {
      "settings": dict()
    }

    DEFAULT_DIR_LOCATION = get_config_folder()

    DEFAULT_SCRIPTS_LOCATION = get_scripts_folder()

    DEFAULT_FILE_LOCATION = get_config_file()

    logger = logging.getLogger("Configuration")

    def __init__(self):
        configparser.ConfigParser.__init__(self)
        self.initialize()

    def handle_includes(self):
       if "include" in self.keys():
           for name in self["include"]:
               self.logger.debug("including %s" % name)
               self.read(os.path.expanduser(self.get("include", name)))

    def initialize(self):
        if not os.path.exists(self.DEFAULT_DIR_LOCATION):
            os.makedirs(self.DEFAULT_DIR_LOCATION)
        if not os.path.exists(self.DEFAULT_SCRIPTS_LOCATION):
            os.makedirs(self.DEFAULT_SCRIPTS_LOCATION)
        if os.path.exists(self.DEFAULT_FILE_LOCATION):
            self.read(self.DEFAULT_FILE_LOCATION)
            self.handle_includes()
        else:
            for section in self.default_info:
                self[section] = {}
                for field in self.default_info[section]:
                    self[section][field] = self.default_info[section][field]
            with open(self.DEFAULT_FILE_LOCATION, "w") as configfile:
                self.write(configfile)

    def save(self):
        fd = open(self.DEFAULT_FILE_LOCATION, "w")
        self.write(fd)
        fd.close()
