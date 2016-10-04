# -*- coding: utf-8 -*-
"""Tasks for tutorial-6-abstractions."""

import invoke

from . import tasks_db, tasks_site, tasks_service

ns = invoke.Collection()
ns.add_collection(invoke.Collection.from_module(tasks_db), 'db')
ns.add_collection(invoke.Collection.from_module(tasks_site), 'site')
ns.add_collection(invoke.Collection.from_module(tasks_service), 'serivce')
