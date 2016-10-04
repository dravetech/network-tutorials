* [Goals](#goals)
* [Instructions](#instructions)
	* [Requirements](#requirements)
	* [Getting information](#getting-information)
		* [JunOS](#junos)
		* [EOS](#eos)
	* [Doing small changes](#doing-small-changes)
		* [JunOS](#junos-1)
		* [EOS](#eos-1)
* [Summary](#summary)

# Goals

In this tutorial we are going to:

1. connect to the devices in via their respective APIs
2. retrieve information from the devices such as the serial number, model, etc.
3. perform a simple change on the device; change the hostname.

# Instructions

## Getting information

### JunOS

    from jnpr.junos import Device
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    junos = Device(host='127.0.0.1', user='vagrant', port=12203)
    junos.open()
    junos_facts = junos.facts
    pp.pprint(junos_facts)
    junos.close()

### EOS

    import pyeapi
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    connection = pyeapi.client.connect(transport='https', host='127.0.0.1', username='vagrant', password='vagrant', port=12443,)
    eos = pyeapi.client.Node(connection)
    eos_facts = eos.run_commands(['show version'])
    pp.pprint(eos_facts)

## Doing small changes

### JunOS

    from jnpr.junos import Device
    from jnpr.junos.utils.config import Config

    junos = Device(host='127.0.0.1', user='vagrant', port=12203)
    junos.open()

    print(junos.facts['hostname'])
    junos.bind(cu=Config)
    junos.cu.lock()
    junos.cu.load("system {host-name new-hostname;}", format="text", merge=True)
    junos.cu.commit()
    junos.cu.unlock()
    junos.facts_refresh()
    print(junos.facts['hostname'])
    junos.close()
    



### EOS

    import pyeapi
    connection = pyeapi.client.connect(
        transport='https',
        host='127.0.0.1',
        username='vagrant',
        password='vagrant',
        port=12443,
    )
    eos = pyeapi.client.Node(connection)
    print(eos.run_commands(['show hostname'])[0]['hostname'])
    eos.run_commands(['configure', 'hostname a-new-hostname'])
    print(eos.run_commands(['show hostname'])[0]['hostname'])

# Summary
