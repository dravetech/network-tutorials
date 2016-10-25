"""Tasks to manipulate sites"""

from invoke import task
from pynsot.client import get_api_client

from pynsot.vendor.slumber.exceptions import HttpClientError

import helpers

import yaml

import sys


def _create_networks(client, networks, service, site_id):
    result = {}

    for net_type, prefix in networks.items():
        network = client.sites(site_id).networks.get(cidr=prefix, service=service, type=net_type)
        data = {
            'attributes': {
                'type': net_type,
                'service': service
            },
            'cidr': prefix
        }
        if not network:
            logger.info("Creating network: {}".format(data))
            network = client.sites(site_id).networks.post(data)
        else:
            logger.info("Updating network: {}".format(network))
            network = client.sites(site_id).networks(network[0]['id']).put(data)
        result[net_type] = network
    return result


def _create_subnet(client, site_id, supernet, prefix_length):
    network = client.sites(site_id).networks(supernet['id']).next_network.get(
                                                            prefix_length=prefix_length)
    print(supernet)
    print(network)
    data = {
        'attributes': {
            'type': supernet['attributes']['type'],
            'service': supernet['attributes']['service'],
        },
        'cidr': network[0]
    }
    logger.info("Creating network: {}".format(data))
    network = client.sites(site_id).networks.post(data)
    return network


def _create_interface(client, site_id, device_id, iface_name, link_type,
                      connects_to_device, connects_to_iface, network=None):
    """
    nsot interfaces add --site-id 1 --device 1 --name lo0 --addresses 2001:db8:b33f::100/128 -a
    link_type=loopback -a connects_to_device=loopback -a connects_to_iface=lo0
    """
    iface = [i for i in client.sites(site_id).devices(device_id).interfaces.get()
             if i['name'] == iface_name]

    if not iface:
        assigned = client.sites(site_id).networks(network['id']).next_address.get() \
                   if network else []
    else:
        if iface[0]['addresses']:
            assigned = iface[0]['addresses']
        else:
            assigned = client.sites(site_id).networks(network['id']).next_address.get() \
                      if network else []
            print(assigned)

    data = {
        'name': iface_name,
        'device': device_id,
        'addresses': assigned,
        'attributes': {
            'link_type': link_type,
            'connects_to_device': connects_to_device,
            'connects_to_iface': connects_to_iface,
        }
    }
    try:
        if not iface:
            logger.info("Creating iface: {}".format(data))
            iface = client.sites(site_id).interfaces.post(data)
        else:
            logger.info("Updating iface: {}".format(iface))
            iface = client.sites(site_id).interfaces(iface[0]['id']).put(data)

    except HttpClientError as e:
        logger.error(e)
        logger.error(e.response.json())
        sys.exit(-1)
    logger.info(iface)
    return iface


@task
def loopbacks(ctx, site, filename="data/services.yml", debug=False):
    """Read service definition for loopbacks service and add data to the backend."""
    global logger
    logger = helpers.get_logger(debug)

    client = get_api_client()
    with open(filename, 'r') as f:
        service = yaml.load(f.read())['loopbacks']
        logger.debug(service)

    site_id = helpers.get_site_id(client, site)

    network = _create_networks(client, service['network_ranges'], 'loopback',
                               site_id)['loopbacks']

    ifaces = []
    for device in client.sites(site_id).devices.get():
        ifaces.append(_create_interface(client, site_id, device['id'], 'lo0', 'loopbacks',
                                        'loopback', 'loopback', network))
    return ifaces


@task
def ipfabric(ctx, site, filename="data/services.yml", debug=False):
    """Read service definition for ipfabric service and add data to the backend."""
    global logger
    logger = helpers.get_logger(debug)

    client = get_api_client()
    with open(filename, 'r') as f:
        service = yaml.load(f.read())['ipfabric']
        logger.debug(service)

    site_id = helpers.get_site_id(client, site)

    supernet = _create_networks(client, service['network_ranges'], 'ipfabric',
                                site_id)['fabric_links']

    for link in service['definition']['links']:
        network = None
        logger.debug("Processing {}".format(link))
        left_id = helpers.get_host_id(client, site_id, link['left_device'])
        right_id = helpers.get_host_id(client, site_id, link['right_device'])
        logger.debug("Found hosts {} and {}".format(left_id, right_id))

        left_interface = _create_interface(client, site_id, left_id, link['left_iface'],
                                           'fabric_links', link['right_device'],
                                           link['right_iface'])
        right_interface = _create_interface(client, site_id, right_id, link['right_iface'],
                                            'fabric_links', link['left_device'],
                                            link['left_iface'])
        if not left_interface['networks']:
            network = _create_subnet(client, site_id, supernet, 127)
            left_interface = _create_interface(client, site_id, left_id, link['left_iface'],
                                               'fabric_links', link['right_device'],
                                               link['right_iface'], network)
        if not right_interface['networks']:
            network = client.sites(site_id).networks(left_interface['networks'][0]).get()
            right_interface = _create_interface(client, site_id, right_id, link['right_iface'],
                                                'fabric_links', link['left_device'],
                                                link['left_iface'], network)

    return network
