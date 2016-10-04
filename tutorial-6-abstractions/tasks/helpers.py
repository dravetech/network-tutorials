"""Some helpers for the rest of the tasks."""

import logging
import sys


def get_logger(debug, configure=True):
    """Configure the logging facility."""
    logger = logging.getLogger("tutorial-6-abstractions")

    if not configure:
        return logger

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_site_id(client, name):
    """Return id of a site."""
    result = client.sites.get(name=name)
    logger = get_logger(False, False)

    if result:
        return result[0]['id']
    else:
        logger.error("Site {} doesn't exist.".format(name))
        sys.exit(-1)


def get_host_id(client, site_id, name):
    """Return id of a site."""
    result = client.sites(site_id).devices.get(hostname=name)
    logger = get_logger(False, False)

    if result:
        return result[0]['id']
    else:
        logger.error("Host {} doesn't exist.".format(name))
        sys.exit(-1)
