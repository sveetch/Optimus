"""
Logging
=======

Optimus makes usage of logging during its processes to inform user about
what it is doing or errors that occured.

To be more readable, its logger is configured to be colored using
``colorlog`` package.

"""
import logging

import colorlog


def set_loggers_level(names, level=logging.CRITICAL):
    """
    Set a log level on multiple loggers.

    Arguments:
        names (list): A list of logger names to set level.

    Keyword Arguments:
        level (integer): Logging level to set on all given logger names. Default to
            value from ``logging.CRITICAL``.
    """
    for item in names:
        logging.getLogger(item).setLevel(level)


def init_logger(level, printout=True):
    """
    Initialize app logger to configure its level/handler/formatter/etc..

    Arguments:
        level (str): Level name (``debug``, ``info``, etc..).

    Keyword Arguments:
        printout (bool): If False, logs will never be outputed.

    Returns:
        logging.Logger: Application logger.
    """
    root_logger = logging.getLogger("optimus")
    root_logger.setLevel(level)

    # Redirect outputs to the void space, mostly for usage within unittests
    if not printout:
        from io import StringIO

        dummystream = StringIO()
        handler = logging.StreamHandler(dummystream)
    # Standard output with colored messages
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(asctime)s - %(log_color)s%(message)s", datefmt="%H:%M:%S"
            )
        )

    root_logger.addHandler(handler)

    return root_logger
