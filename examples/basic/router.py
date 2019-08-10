"""
Basic usage example of registering routes
from a file structure to valid flask api routes.

The following file uses the directory structure defined
in routes to create a very simple endpoint with two routes:

/api/
/api/<variable>

It supports GET requests on both endpoints

GET /api/ will return "Welcome to the Base API path"

GET /api/<variable> will return "The variable is <variable>"
"""

import os

from flask import Flask
from flouter import Router

app = Flask(__name__)

route_dir = os.getcwd() + "/routes/"
router = Router(route_dir)

router.register_routes(app)

app.run()
