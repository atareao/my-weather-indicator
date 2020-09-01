#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
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

import requests


def get_external_ip():
    response = requests.get('https://api.ipify.org', verify=False)
    if response.status_code == 200:
        return response.text
    return None


def get_latitude_longitude_city(ip=None):
    if ip is None:
        ip = get_external_ip()
    print('ip', ip)
    if ip is not None:
        url = 'https://freegeoip.net/json/{0}'.format(ip)
        url = 'http://ip-api.com/json/{0}'.format(ip)
        print(url)
        response = requests.get(url, verify=False)
        print(response)
        if response.status_code == 200:
            position = response.json()
            print(position)
            return (position['lat'],
                    position['lon'],
                    position['city'])
    return None


if __name__ == '__main__':
    ip = get_external_ip()
    if ip is not None:
        ll = get_latitude_longitude_city(ip)
        if ll is not None:
            print(ll)
    exit(0)
