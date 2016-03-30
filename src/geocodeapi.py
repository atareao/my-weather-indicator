#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# A library for access to geocode for address
#
# Copyright (C) 2011 Lorenzo Carbonell
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
import sys
import json
from comun import read_from_url
import locale
import datetime
import pytz

locale.setlocale(locale.LC_MESSAGES, '')
LANG = locale.getlocale(locale.LC_MESSAGES)[0]

URLDIR_YAHOO = 'http://query.yahooapis.com/v1/public/yql?q=\
                select * from geo.placefinder where text="%s" and gflags="R"\
                and locale="%s"&format=json'
URLDIR_YAHOO2 = 'http://gws2.maps.yahoo.com/findlocation?pf=1&locale=%s\
                 &offset=15&flags=&q=%s&gflags=R&start=0&count=10&format=json'
URLINV_YAHOO = 'http://query.yahooapis.com/v1/public/yql?q=\
                select * from geo.placefinder where text="%s,%s" and\
                gflags="R" and locale="%s"&format=json'
URLINV_YAHOO2 = 'http://gws2.maps.yahoo.com/findlocation?pf=1&locale=%s\
&offset=15&flags=&q=%s,%s&gflags=R&start=0&count=10&format=json'


def s2f(cadena):
    try:
        value = float(cadena)
    except:
        value = 0.0
    return value


def fromjson2direction(json_string):
    direction = get_default_values()
    if 'city' in json_string.keys() and json_string['city']:
        direction['city'] = json_string['city']
    if 'state' in json_string.keys() and json_string['state']:
        direction['state'] = json_string['state']
    if 'country' in json_string.keys() and json_string['country']:
        direction['country'] = json_string['country']
    if 'latitude' in json_string.keys() and json_string['latitude']:
        direction['lat'] = s2f(json_string['latitude'])
    if 'longitude' in json_string.keys() and json_string['longitude']:
        direction['lng'] = s2f(json_string['longitude'])
    if 'woeid' in json_string.keys() and json_string['woeid']:
        direction['woeid'] = json_string['woeid']
    direction['search_string'] = ''
    if len(direction['city']):
        direction['search_string'] += direction['city']+','
    if len(direction['state']):
        direction['search_string'] += direction['state']+','
    if len(direction['country']):
        direction['search_string'] += direction['country']
    if direction['search_string'].endswith(','):
        direction['search_string'] = direction['search_string'][:-1]
    if s2f(direction['woeid']) == 0.0:
        direction = get_direction(direction['search_string'])
    return direction


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


def get_timezoneId(lat, lon):
    print('****** Requesting timezone identificacion')
    try:
        response = read_from_url('http://api.geonames.org/timezoneJSON?lat=\
                                 %s&lng=%s&username=atareao'
                                 % (lat, lon)).decode()
        json_response = json.loads(response)
        if json_response and 'timezoneId' in json_response.keys():
            return json_response['timezoneId']
    except Exception as e:
        print('Error requesting timezone identification: %s' % (str(e)))
    return 'Europe/London'


def get_rawOffset(timezoneId):
    print('****** Calculating rawOffset')
    if timezoneId is not None:
        try:
            timezone = pytz.timezone(timezoneId)
            timeinzone = timezone.localize(datetime.datetime.now())
            nowdt = timeinzone.strftime('%z')
            h = s2f(nowdt)
            m = (h - int(h))/60.0
            h = int(h/100.0)+m
            return h
        except Exception as e:
            print('Error calculating rawOffset: %s' % (str(e)))
    return 0.0


def get_inv_direction(lat, lon):
    directions = get_inv_directions(lat, lon)
    if len(directions) > 0:
        return directions[0]
    return None


def get_directions(search_string):
    directions = []
    try:
        url = URLDIR_YAHOO2 % (LANG, search_string)
        print('Searching url: %s' % (url))
        yahooResponse = read_from_url(url)
        if sys.version_info[0] == 3:
            jsonResponse = json.loads(yahooResponse.decode())
        else:
            jsonResponse = json.loads(yahooResponse)
        print(jsonResponse)
        if int(jsonResponse['Found']) > 1:
            for ans in jsonResponse['Result']:
                directions.append(fromjson2direction(ans))
        else:
            ans = jsonResponse['Result']
            directions.append(fromjson2direction(ans))
    except Exception as e:
        print('Error:', e)
    return directions


def get_inv_directions(lat, lon):
    directions = []
    try:
        url = URLINV_YAHOO2 % (LANG, lat, lon)
        print('Searching url: %s' % (url))
        yahooResponse = read_from_url(url)
        if sys.version_info[0] == 3:
            print(yahooResponse)
            jsonResponse = json.loads(yahooResponse.decode())
        else:
            jsonResponse = json.loads(yahooResponse)
        print(jsonResponse)
        if int(jsonResponse['Found']) > 1:
            for ans in jsonResponse['Result']:
                directions.append(fromjson2direction(ans))
        else:
            ans = jsonResponse['Result']
            directions.append(fromjson2direction(ans))
    except Exception as e:
        print('Error:', e)
    return directions


if __name__ == "__main__":
    print(get_inv_directions(40,0))
    '''
    print(get_timezoneId(28.63098,77.21725))
    print(get_rawOffset(get_timezoneId(28.63098,77.21725)))
    print('***********')
    print(get_timezoneId(34.2,58.3))
    print(get_rawOffset(get_timezoneId(-34.60851,-58.37349)))
    print(get_inv_directions(28.63098,77.21725))
    '''
    """
    direc3 = get_inv_direction(39.4697524227712, -0.377386808395386)
    print(direc3)
    print(get_directions('valencia'))
    """
    print(get_directions('alicante'))
