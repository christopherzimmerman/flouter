# -*- coding: utf-8 -*-
"""
    flouter.router
    ~~~~~

    Exposes class for the Flouter library.  Provides an interface
    for adding routes to the flask application

    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import os

from flask import jsonify
from flask import request

from .helpers import _convert_path_to_function
from .helpers import _convert_path_to_route
from .helpers import _extract_methods_from_route
from .helpers import _find_files_from_path
from .helpers import _remove_base_path_from_file
from .logging import logger


class BaseRoute(object):
    """ Takes an arbitrary filename and wraps convenient
    functions to convert it to valid routes/files/functions
    for Router to use

    Parameters
    ----------
    filename : str,
        filename to use to construct a BaseRoute
    base_path: str,
        base_path to be clipped for route generation
    """

    def __init__(self, filename, base_path):
        self.filename = filename
        self.base_path = base_path
        self.methods = _extract_methods_from_route(self.filename)

    @property
    def clipped_path(self):
        return _remove_base_path_from_file(self.base_path, self.filename)

    @property
    def route_url(self):
        return _convert_path_to_route(self.clipped_path)

    @property
    def function_name(self):
        return _convert_path_to_function(self.clipped_path)

    @property
    def function(self):
        """
        Computes a function for a given route, that will be passed
        into a flask app rule.  This will need considerable work
        to ensure that all route decorators can be passed through
        this function and have it work correctly

        Returns
        -------
        fn : wrapped function
        """

        def outer(fn_dict):
            """Returns a function correctly named for a route
            while also properly routing requests where they
            need to go"""

            def inner(**kwargs):
                """Simple wrapper function to handle route
                navigation
                """
                fn = fn_dict.get(request.method.lower())

                if fn is not None:
                    return jsonify(fn(**kwargs))

            inner.__name__ = self.function_name
            return inner

        return outer(self.methods)


class Router(object):
    """ Takes a path and allows routes to be trivially
    registered on an application based on directory structure
    and RESTfully-named functions.  Supports route params,
    and *most* other options that Flask supports adding to
    a route (eventually will be all, but this is in development)

    Parameters
    ----------
    path : str
        path to begin searching for routes
    absolute : bool
        flag regarding if a path is absolute or relative.  This isn't
        really used yet, but I feel like an edge case is going to
        come up eventually that makes this useful and I'd rather
        not have it break existing code
    """

    def __init__(self, path, absolute=False):
        # setting initial values
        self.path = path
        self.absolute = absolute

        # computed paths
        self.routes = self.compute_api_structure()

    @property
    def norm_path(self):
        """standardized path to make switching
        between OS's easier.  Used for computing
        route names and removing the path from
        files

        Returns
        -------
        n : normalized path string
        """
        return os.path.normpath(self.path)

    def compute_api_structure(self):
        """uses a helper function to find files
        from a given path.  Currently uses glob
        in virtually a one line function, but in
        case that implementation changes it's easier
        to wrap it here

        Returns
        -------
        m : [BaseRoute] -- List of base routes for each found file
        """
        return [
            BaseRoute(file, self.norm_path)
            for file in _find_files_from_path(self.norm_path)
        ]

    def register_routes(self, app):
        """
        Adds routes as app rules to a flask application.
        Requires a flask application to be initialized
        before it will be able to add routes

        Parameters
        ----------
        app : a flask application

        Returns
        -------
        None -- adds routes directly to the application
        """

        for route in self.routes:
            fn = route.function
            app.add_url_rule(route.route_url, fn.__name__, fn)
            logger.debug("Adding {} to application".format(route.route_url))
