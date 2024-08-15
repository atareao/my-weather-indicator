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

import http.client
import socket
import time
import logging
import requests

logger = logging.getLogger(__name__)


def check_connectivity():
    """
    Check the connectivity to various sockets and URLs.

    Returns:
        bool: True if connectivity is successful, False otherwise.
    """
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
    """
    Check the connectivity with the given HTTP connection reference.

    Parameters:
    - reference (str): The HTTP connection reference to check.

    Returns:
    - bool: True if the connection is successful, False otherwise.
    """
    try:
        conn = http.client.HTTPConnection(reference)
        conn.close()
        logger.debug("OK. Internet connection. HTTPConnection: %s", reference)
        return True
    except Exception as ex:
        logger.error("No internet connection. HTTPConnection: %s. %s",
                     reference, ex)
        logger.error(ex)
    return False


def check_connectivity_with_socket(reference, port=80):
    """
    Check the connectivity with a socket.

    Args:
        reference (str): The reference to check the connectivity with.
        port (int, optional): The port to use for the connection. Defaults to
            80.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        conn = socket.create_connection((reference, port))
        conn.close()
        logger.debug("OK. Internet connection. Socket: %s", reference)
        return True
    except Exception as ex:
        logger.error("No internet connection. Socket: %s. %s", reference, ex)
    return False


def check_connectivity_with_reference(reference, timeout=2):
    """
    Check the connectivity with a reference URL.

    Args:
        reference (str): The URL to check the connectivity with.
        timeout (int, optional): The timeout value in seconds. Defaults to 2.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        requests.get(reference, timeout=timeout, verify=False)
        logger.debug("OK. Internet connection. Url: %s", reference)
        return True
    except Exception as ex:
        logger.error("No internet connection. Url: %s. %s", reference, ex)
        logger.error(ex)
    return False


if __name__ == '__main__':
    atime = time.time()
    logger.debug(check_connectivity(), time.time() - atime)
