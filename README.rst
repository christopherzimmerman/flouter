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
         return request



.. _Flask: https://www.palletsprojects.com/p/flask/
.. _pip: https://pip.pypa.io/en/stable/quickstart/
