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
from flask.views import MethodView

from .helpers import _convert_path_to_function
from .helpers import _convert_path_to_route
from .helpers import _extract_methods_from_route
from .helpers import _find_files_from_path
from .helpers import _remove_base_path_from_file


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

    def _wraps_fn(self, fn, params):
        """
        Parameters
        ----------
        fn
        params

        Returns
        -------

        """

        def wrapped(**kwargs):
            vn = set(fn.__code__.co_varnames)
            for k in params.keys() & vn:
                kwargs[k] = params.get(k)
            return jsonify(fn(**kwargs))

        wrapped.__name__ = "{}{}".format(self.function_name, fn.__name__)

        return wrapped

    def function(self, params):
        """
        Computes a function for a given route, that will be passed
        into a flask app rule.  This will need considerable work
        into a flask app rule.  This will need considerable work
        to ensure that all route decorators can be passed through
        this function and have it work correctly

        Returns
        -------
        fn : wrapped function
        """

        class Dynamic(MethodView):
            pass

        for name, fn in self.methods.items():
            f = self._wraps_fn(fn, params)
            setattr(Dynamic, name, staticmethod(f))

        return Dynamic


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

    def __init__(self, path, route_params=None):
        # setting initial values
        self.path = path

        if route_params is None:
            self.route_params = {"request": request}
        else:
            self.route_params = route_params

        self.route_params["request"] = request

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
            view = route.function(self.route_params).as_view(route.function_name)
            app.add_url_rule(
                route.route_url,
                view_func=view,
                methods=[m.upper() for m in route.methods],
            )
