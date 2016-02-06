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

import sys
import json
import requests
from geocodeapi import get_inv_direction

def s2f(cadena):
	try:
		value = float(cadena)
	except:
		value = 0.0
	return value

def get_ip():
	try:
		r = requests.request('GET','http://www.telize.com/ip')
		r.raise_for_status()
		if r.status_code == 200:
			return r.text
	except Exception as e:
		print(e)
	return None	

def get_current_location():
	try:
		r = requests.request('GET','http://www.telize.com/geoip')
		r.raise_for_status()
		if r.status_code == 200:
			ans = r.json()
			latitude = s2f(ans['latitude'])
			longitude = s2f(ans['longitude'])
			return latitude,longitude
	except Exception as e:
		print(e)
	return 0.0,0.0
	
def get_address_from_ip2():
	lat,lon = get_current_location()
	return get_inv_direction(lat,lon)['search_string']

def get_address_from_ip():
	try:
		r = requests.request('GET','http://www.telize.com/geoip')
		r.raise_for_status()
		if r.status_code == 200:
			ans = r.json()
			return ans['city']
	except Exception as e:
		print(e)
	return ''

if __name__ == "__main__":
	print(get_ip())
	print(get_current_location())
	print(get_address_from_ip())
	print(get_address_from_ip2())
