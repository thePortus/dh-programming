#!/usr/bin/python
""" /library

Library of helper objects/functions for DH students so that they can quickly
load/save common kinds of data as well as fetch data from the web.

This is a module init file, where various files, objects, and functions
are imported for easy access at the module level.

"""

from .web import WebPage
from .files import TextFile, CSVFile
