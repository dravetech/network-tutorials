#!/usr/bin/env python
"""
nsot docstring.
"""
import json
import netaddr


from pynsot.client import get_api_client


def _build_resource_map(resource_list, alias='name'):
    return {r['id']: r[alias] for r in resource_list}


def _process_devices(devices, sites_map, result):
    for device in devices:
        result[sites_map[device['site_id']]]['hosts'].append(device['hostname'])
        result['_meta']['hostvars'][device['hostname']] = device['attributes']
        result['_meta']['hostvars'][device['hostname']]['interfaces'] = {}


def _resolve_cidr(address, networks):
    for network in networks:
        net = netaddr.IPNetwork(network)
        cidr = '{}/{}'.format(address, net.prefixlen)
        if address in net:
            return cidr


def _process_interfaces(interfaces, device_map, result):
    for interface in interfaces:
        ipv4 = []
        ipv6 = []
        for address in interface['addresses']:
            addr = netaddr.IPAddress(address.split('/')[0])
            cidr = _resolve_cidr(addr, interface['networks'])
            if addr.version == 4:
                ipv4.append(cidr)
            else:
                ipv6.append(cidr)
        interface['ipv4'] = ipv4
        interface['ipv6'] = ipv6
        result['_meta']['hostvars'][device_map[interface['device']]]['interfaces'][interface['name']] = interface  # noqa


def main():
    """Main process."""
    api = get_api_client()
    sites = api.sites.get()
    sites_map = _build_resource_map(sites)

    devices = []
    for site in sites:
        devices += api.sites(site['id']).devices.get()
    devices_map = _build_resource_map(devices, 'hostname')

    interfaces = []
    for site in sites:
        interfaces += api.sites(site['id']).interfaces.get()

    result = {
        "_meta": {
            "hostvars": {}
        }
    }

    for _, site in sites_map.items():
        result[site] = {
            "hosts": [],
            "children": [],
            "vars": {}
        }
    _process_devices(devices, sites_map, result)
    _process_interfaces(interfaces, devices_map, result)

    return result


if __name__ == "__main__":
    print json.dumps(main())
