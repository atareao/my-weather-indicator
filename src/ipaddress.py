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

import dbus
import comun
import re
import json
from functools import partial
from collections import namedtuple
from geocodeapi import get_inv_direction


def convert(dbus_obj):
    """Converts dbus_obj from dbus type to python type.
    :param dbus_obj: dbus object.
    :returns: dbus_obj in python type.
    """
    _isinstance = partial(isinstance, dbus_obj)
    ConvertType = namedtuple('ConvertType', 'pytype dbustypes')

    pyint = ConvertType(int, (dbus.Byte, dbus.Int16, dbus.Int32, dbus.Int64,
                              dbus.UInt16, dbus.UInt32, dbus.UInt64))
    pybool = ConvertType(bool, (dbus.Boolean, ))
    pyfloat = ConvertType(float, (dbus.Double, ))
    pylist = ConvertType(lambda _obj: list(map(convert, dbus_obj)),
                         (dbus.Array, ))
    pytuple = ConvertType(lambda _obj: tuple(map(convert, dbus_obj)),
                          (dbus.Struct, ))
    types_str = (dbus.ObjectPath, dbus.Signature, dbus.String)
    pystr = ConvertType(str, types_str)

    pydict = ConvertType(
        lambda _obj: dict(list(zip(list(map(convert, dbus_obj.keys())),
                                   list(map(convert, dbus_obj.values()))
                                   ))
                          ),
        (dbus.Dictionary, )
    )

    for conv in (pyint, pybool, pyfloat, pylist, pytuple, pystr, pydict):
        if any(map(_isinstance, conv.dbustypes)):
            return conv.pytype(dbus_obj)
    else:
        return dbus_obj


def get_current_location():
    latitude, longitude = get_current_location_option1()
    if latitude == 0 and longitude == 0:
        latitude, longitude = get_current_location_option2()
    return latitude, longitude


def get_current_location_option1():
    '''Gets the current location from geolocation via IP (only method
       currently supported)
    '''
    latitude = 0
    longitude = 0
    bus = dbus.SessionBus()

    # For now we default to the UbuntuGeoIP provider and we fall back to
    # Hostip. We should probably be cleverer about provider detection, but
    # this solution works for now and does not rely solely on UbuntuGeoIP,
    # which means qreator can run on other distros
    try:
        geoclue = bus.get_object(
            'org.freedesktop.Geoclue.Providers.UbuntuGeoIP',
            '/org/freedesktop/Geoclue/Providers/UbuntuGeoIP')
        position_info = geoclue.GetPosition(
            dbus_interface='org.freedesktop.Geoclue.Position')
        latitude = convert(position_info[2])
        longitude = convert(position_info[3])
    except dbus.exceptions.DBusException as e:
        print('Error 1', e)
        try:
            geoclue = bus.get_object(
                'org.freedesktop.Geoclue.Providers.Hostip',
                '/org/freedesktop/Geoclue/Providers/Hostip')
            position_info = geoclue.GetPosition(
                dbus_interface='org.freedesktop.Geoclue.Position')
            latitude = convert(position_info[2])
            longitude = convert(position_info[3])
        except dbus.exceptions.DBusException as e:
            print('Error 2', e)
    return latitude, longitude


def get_ip():
    url = 'http://whatismyip.org'
    ans = comun.read_from_url(url)
    # print(ans)
    return re.compile(r'(\d+\.\d+\.\d+\.\d+)').search(ans).group(1)


def get_current_location_option2():
    try:
        url = 'http://ip-api.com/json'
        ans = json.loads(comun.read_from_url(url))
        return ans['lat'], ans['lon']
    except Exception as e:
        print(e)
    return 0, 0


def get_address_from_ip():
    lat, lon = get_current_location()
    ans = get_inv_direction(lat, lon)
    return ans


if __name__ == "__main__":
    # import requests
    # r = requests.get("https://stackoverflow.com")

    print(get_current_location_option2())
    print('======')
    print(get_current_location())
    # print(get_address_from_ip())
