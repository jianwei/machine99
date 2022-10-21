#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,json
sys.path.append("..")
from common.unix_socket import unix_socket

u = unix_socket()
message = json.dumps({"a":1})
u.send_message(message)