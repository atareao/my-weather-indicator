#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A library for access to check connectivity
# Copyright (C) 2011-2017 Lorenzo Carbonell
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

import http.client
import requests
import socket
import time


def check_connectivity():
    sockets = ['www.google.com',
               '216.58.192.142',
               'www.baidu.com']
    for asocket in sockets:
        if check_connectivity_with_httpconnection(asocket):
            return True
    for asocket in sockets:
        if check_connectivity_with_socket(asocket):
            return True
    urls = ['https://www.google.com',
            'http://www.google.com',
            'http://216.58.192.142',
            'http://www.baidu.com']
    for url in urls:
        if check_connectivity_with_reference(url):
            return True
    return False


def check_connectivity_with_httpconnection(reference):
    try:
        conn = http.client.HTTPConnection(reference)
        conn.close()
        print('OK. Internet connection. HTTPConnection: {0}'.format(reference))
        return True
    except Exception as ex:
        print('NO internet connection. HTTPConnection: {0}'.format(reference))
        print('Error:', ex)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    return False


def check_connectivity_with_socket(reference, port=80):
    try:
        conn = socket.create_connection((reference, port))
        conn.close()
        print('OK. Internet connection. Socket: {0}'.format(reference))
        return True
    except Exception as ex:
        print('NO internet connection. Socket: {0}'.format(reference))
        print('Error:', ex)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    return False


def check_connectivity_with_reference(reference, timeout=2):
    try:
        requests.get(reference, timeout=timeout, verify=False)
        print('OK. Internet connection. Url: {0}'.format(reference))
        return True
    except Exception as ex:
        print('NO internet connection. Url: {0}'.format(reference))
        print('Error:', ex)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    return False


if __name__ == '__main__':
    atime = time.time()
    print(check_connectivity(), time.time() - atime)
    '''
    urls = ['https://www.google.com',
            'http://www.google.com',
            'http://216.58.192.142',
            'http://www.baidu.com']
    sockets = ['www.google.com',
               '216.58.192.142',
               'www.baidu.com']
    print('======== SOCKET ========')
    for index, asocket in enumerate(sockets):
        atime = time.time()
        print(index, check_connectivity_with_httpconnection(asocket), asocket,
              time.time() - atime)
    print('======== SOCKET ========')
    for index, asocket in enumerate(sockets):
        atime = time.time()
        print(index, check_connectivity_with_socket(asocket), asocket,
              time.time() - atime)
    print('======== URLS ========')
    for index, url in enumerate(urls):
        atime = time.time()
        print(index, check_connectivity_with_reference(url), url,
              time.time() - atime)
    '''