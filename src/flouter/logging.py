# -*- coding: utf-8 -*-
"""
    flouter.logging
    ~~~~~

    File Description

    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import logging
import sys

default_handler = logging.StreamHandler(sys.stderr)
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)
