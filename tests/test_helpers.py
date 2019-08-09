# -*- coding: utf-8 -*-
"""
    tests.helpers
    ~~~~~

    Tests helper functions

    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
from flouter.router import Router

EMPTY_FILE_CONTENT = "# empty"


class TestFiles(object):
    """
    Faking directories and testing file helpers
    """

    def test_find_files_from_path(self, tmpdir):
        """tests our globber using pytest tempdir"""

        # setup
        api = tmpdir.mkdir("api")
        f1 = api.join("index.py")
        f2 = api.mkdir("foo").join("index.py")
        f1.write(EMPTY_FILE_CONTENT)
        f2.write(EMPTY_FILE_CONTENT)

        # test
        found = Router(tmpdir.strpath).routes
        assert len(found) == 2

    def test_file_remove_base_path(self, tmpdir):
        """ tests removal of clutter from filename """

        # setup
        f = tmpdir.mkdir("api").join("index.py")
        f.write(EMPTY_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes
        assert found.clipped_path == "\\api\\index.py"

    def test_file_to_route_remove_index(self, tmpdir):
        """ tests route creation from a clipped file"""

        # setup
        f = tmpdir.mkdir("api").join("index.py")
        f.write(EMPTY_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes
        assert found.route_url == "/api/"

    def test_file_to_route_named_params(self, tmpdir):
        """ tests that named parameters are converted into
        the appropriate route
        """

        # setup
        f = tmpdir.mkdir("api").join("_foo.py")
        f.write(EMPTY_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes
        assert found.route_url == "/api/<foo>/"
