#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

import panplot.commands
import panplot.utils
import panplot.config


logger = logging.getLogger("panplot")

def main():
    panplot.commands.init()
    panplot.commands.main()

if __name__ == "__main__":
    main()

# vim:set et sw=4 ts=4 ft=python:
