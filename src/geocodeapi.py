#!/usr/bin/python3
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
#
#
#
import gi
try:
    gi.require_version('GeocodeGlib', '1.0')
except BaseException:
    print('Repository version required not present')
    exit(1)
import sys
import json
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


def s2f(word):
    try:
        value = float(word)
    except BaseException:
        value = 0.0
    return value


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
    location = GeocodeGlib.Location.new(s2f(lat), s2f(lon), 1000)
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
