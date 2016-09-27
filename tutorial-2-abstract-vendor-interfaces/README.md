In this tutorial we are going to perform exactly the same tasks we did on the previous tutorial. However, this time we will use napalm.

Requirements
------------

    pip install -r requirements.txt

Getting information
===================

from napalm_base import get_network_driver
junos_driver =  get_network_driver('junos')
eos_driver =  get_network_driver('eos')

junos_configuration = {
    'hostname': '127.0.0.1',
    'username': 'vagrant',
    'password': '', 
    'optional_args': {'port': 12203}
}

eos_configuration = {
    'hostname': '127.0.0.1',
    'username': 'vagrant',
    'password': 'vagrant', 
    'optional_args': {'port': 12443}
}

def extract_hostname(device):
    print(device.get_facts()['hostname'])
    

with junos_driver(**junos_configuration) as junos:
    extract_hostname(junos)


with eos_driver(**eos_configuration) as eos:
    extract_hostname(eos)




Doing small changes
===================

from napalm_base import get_network_driver
junos_driver =  get_network_driver('junos')
eos_driver =  get_network_driver('eos')

junos_configuration = {
    'hostname': '127.0.0.1',
    'username': 'vagrant',
    'password': '', 
    'optional_args': {'port': 12203}
}

eos_configuration = {
    'hostname': '127.0.0.1',
    'username': 'vagrant',
    'password': 'vagrant', 
    'optional_args': {'port': 12443}
}

def change_configuration(device, configuration):
    device.load_merge_candidate(config=configuration)
    print(device.compare_config())
    device.commit_config()


with junos_driver(**junos_configuration) as junos:
    change_configuration(junos, "system {host-name yet-another-hostname;}")


with eos_driver(**eos_configuration) as eos:
    change_configuration(eos, 'hostname yet-another-hostname')
