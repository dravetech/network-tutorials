"""Tasks to manipulate the db."""

from invoke import task
from pynsot.client import get_api_client

from pynsot.vendor.slumber.exceptions import HttpClientError

import helpers

import sys


@task
def reset(ctx, debug=False):
    """Resets the database. All sites and their related data are wiped out."""
    global logger
    logger = helpers.get_logger(debug)

    client = get_api_client()

    for site in client.sites.get():
        logger.info("Deleting site: {}".format(site))
        _reset_resources(client, site['id'])
        _reset_resources(client, site['id'])
        _reset_resources(client, site['id'])
        try:
            client.sites(site['id']).delete()
        except HttpClientError as e:
            logger.error(e)
            logger.error(e.response.json())
            sys.exit(-1)


def _reset_resources(client, site_id):
    resources = ['interfaces', 'networks', 'devices', 'attributes']
    for r in resources:
        path = getattr(client.sites(site_id), r)
        for element in path.get():
            logger.debug("Deleteing {}: {}".format(r, element))
            try:
                path(element['id']).delete()
            except HttpClientError as e:
                logger.debug(e)
                logger.debug(e.response.json())
