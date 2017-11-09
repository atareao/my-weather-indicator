#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# geolocation.py
#
# Copyright (C) 2017 Lorenzo Carbonell Cerezo
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        print(url)
        response = requests.get(url, verify=False)
        print(response)
        if response.status_code == 200:
            position = response.json()
            print(position)
            return (position['latitude'],
                    position['longitude'],
                    position['city'])
    return None


if __name__ == '__main__':
    ip = get_external_ip()
    if ip is not None:
        ll = get_latitude_longitude_city(ip)
        if ll is not None:
            print(ll)
    exit(0)
