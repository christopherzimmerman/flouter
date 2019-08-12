Flouter
============

Flouter (Flask Router) is a convenience add-on for the `Flask`_ library.  It converts a directory structure into valid routes
for a Flask application.  This allows developers to quickly layout complex applications, and easily navigate
to existing code.  This library is under heavy development and may not yet support a feature you need.  If that is
the case, please submit a feature request so the library can continue to improve.


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U flouter


Basic Usage
-----------

Flouter will convert the following ``routes`` directory structure...

.. code-block:: text

    routes/
    |-- api/
        |-- index.py
        |-- echo.py
        |-- _foo.py

...to the corresponding routes in a flask application.

.. code-block:: text

    /api/
    /api/echo/
    /api/<foo>

In one of these files, methods are defined by simple named functions that are called when the appropriate HTTP request
is passed to the route.

.. code-block:: python

     # echo.py

     def get():
         return 'Hello World'

     def post(request):
         # returns are turned into valid responses by the library
         return request.json


An example usage of this library is included in `examples/basic`_

.. code-block:: python

    # main.py
    import os

    from flask import Flask
    from src.flouter import Router

    app = Flask(__name__)

    route_dir = os.getcwd() + "/routes/"
    router = Router(route_dir)

    router.register_routes(app)

    app.run()

A `Router` object also allows ``route_params`` to be defined, which allow methods to access
important elements of an application without having to explicitly import these into
every single file, which could quickly become annoying.  The default value for this dictionary
contains only the ``flask.request`` object, which you can access in any function by adding
the ``request`` kwarg.  However, you can extend this to pass in any important variables you
may have.

.. code-block:: python

    # main.py

    d = dict(
        my_constant=10,
    )

    router = Router(directory, route_params=d)

Which enables ``my_constant`` to be passed to any route child function.

.. code-block:: python

    # /api/index.py

    def get(my_constant):
        return my_constant






.. _Flask: https://www.palletsprojects.com/p/flask/
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _examples/basic: examples/basic
