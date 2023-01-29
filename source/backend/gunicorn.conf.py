"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
"""
import asyncio
import multiprocessing

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

wsgi_app = 'derailed.app:app'
loglevel = 'info'
proxy_allow_ips = '*'
bind = ['0.0.0.0:8080']
backlog = 1024
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = 'uvicorn.workers.UvicornWorker'
