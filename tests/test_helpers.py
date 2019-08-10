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

GET_FILE_CONTENT = """
# simple get
def get():
    return 'Hello World'
"""


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

    def test_file_to_route_nested_named_params(self, tmpdir):
        """ tests that nested routes are handled appropriately
        by the parser
        """

        # setup
        f = tmpdir.mkdir("api").mkdir("_foo").join("_bar.py")
        f.write(EMPTY_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes
        assert found.route_url == "/api/<foo>/<bar>/"

    def test_methods_imported_from_file(self, tmpdir):
        """tests that methods can be imported from a found
        file path
        """

        # setup
        f = tmpdir.mkdir("api").join("index.py")
        f.write(GET_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes
        assert "get" in found.methods

    def test_methods_imported_from_file_callable(self, tmpdir):
        """tests that imported functions can be called and return
        expected result"""

        # setup
        f = tmpdir.mkdir("api").join("index.py")
        f.write(GET_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes
        assert found.methods["get"]() == "Hello World"

    def test_methods_have_proper_name(self, tmpdir):
        """tests that function names are properly related to
        api route name"""

        # setup
        f = tmpdir.mkdir("api").join("index.py")
        f.write(GET_FILE_CONTENT)

        # test
        found, *_ = Router(tmpdir.strpath).routes

        print(found.function.__name__)

        assert found.function.__name__ == "api_index"
