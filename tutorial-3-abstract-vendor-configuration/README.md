In this tutorial we are going to perform exactly the same tasks we did on the previous tutorial. However, this time we will use napalm.

Requirements
------------

    pip install -r requirements.txt

Getting information
===================

    ansible-playbook playbook_facts.yml



Doing small changes
===================

    ansible-playbook playbook_configure.yml


    ansible-playbook playbook_configure.yml -e commit_changes=1
