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

from flask.logging import has_level_handler

default_handler = logging.StreamHandler(sys.stderr)
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)


def create_logger(router):
    """Get the logger for a router and configure it if needed

    When :attr:`~flouter.Router.debug` is enabled, set the logger level to
    :data:`logging.DEBUG` if it is not set

    Uses flasks :func:`has_level_handler` to ensure that a logger has a handler
    for its effective level.
    """
    logger = logging.getLogger(router.name)

    if router.debug and not logger.level:
        logger.setLevel(logging.DEBUG)

    if not has_level_handler(logger):
        logger.addHandler(default_handler)

    return logger
