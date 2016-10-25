# tutorial-6-abstractions

https://www.dravetech.com/presos/network_automation_tutorial.html#/10

## Deploy site ACME


    inv site.create -n acme -d "Acme Corp."
    inv site.add_atribbutes -s acme -f data/acme/attributes.yml
    inv site.add_devices -s acme -f data/acme/devices.yml
    inv serivce.loopbacks -s acme -f data/acme/services.yml
    inv serivce.ipfabric -s acme -f data/acme/services.yml
      
    inv site.deploy -s acme
    inv site.deploy -s acme --commit
    inv site.verity -s acme

### Deploy site EVIL

    inv site.create -n evil -d "Evil Corp."
    inv site.add_atribbutes -s evil -f data/evil/attributes.yml
    inv site.add_devices -s evil -f data/evil/devices.yml
    inv serivce.loopbacks -s evil -f data/evil/services.yml
    inv serivce.ipfabric -s evil -f data/evil/services.yml
     
    inv site.deploy -s evil
    inv site.deploy -s evil --commit
    inv site.verity -s evil
