# tutorial-5-data-driven-configuration_with_backend

https://www.dravetech.com/presos/network_automation_tutorial.html#/9

## Backend

### Start NSOT

    cd labs/nsot
    vagrant up
    vagrant ssh
    nsot-server start
    (input email/password)

Go to http://localhost:8990/users/1 and get "Secret key".

### Configure NSOT

    # nsot sites list
    /Users/dbarroso/.pynsotrc not found; would you like to create it? [Y/n]:
    Please enter url: http://localhost:8990/api
    Please choose auth_method [auth_token, auth_header]: auth_token
    Please enter secret_key: bVg27yn1i9MkmRa14fJFAtsfMRZjuYtG1H5X4ZVaCgU=
    Please enter email: asd@asd.com
    Please enter default_site (optional):
    Please enter api_version (optional):
    No site found matching args: offset=None, limit=None, id=None, name=None!

### Adding data to the backend

    ./create_data.sh

## Doing small changes

    ansible-playbook playbook_configure.yml -C

    ansible-playbook playbook_configure.yml 


## Getting information

    ansible-playbook playbook_verify.yml

    Note: Highlight differences between previous tutorial and this one
