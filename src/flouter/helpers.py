# -*- coding: utf-8 -*-
"""
    flouter.helpers
    ~~~~~

    Helper functions only accessed by internal objects

    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import glob
import os
import re
import importlib.util


_ALLOWED_METHODS = {'get', 'post', 'delete', 'put', 'head'}


def _find_files_from_path(path):
    """
    Parameters
    ----------
    path : str
        path to search for files

    Returns
    -------
    paths : list of paths for an application
    """

    # python file extension
    glob_opts = {"pathname": path + "/**/*.py", "recursive": True}

    return glob.glob(**glob_opts)


def _remove_base_path_from_file(base_path, filename):
    """

    Turn a file into a route.  This will probably get more
    complicated to account for multiple OS and strange
    file names

    Parameters
    ----------
    base_path : str
        normalized base path
    filename : str
        filename to remove base_path from

    Returns
    -------
    s : filename with base_path removed
    """
    return filename.replace(base_path, "", 1)


def _convert_path_to_route(clipped_path, index_name="index.py"):
    """
    Parameters
    ----------
    clipped_path : str
        api route with absolute path clipped
    index_name : str
        name of index files to remove.  This is not currently
        able to be altered through Router, but might be worth
        exposing to users eventually if they want to conform
        to a different name than index.py for their index files

    Returns
    -------
    r : str -- route url
    """
    swapped_slashes = clipped_path.replace(os.sep, "/")
    escaped_index = re.escape(index_name)
    rgx = "({})$".format(escaped_index)

    # steps to do stuff, probably can be optimized
    removed_index = re.sub(rgx, "", swapped_slashes)
    inner_links_formatted = re.sub(r"/_([^/]+)/", r"/<\1>/", removed_index)
    final_link_formatted = re.sub(r"_(.*?).py$", r"<\1>/", inner_links_formatted)

    return final_link_formatted


def _extract_methods_from_route(path):
    """
    Extract methods from a given path.  This imports
    an absolute path, although I don't see how this
    is any more dangerous than executing other code
    since you define the path that is imported

    Parameters
    ----------
    path : str
        absolute path to import

    Returns
    -------
    d : dictionary of RESTful methods

    """
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    fns = set(dir(module)) & _ALLOWED_METHODS

    return {fn: getattr(module, fn) for fn in fns}


def _convert_path_to_function(clipped_path):
    """
    Parameters
    ----------
    clipped_path : str
        api route with absolute path clipped

    Returns
    -------
    fn : str -- function name
    """
    components = [comp for comp in clipped_path.split(os.sep) if comp]
    return '_'.join(components)[:-3]

