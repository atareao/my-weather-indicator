#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# ipaddress.py
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
import dbus
import sys
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
        lambda _obj: dict(zip(map(convert, dbus_obj.keys()),
                              map(convert, dbus_obj.values())
                              )
                          ),
        (dbus.Dictionary, )
    )

    for conv in (pyint, pybool, pyfloat, pylist, pytuple, pystr, pydict):
        if any(map(_isinstance, conv.dbustypes)):
            return conv.pytype(dbus_obj)
    else:
        return dbus_obj


def get_current_location2():
    '''Gets the current location from geolocation via IP (only method
       currently supported)'''
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
    # url = 'http://checkip.dyndns.com/'
    url = 'http://whatismyip.org'
    ans = comun.read_from_url(url)
    # print(ans)
    return re.compile(r'(\d+\.\d+\.\d+\.\d+)').search(ans).group(1)


def get_current_location():
    url = 'http://geoip.nekudo.com/api/'
    print(url)
    ans = json.loads(comun.read_from_url(url))
    return ans['location']['latitude'], ans['location']['longitude']


def get_address_from_ip():
    lat, lon = get_current_location()
    ans = get_inv_direction(lat, lon)
    return ans


if __name__ == "__main__":
    import requests
    #r = requests.get("https://stackoverflow.com")

    #print(get_ip())
    print(get_current_location2())
    #print(get_current_location())
    # print(get_address_from_ip())
