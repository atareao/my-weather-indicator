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

import utils as cf
import gi
try:
    gi.require_version('GeocodeGlib', '1.0')
except BaseException:
    print('Repository version required not present')
    exit(1)
from comun import read_json_from_url
from comun import internet_on
import locale
import datetime
import pytz
from gi.repository import GeocodeGlib

locale.setlocale(locale.LC_MESSAGES, '')
LANG = locale.getlocale(locale.LC_MESSAGES)[0].replace('_', '-')

URLINV_YAHOO2 = 'http://gws2.maps.yahoo.com/findlocation?pf=1&locale=%s\
&offset=15&flags=&q=%s,%s&gflags=R&start=0&count=10&format=json'


def get_default_values():
    direction = {}
    direction['city'] = ''
    direction['state'] = ''
    direction['country'] = ''
    direction['lat'] = 0.0
    direction['lng'] = 0.0
    direction['woeid'] = ''
    direction['search_string'] = ''
    return direction


def is_direction_in_directions(direction, directions):
    for adirection in directions:
        if direction['search_string'] == adirection['search_string']:
            return True
    return False


def get_direction(search_string):
    directions = get_directions(search_string)
    if len(directions) > 0:
        return directions[0]
    return None


def get_timezoneId(latitude, longitude):
    print('****** Requesting timezone identificacion')
    try:
        json_response = read_json_from_url(
            'http://api.geonames.org/timezoneJSON?lat=%s&lng=%s&\
username=atareao' % (latitude, longitude))
        if json_response and 'timezoneId' in json_response.keys():
            return json_response['timezoneId']
        raise Exception
    except Exception as e:
        print('Error requesting timezone identification: %s' % (str(e)))
        try:
            json_response = read_json_from_url(
                'http://api.timezonedb.com/v2/get-time-zone?\
key=02SRH5M6VFLC&format=json&by=position&lat=%s&lng=%s' % (latitude,
                                                           longitude))
            if json_response is not None and\
                    'status' in json_response.keys() and\
                    json_response['status'] == 'OK':
                return json_response['zoneName']
            raise Exception
        except Exception as e:
            print('Error requesting timezone identification: %s' % (str(e)))
    return None


def get_rawOffset(timezoneId):
    print('****** Calculating rawOffset')
    if timezoneId is not None:
        try:
            timezone = pytz.timezone(timezoneId)
            timeinzone = timezone.localize(datetime.datetime.now())
            nowdelta = timeinzone.utcoffset()
            h = nowdelta.total_seconds() / 3600
            return h
        except Exception as e:
            print('Error calculating rawOffset: %s' % (str(e)))
    return 0.0


def get_woeid(lat, lon):
    print('******* Adquiring woeids *******')
    tries = 3
    while(tries > 0 and internet_on()):
        try:
            url = URLINV_YAHOO2 % (LANG, lat, lon)
            jsonResponse = read_json_from_url(url)
            if int(jsonResponse['Found']) > 1:
                woeid = jsonResponse['Result'][0]['woeid']
            else:
                woeid = jsonResponse['Result']['woeid']
            return woeid
        except Exception as e:
            print('******* Error adquiring inv directions *******')
            print('Error:', e)
        tries -= 1
    return None


def get_inv_direction(lat, lon):
    print('******* Adquiring inv direction *******')
    location = GeocodeGlib.Location.new(cf.s2f(lat), cf.s2f(lon), 1000)
    reverse = GeocodeGlib.Reverse.new_for_location(location)
    aplace = reverse.resolve()
    direction = {}
    direction['city'] = aplace.get_town()
    direction['state'] = aplace.get_state()
    direction['country'] = aplace.get_country()
    direction['lat'] = aplace.get_location().get_latitude()
    direction['lng'] = aplace.get_location().get_longitude()
    direction['woeid'] = None
    direction['search_string'] = aplace.get_name()
    return direction


def get_directions(search_string):
    forward = GeocodeGlib.Forward.new_for_string(search_string)
    places = forward.search()
    directions = []
    for aplace in places:
        direction = {}
        direction['city'] = aplace.get_town()
        direction['state'] = aplace.get_state()
        direction['country'] = aplace.get_country()
        direction['lat'] = aplace.get_location().get_latitude()
        direction['lng'] = aplace.get_location().get_longitude()
        direction['woeid'] = None
        direction['search_string'] = aplace.get_name()
        directions.append(direction)
    return directions


def get_inv_directions(lat, lon):
    print('******* Adquiring inv directions *******')
    location = GeocodeGlib.Location.new(lat, lon, 2000)
    reverse = GeocodeGlib.Reverse.new_for_location(location)
    aplace = reverse.resolve()
    directions = []
    direction = {}
    direction['city'] = aplace.get_town()
    direction['state'] = aplace.get_state()
    direction['country'] = aplace.get_country()
    direction['lat'] = aplace.get_location().get_latitude()
    direction['lng'] = aplace.get_location().get_longitude()
    direction['woeid'] = None
    direction['search_string'] = aplace.get_name()
    directions.append(direction)
    directions = get_directions(aplace.get_name())
    return directions


if __name__ == "__main__":
    '''
    print(get_inv_direction(40, 0))
    print('************************************************')
    print(get_direction('Silla'))
    print('************************************************')
    print(get_woeid(40, 0))
    print(get_inv_direction(39.3667, -0.4167))
    print(get_inv_direction(39.4, -0.4))
    '''
    print(get_timezoneId(40, 0))
    print(get_directions('Silla'))
