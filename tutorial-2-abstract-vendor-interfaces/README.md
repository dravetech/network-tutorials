# tutorial-2-abstract-vendor-interfaces

https://www.dravetech.com/presos/network_automation_tutorial.html#/6

## Getting information

    from napalm_base import get_network_driver
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

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
    
    with junos_driver(**junos_configuration) as junos:
        pp.pprint(junos.get_facts()) 
    
    with eos_driver(**eos_configuration) as eos:
        pp.pprint(eos.get_facts()) 




## Doing small changes

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
