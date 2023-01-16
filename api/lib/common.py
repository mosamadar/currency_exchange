"""
This module exposes commonly used initialization patterns
that a number of library and lambda modules use.
"""
import logging

# global pool dictionary reference
POOL_DICT = {}
PUBLIC_KEYS = {}


def initilalized_logger(name):
    """
    Returns an initialized logger with pre-configured handlers.
    """
    # The Lambda environment pre-configures a handler logging to stderr.
    # If a handler is already configured, `.basicConfig` does not execute.
    # Thus we set the level directly.
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s - %(message)s')
    logger = logging.getLogger(name)
    return logger
