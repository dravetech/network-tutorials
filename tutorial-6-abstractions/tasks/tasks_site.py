"""Tasks to manipulate sites"""

import invoke

from pynsot.client import get_api_client

from pynsot.vendor.slumber.exceptions import HttpClientError

import helpers

import yaml

import sys


@invoke.task
def create(ctx, name, description="", debug=False):
    """Create a site."""
    global logger
    logger = helpers.get_logger(debug)

    client = get_api_client()
    site = client.sites.get(name=name)

    site_data = {
        'name': name,
        'description': description,
    }

    if not site:
        site = client.sites.post(site_data)
    else:
        site = client.sites(site[0]['id']).put(site_data)

    logger.info(site)
    return site


@invoke.task
def add_atribbutes(ctx, site, filename="data/attributes.yml", debug=False):
    """Add attributes to a site."""
    global logger
    logger = helpers.get_logger(debug)

    client = get_api_client()
    with open(filename, 'r') as f:
        attributes = yaml.load(f.read())['attributes']

    site_id = helpers.get_site_id(client, site)

    result = {}
    for resource, attrs in attributes.items():
        for attr_name, attr_options in attrs.items():
            attribute = client.sites(site_id).attributes.get(resource=resource, name=attr_name)

            options = {
                'name': attr_name,
                'resource_name': resource,
            }
            options.update(attr_options)
            try:
                if not attribute:
                    logger.info("Creating attribute: {}".format(options))
                    attribute = client.sites(site_id).attributes.post(options)
                else:
                    logger.info("Updating attribute: {}".format(attribute))
                    attribute = client.sites(site_id).attributes(attribute[0]['id']).put(options)
            except HttpClientError as e:
                logger.error(e)
                logger.error(e.response.json())
                sys.exit(-1)

            result[attr_name] = attribute

    return result


@invoke.task
def add_devices(ctx, site, filename="data/devices.yml", debug=False):
    """Add devices to a site."""
    global logger
    logger = helpers.get_logger(debug)

    client = get_api_client()
    with open(filename, 'r') as f:
        devices = yaml.load(f.read())['devices']

    site_id = helpers.get_site_id(client, site)

    result = {}
    for host, data in devices.items():
        device = client.sites(site_id).devices.get(hostname=host)
        data = {
            'attributes': data,
            'hostname': host
        }
        if not device:
            logger.info("Creating device: {}".format(data))
            device = client.sites(site_id).devices.post(data)
        else:
            logger.info("Updating device: {}".format(device))
            device = client.sites(site_id).devices(device[0]['id']).put(data)
        result[host] = device

    return result


@invoke.task
def deploy(ctx, site, commit=False):
    """Deploy a site."""
    check_mode = "-C" if not commit else ""
    cli = "ansible-playbook playbook_configure.yml -l {} {}".format(site,
                                                                    check_mode)
    invoke.run(cli)


@invoke.task
def verify(ctx, site):
    """Verify site is healthy."""
    cli = "ansible-playbook playbook_verify.yml -l {}".format(site)
    invoke.run(cli)
