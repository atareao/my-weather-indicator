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

import requests
import datetime
import pytz
from comun import LANG
import logging
from urllib.parse import quote


logger = logging.getLogger(__name__)

BASE_URI = "https://geocoding-api.open-meteo.com"
TZ_BASE_URI = "https://api.wheretheiss.at"
GEO_BASE_URI = "https://api.bigdatacloud.net"


def is_direction_in_directions(direction, directions):
    for adirection in directions:
        if direction['search_string'] == adirection['search_string']:
            return True
    return False


def get_external_ip():
    response = requests.get('https://api.ipify.org', verify=False)
    if response.status_code == 200:
        return response.text
    return None


def get_direction(search_string):
    directions = get_directions(search_string)
    if len(directions) > 0:
        return directions[0]
    return None


def get_latitude_longitude_city(ip=None):
    if ip is None:
        ip = get_external_ip()
    if ip is not None:
        url = f"http://ip-api.com/json/{ip}?lang={LANG}"
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            position = response.json()
            logger.debug(position)
            return position
    return None


def get_inv_direction(latitude, longitude):
    url = (f"{GEO_BASE_URI}/data/reverse-geocode-client?latitude={latitude}"
           f"&longitude={longitude}&localityLanguage={LANG}")
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data
    except Exception as exception:
        logger.error(exception)
    return None


def get_timezoneId(latitude, longitude):
    url = f"{TZ_BASE_URI}/v1/coordinates/{latitude},{longitude}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data["timezone_id"]
        elif "error" in data.keys():
            raise Exception(f"Error: {data['error']}")
        raise Exception("Cant")
    except Exception as exception:
        logger.error(exception)
    return None


def get_rawOffset(timezoneId):
    logger.debug('****** Calculating rawOffset')
    logger.debug(f"Timezone: {timezoneId}")
    if timezoneId:
        try:
            timezone = pytz.timezone(timezoneId)
            logger.debug(f"Timezone: {timezone}")
            timeinzone = timezone.localize(datetime.datetime.now())
            logger.debug(f"Time in zone: {timeinzone}")
            nowdelta = timeinzone.utcoffset()
            logger.debug(f"Delta: {nowdelta}")
            if nowdelta:
                return nowdelta.total_seconds() / 3600
        except Exception as e:
            logger.error('Error calculating rawOffset: %s' % (str(e)))
            logger.error(e)
    return 0.0


def get_directions(name):
    logger.debug("get_directions")
    search_string = quote(name)
    url = f"{BASE_URI}/v1/search?name={search_string}&language={LANG}"
    logger.debug(url)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            data = response.json()
            logger.debug(data)
            if "results" in data.keys():
                return data["results"]
        raise Exception("Cant find")
    except Exception as exception:
        logger.error(exception)
    return []


if __name__ == "__main__":
    timezone_id = get_timezoneId(0, 0)
    logger.debug(timezone_id)
    logger.debug(get_rawOffset(timezone_id))
