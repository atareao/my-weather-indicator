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
import yql

locale.setlocale(locale.LC_MESSAGES, '')
LANG = locale.getlocale(locale.LC_MESSAGES)[0].replace('_','-')
API_KEY = 'dj0yJmk9djNkNk5hRUZNODFCJmQ9WVdrOWVEbFVXRWxITTJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZW\
NyZXQmeD1jMQ--'
SHARED_SECRET = '27dcb39434d1ee95b90e5f3a7e227d3992ecd573'

URLINV_YAHOO2 = 'http://gws2.maps.yahoo.com/findlocation?pf=1&locale=%s\
&offset=15&flags=&q=%s,%s&gflags=R&start=0&count=10&format=json'


def s2f(word):
    try:
        value = float(word)
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
            nowdelta = timeinzone.utcoffset()
            h = nowdelta.total_seconds() / 3600
            return h
        except Exception as e:
            print('Error calculating rawOffset: %s' % (str(e)))
    return 0.0


def get_inv_direction(lat, lon):
    directions = get_inv_directions(lat, lon)
    if len(directions) > 0:
        return directions[0]
    return None


def get_inv_directions2(lat, lon):
    y = yql.TwoLegged(API_KEY, SHARED_SECRET)
    query = 'select * from geo.places where text="%s,%s"' % (lat, lon)
    print(query)
    ans = y.execute(query)
    print(ans.results)


def get_directions(search_string):
    print('******* Adquiring directions yql*******')
    directions = []
    try:
        y = yql.TwoLegged(API_KEY, SHARED_SECRET)
        query = 'select * from geo.places where text="%s" and lang="%s"' %\
            (search_string, LANG)
        ans = y.execute(query)
        if ans is not None and ans.results is not None and 'place' in\
                ans.results.keys():
            for element in ans.results['place']:
                if element is not None:
                    direction = {}
                    if element['locality1'] is not None:
                        direction['city'] = element['locality1']['content']
                        direction['state'] = element['admin1']['content']
                        direction['country'] = element['country']['content']
                        direction['lat'] = s2f(element['centroid']['latitude'])
                        direction['lng'] =\
                            s2f(element['centroid']['longitude'])
                        direction['woeid'] = element['woeid']
                        direction['search_string'] =\
                            element['locality1']['content']
                        directions.append(direction)
    except Exception as e:
        print('yql', e)
    return directions


def get_inv_directions(lat, lon):
    print('******* Adquiring inv directions *******')
    directions = []
    try:
        url = URLINV_YAHOO2 % (LANG, lat, lon)
        print(url)
        yahooResponse = read_from_url(url)
        jsonResponse = json.loads(yahooResponse.decode())
        if int(jsonResponse['Found']) > 1:
            for ans in jsonResponse['Result']:
                directions.append(fromjson2direction(ans))
        else:
            ans = jsonResponse['Result']
            directions.append(fromjson2direction(ans))
    except Exception as e:
        print('******* Error adquiring inv directions *******')
        print('Error:', e)
    return directions


if __name__ == "__main__":
    print(get_inv_directions(40, 0))
    print('************************************************')
    print(get_directions('Silla'))
