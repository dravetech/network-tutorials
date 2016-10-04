#!/usr/bin/env python
"""
nsot docstring.
"""

import logging
import sys

from pynsot.client import get_api_client
from pynsot.models import Network

import yaml


logger = logging.getLogger("site_creator")


def _configure_logging(logger, debug):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def create_site(site_data):
    """Create site."""
    site = api.sites.get(name=site_data['name'])

    if not site:
        site = api.sites.post(site_data)
    else:
        site = api.sites(site[0]['id']).put(site_data)
    logger.debug("site: {}".format(site))
    return site


def create_attributes(attributes, site):
    """Create attributes."""
    result = {}
    for resource, attrs in attributes.items():
        for attr_name, attr_options in attrs.items():
            attribute = api.attributes.get(site=site['id'], resource=resource, name=attr_name)

            options = {
                'name': attr_name,
                'resource_name': resource,
            }
            options.update(attr_options)
            if not attribute:
                attribute = api.sites(site['id']).attributes.post(options)
            else:
                attribute = api.sites(site['id']).attributes(attribute[0]['id']).put(options)
            result[attr_name] = attribute
            logger.debug("attribute: {}".format(attribute))
    return result


def _create_networks(networks, service, site):
    result = {}

    for net_type, prefix in networks.items():
        network = api.networks.get(site=site['id'], cidr=prefix, service=service, type=net_type)
        data = {
            'attributes': {
                'type': net_type,
                'service': service
            },
            'cidr': prefix
        }
        if not network:
            network = api.sites(site['id']).networks.post(data)
        else:
            network = api.sites(site['id']).networks(network[0]['id']).put(data)
        logger.debug("network: {}".format(network))
        result[net_type] = network
    return result


def service_fabric_links(data, networks):
    logger.info(data)
    logger.info(networks)


def service_loopbacks(devices, network):
    logger.info(devices)
    logger.info(network)
    net = Network(client=api, site_id=network['site_id'],
                  cidr='{}/{}'.format(network['network_address'], network['prefix_length']))
    logger.info(dir(net))
    logger.info(net.next())



def create_service(name, data, site, devices):
    result = {'networks': _create_networks(data['network_ranges'], name, site), 'services': {}}
    logger.info(result)

    #  if name == 'fabric_links':
    #  result['services']['fabric_links'] = service_fabric_links(data, result['networks'])
    if name == 'loopbacks':
        result['services']['loopbacks'] = service_loopbacks(devices,
                                                            result['networks']['loopbacks'])

    return result


def create_devices(devices, site):
    """Create devices."""
    result = {}

    for host, data in devices.items():
        device = api.devices.get(site=site['id'], hostname=host)
        data = {
            'attributes': data,
            'hostname': host
        }
        if not device:
            device = api.sites(site['id']).devices.post(data)
        else:
            device = api.sites(site['id']).devices(device[0]['id']).put(data)
        result[host] = device
        logger.debug("device: {}".format(device))
    return result

if __name__ == "__main__":
    with open('service.yaml', 'r') as f:
        data = yaml.load(f.read())

    _configure_logging(logger, debug=False)

    global api
    api = get_api_client()

    site = create_site(data['site'])
    attributes = create_attributes(data['attributes'], site)
    devices = create_devices(data['devices'], site)

    services = {}
    for svc, svc_data in data['services'].items():
        services[svc] = create_service(svc, svc_data, site, devices)
