In this tutorial we are just going to see we can connect to the devices via their respective APIs, retrieve information and perform simple changes.

Requirements
------------

    pip install -r requirements.txt

Getting information
===================

JunOS
-----

    from jnpr.junos import Device
    junos = Device(host='127.0.0.1', user='vagrant', port=12203)
    junos.open()
    junos_facts = junos.facts
    print(junos_facts)
    junos.close()

EOS
---

    import pyeapi
    connection = pyeapi.client.connect(
        transport='https',
        host='127.0.0.1',
        username='vagrant',
        password='vagrant',
        port=12443,
    )
    eos = pyeapi.client.Node(connection)
    eos_facts = eos.run_commands(['show version'])
    print(eos_facts)

Doing small changes
===================

JunOS
-----

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
    



EOS
---

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
