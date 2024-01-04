import functools
import logging
import sys
from urllib.parse import urlparse


@functools.lru_cache(maxsize=0)
def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create handlers for logging to the standard output and a file
    stdoutHandler = logging.StreamHandler(stream=sys.stdout)
    errHandler = logging.StreamHandler(stream=sys.stderr)

    # Set the log levels on the handlers
    stdoutHandler.setLevel(logging.DEBUG)
    errHandler.setLevel(logging.ERROR)

    # Create a log format using Log Record attributes
    fmt = logging.Formatter(
        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
    )

    # Set the log format on each handler
    stdoutHandler.setFormatter(fmt)
    errHandler.setFormatter(fmt)

    # Add each handler to the Logger object
    logger.addHandler(stdoutHandler)
    logger.addHandler(errHandler)

    return logger


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
