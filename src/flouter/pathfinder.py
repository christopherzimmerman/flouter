# -*- coding: utf-8 -*-
"""
    flouter.pathfinder
    ~~~~~

    Primarily functions related to finding paths for
    routes from a directory structure.  <3 glob

    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import os


class PathFinder(object):
    """Searches a directory to find python files matching
    flouter's naming convention, and converts them to Path
    objects that can be easily converted to Flask routes when
    an app uses flouter to register routes

    Parameters
    ----------
    path : str
        path pointing to routes for an application
    """

    def __init__(self, path):
        # initialize passed in vars
        self.path = path

        # initialize more useful and normalized path variable
        self.normpath = os.path.normpath(path)
