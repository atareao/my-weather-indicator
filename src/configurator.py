#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of my-weather-indicator
#
# Copyright (c) 2012 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import codecs
import os
import json
import comun
import logging

logger = logging.getLogger(__name__)


class Configuration(object):

    def __init__(self):
        self.params = comun.PARAMS
        self.read()

    def get(self, key):
        try:
            return self.params[key]
        except KeyError as e:
            logger.error(e)
            self.params[key] = comun.PARAMS[key]
            return self.params[key]

    def set(self, key, value):
        self.params[key] = value

    def reset(self):
        if os.path.exists(comun.CONFIG_FILE):
            os.remove(comun.CONFIG_FILE)
        self.params = comun.PARAMS
        self.save()

    def set_defaults(self):
        self.params = comun.PARAMS
        self.save()

    def read(self):
        try:
            f = codecs.open(comun.CONFIG_FILE, 'r', 'utf-8')
        except IOError as e:
            logger.error(e)
            self.save()
            f = codecs.open(comun.CONFIG_FILE, 'r', 'utf-8')
        try:
            self.params = json.loads(f.read())
        except ValueError as e:
            logger.error(e)
            self.save()
        f.close()

    def save(self):
        if not os.path.exists(comun.CONFIG_APP_DIR):
            os.makedirs(comun.CONFIG_APP_DIR)
        f = codecs.open(comun.CONFIG_FILE, 'w', 'utf-8')
        f.write(json.dumps(self.params, indent=4, sort_keys=True))
        f.close()
