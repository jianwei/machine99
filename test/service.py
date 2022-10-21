#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from common.unix_socket import unix_socket

u = unix_socket(True)
u.server()