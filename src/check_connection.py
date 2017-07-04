#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A library for access to geocode for address
#
# Copyright (C) 2011-2016 Lorenzo Carbonell
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
import urllib.request
import urllib.parse
import socket
import time
import http.client


def check_connectivity1(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False


def check_connectivity2(reference, timeout=5):
    try:
        requests.get(reference, timeout=timeout, verify=False)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


def check_connectivity3(host="8.8.8.8", port=53):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(1)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print('No internet connection available.')
        print('^^^^^', ex, '^^^^^')
    return False


def check_connectivity4():
    conn = http.client.HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False


def check_connectivity5():
    conn_url = 'https://www.google.com/'
    try:
        data = urllib.request.urlopen(conn_url, timeout=5)
    except Exception as e:
        return False
    try:
        host = data.fp._sock.fp._sock.getpeername()
    except AttributeError:  # Python 3
        host = data.fp.raw._sock.getpeername()

    # Ensure conn_url is an IPv4 address otherwise future queries will fail
    conn_url = 'http://' + (
        host[0] if len(host) == 2 else socket.gethostbyname(
                urllib.parse.urlparse(data.geturl()).hostname))
    return True


if __name__ == '__main__':
    TESTURL = 'https://www.google.com'
    atime = time.time()
    #print(1, check_connectivity1(TESTURL), time.time() - atime)
    atime = time.time()
    print(2, check_connectivity2(TESTURL), time.time() - atime)
    atime = time.time()
    print(3, check_connectivity3(), time.time() - atime)
    atime = time.time()
    print(4, check_connectivity4(), time.time() - atime)
    atime = time.time()
    print(5, check_connectivity5(), time.time() - atime)
