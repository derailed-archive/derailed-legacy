"""
Copyright (C) 2021-2023 Derailed.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
