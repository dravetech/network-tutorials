In this tutorial we are going to perform exactly the same tasks we did on the previous tutorial. However, this time we will use napalm.

Requirements
------------

    pip install -r requirements.txt

Backend
=======

Start NSOT
----------

    cd labs/nsot
    vagrant up
    vagrant ssh
    nsot-server start
    (input emoail/password)

Go to http://localhost:8990/users/1 and get "Secret key".

Configure NSOT
-------------

    # nsot sites list
    /Users/dbarroso/.pynsotrc not found; would you like to create it? [Y/n]:
    Please enter url: http://localhost:8990/api
    Please choose auth_method [auth_token, auth_header]: auth_token
    Please enter secret_key: bVg27yn1i9MkmRa14fJFAtsfMRZjuYtG1H5X4ZVaCgU=
    Please enter email: asd@asd.com
    Please enter default_site (optional):
    Please enter api_version (optional):
    No site found matching args: offset=None, limit=None, id=None, name=None!

Adding data to the backend
-------------------------

nsot sites add --name my_demo_site

nsot attributes add --site-id 1 --resource-name device --name os
nsot attributes add --site-id 1 --resource-name device --name host
nsot attributes add --site-id 1 --resource-name device --name user
nsot attributes add --site-id 1 --resource-name device --name password --allow-empty
nsot attributes add --site-id 1 --resource-name device --name port

nsot devices add --site-id 1 --hostname rtr00
nsot devices update --site-id 1 --id 1 -a os=eos -a host=127.0.0.1 -a user=vagrant -a password=vagrant -a port=12443
nsot devices add --site-id 1 --hostname rtr01
nsot devices update --site-id 1 --id 2 -a os=junos -a host=127.0.0.1 -a user=vagrant -a password="" -a port=12203


nsot attributes add --site-id 1 --resource-name device --name asn
nsot attributes add --site-id 1 --resource-name device --name router_id

nsot devices update --site-id 1 --id 1 -a asn=65001 -a router_id=10.1.1.1
nsot devices update --site-id 1 --id 2 -a asn=65002 -a router_id=10.1.1.2

nsot attributes add --site-id 1 --resource-name network --name type
nsot networks add --site-id 1 --cidr 2001:db8:b33f::/64 -a type=loopbacks

nsot attributes add --site-id 1 --resource-name interface --name link_type
nsot attributes add --site-id 1 --resource-name interface --name connects_to --allow-empty

nsot interfaces add --site-id 1 --device 1 --name lo0 --addresses 2001:db8:b33f::100/128 -a link_type=loopback
nsot interfaces add --site-id 1 --device 2 --name lo0 --addresses 2001:db8:b33f::101/128 -a link_type=loopback

nsot networks add --site-id 1 --cidr 2001:db8:caf3::/64 -a type=ptp
nsot networks add --site-id 1 --cidr 2001:db8:caf3::/127 -a type=ptp
nsot networks add --site-id 1 --cidr 2001:db8:caf3::2/127 -a type=ptp

nsot interfaces add --site-id 1 --device 1 --name et1 -a link_type=fabric -a connects_to=rtr01:ge-0/0/1 -c 2001:db8:caf3::
nsot interfaces add --site-id 1 --device 1 --name et2 -a link_type=fabric -a connects_to=rtr01:ge-0/0/2 -c 2001:db8:caf3::2

nsot interfaces add --site-id 1 --device 2 --name ge-0/0/1 -a link_type=fabric -a connects_to=rtr00:et1 -c 2001:db8:caf3::1
nsot interfaces add --site-id 1 --device 2 --name ge-0/0/2 -a link_type=fabric -a connects_to=rtr00:et2 -c 2001:db8:caf3::3


Getting information
===================

    ansible-playbook playbook_facts.yml



Doing small changes
===================

    ansible-playbook playbook_configure.yml


    ansible-playbook playbook_configure.yml -e commit_changes=1
