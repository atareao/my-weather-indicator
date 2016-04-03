#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# A library for accesssing to gunderground api
#
# Copyright (C) 2012-2014 Lorenzo Carbonell
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
import sys
from sun import Sun
from moon import Moon
from datetime import datetime
from datetime import timedelta
import geocodeapi
import locale
import math

from comun import _

CONDITIONS = {}
CONDITIONS['blowing sand'] = {
    'text': _('Blowing sand'),
    'image': 'mwig-windy.png',
    'image-night': 'mwig-windy.png',
    'icon-dark': 'mwid-windy.png',
    'icon-night-dark': 'mwid-windy.png',
    'icon-light': 'mwil-windy.png',
    'icon-night-light': 'mwil-windy.png'}
CONDITIONS['blizzard'] = {
    'text': _('Blizzard'),
    'image': 'mwig-windy.png',
    'image-night': 'mwig-windy.png',
    'icon-dark': 'mwid-windy.png',
    'icon-night-dark': 'mwid-windy.png',
    'icon-light': 'mwil-windy.png',
    'icon-night-light': 'mwil-windy.png'}
CONDITIONS['blowing snow'] = {
    'text': _('Blowing snow'),
    'image': 'mwig-snow.png',
    'image-night': 'mwig-snow.png',
    'icon-dark': 'mwid-snow.png',
    'icon-night-dark': 'mwid-snow.png',
    'icon-light': 'mwil-snow.png',
    'icon-night-light': 'mwil-snow.png'}
CONDITIONS['blowing widespread dust'] = {
    'text': _('Blowing widespread dust'),
    'image': 'mwig-windy.png', 'image-night': 'mwig-windy.png',
    'icon-dark': 'mwid-windy.png', 'icon-night-dark': 'mwid-windy.png',
    'icon-light': 'mwil-windy.png', 'icon-night-light': 'mwil-windy.png'}
CONDITIONS['chance of a thunderstorm'] = {
    'text': _('Chance of a thunderstorm'),
    'image': 'mwig-chance-of-thunderstorms.png',
    'image-night': 'mwig-chance-of-thunderstorms-night.png',
    'icon-dark': 'mwid-chance-of-thunderstorms.png',
    'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
    'icon-light': 'mwil-chance-of-thunderstorms.png',
    'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'}
CONDITIONS['chance of flurries'] = {
    'text': _('Chance of flurries'), 'image': 'mwig-chance-of-snow.png',
    'image-night': 'mwig-chance-of-snow-night.png',
    'icon-dark': 'mwid-chance-of-snow.png',
    'icon-night-dark': 'mwid-chance-of-snow-night.png',
    'icon-light': 'mwil-chance-of-snow.png',
    'icon-night-light': 'mwil-chance-of-snow-night.png'}
CONDITIONS['chance of rain'] = {
    'text': _('Chance of rain'),
    'image': 'mwig-chance-of-rain.png',
    'image-night': 'mwig-chance-of-rain-night.png',
    'icon-dark': 'mwid-chance-of-rain.png',
    'icon-night-dark': 'mwid-chance-of-rain-night.png',
    'icon-light': 'mwil-chance-of-rain.png',
    'icon-night-light': 'mwil-chance-of-rain-night.png'}
CONDITIONS['chance of showers'] = {
    'text': _('Chance of showers'),
    'image': 'mwig-chance-of-rain.png',
    'image-night': 'mwig-chance-of-rain-night.png',
    'icon-dark': 'mwid-chance-of-rain.png',
    'icon-night-dark': 'mwid-chance-of-rain-night.png',
    'icon-light': 'mwil-chance-of-rain.png',
    'icon-night-light': 'mwil-chance-of-rain-night.png'}
CONDITIONS['chance of snow'] = {'text': _('Chance of snow'), 'image': 'mwig-chance-of-snow.png', 'image-night': 'mwig-chance-of-snow-night.png', 'icon-dark': 'mwid-chance-of-snow.png', 'icon-night-dark': 'mwid-chance-of-snow-night.png', 'icon-light': 'mwil-chance-of-snow.png', 'icon-night-light': 'mwil-chance-of-snow-night.png'}
CONDITIONS['chance of storm'] = {'text': _('Chance of storm'), 'image': 'mwig-chance-of-thunderstorms.png', 'image-night': 'mwig-chance-of-thunderstorms-night.png', 'icon-dark': 'mwid-chance-of-thunderstorms.png', 'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png', 'icon-light': 'mwil-chance-of-thunderstorms.png', 'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'}
CONDITIONS['chance of thunderstorms'] = {'text': _('Chance of thunderstorms'), 'image': 'mwig-chance-of-thunderstorms.png', 'image-night': 'mwig-chance-of-thunderstorms-night.png', 'icon-dark': 'mwid-chance-of-thunderstorms.png', 'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png', 'icon-light': 'mwil-chance-of-thunderstorms.png', 'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'}
CONDITIONS['chance of tstorm'] = {'text': _('Chance of tstorm'), 'image': 'mwig-chance-of-thunderstorms.png', 'image-night': 'mwig-chance-of-thunderstorms-night.png', 'icon-dark': 'mwid-chance-of-thunderstorms.png', 'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png', 'icon-light': 'mwil-chance-of-thunderstorms.png', 'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'}
CONDITIONS['clear'] = {'text': _('Clear'), 'image': 'mwig-clear.png', 'image-night': 'mwig-clear-night.png', 'icon-dark': 'mwid-clear.png', 'icon-night-dark': 'mwid-clear-night.png', 'icon-light': 'mwil-clear.png', 'icon-night-light': 'mwil-clear-night.png'}
CONDITIONS['cloudy'] = {'text': _('Cloudy'), 'image': 'mwig-cloudy.png', 'image-night': 'mwig-cloudy.png', 'icon-dark': 'mwid-cloudy.png', 'icon-night-dark': 'mwid-cloudy.png', 'icon-light': 'mwil-cloudy.png', 'icon-night-light': 'mwil-cloudy.png'}
CONDITIONS['cold'] = {'text': _('Cold'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['drizzle'] = {'text': _('Drizzle'), 'image': 'mwig-light-rain.png', 'image-night': 'mwig-light-rain.png', 'icon-dark': 'mwid-light-rain.png', 'icon-night-dark': 'mwid-light-rain.png', 'icon-light': 'mwil-light-rain.png', 'icon-night-light': 'mwil-light-rain.png'}
CONDITIONS['drizzle rain'] = {'text': _('Drizzle rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['dust whirls'] = {'text': _('Dust whirls'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['dust'] = {'text': _('Dust'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['extreme rain'] = {'text': _('Extreme rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['fair'] = {'text': _('Fair'), 'image': 'mwig-clear.png', 'image-night': 'mwig-clear-night.png', 'icon-dark': 'mwid-clear.png', 'icon-night-dark': 'mwid-clear-night.png', 'icon-light': 'mwil-clear.png', 'icon-night-light': 'mwil-clear-night.png'}
CONDITIONS['flurries'] = {'text': _('Flurries'), 'image': 'mwig-flurries.png', 'image-night': 'mwig-flurries.png', 'icon-dark': 'mwid-flurries.png', 'icon-night-dark': 'mwid-flurries.png', 'icon-light': 'mwil-flurries.png', 'icon-night-light': 'mwil-flurries.png'}
CONDITIONS['fog patches'] = {'text': _('Fog patches'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['fog'] = {'text': _('Fog'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['foggy'] = {'text': _('Foggy'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['freezing drizzle'] = {'text': _('Freezing drizzle'), 'image': 'mwig-freezing-drizzle.png', 'image-night': 'mwig-freezing-drizzle.png', 'icon-dark': 'mwid-freezing-drizzle.png', 'icon-night-dark': 'mwid-freezing-drizzle.png', 'icon-light': 'mwil-freezing-drizzle.png', 'icon-night-light': 'mwil-freezing-drizzle.png'}
CONDITIONS['freezing drizzle'] = {'text': _('Freezing drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['freezing fog.png',] = {'text': _('Freezing fog'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['freezing fog'] = {'text': _('Freezing fog'), 'image': 'mwig-freezing-drizzle.png', 'image-night': 'mwig-freezing-drizzle.png', 'icon-dark': 'mwid-freezing-drizzle.png', 'icon-night-dark': 'mwid-freezing-drizzle.png', 'icon-light': 'mwil-freezing-drizzle.png', 'icon-night-light': 'mwil-freezing-drizzle.png'}
CONDITIONS['freezing rain'] = {'text': _('Freezing rain'), 'image': 'mwig-freezing-drizzle.png', 'image-night': 'mwig-freezing-drizzle.png', 'icon-dark': 'mwid-freezing-drizzle.png', 'icon-night-dark': 'mwid-freezing-drizzle.png', 'icon-light': 'mwil-freezing-drizzle.png', 'icon-night-light': 'mwil-freezing-drizzle.png'}
CONDITIONS['funnel cloud'] = {'text': _('Funnel cloud'), 'image': 'mwig-cloudy.png', 'image-night': 'mwig-cloudy.png', 'icon-dark': 'mwid-cloudy.png', 'icon-night-dark': 'mwid-cloudy.png', 'icon-light': 'mwil-cloudy.png', 'icon-night-light': 'mwil-cloudy.png'}
CONDITIONS['hail showers'] = {'text': _('Hail showers'), 'image': 'mwig-hail.png', 'image-night': 'mwig-hail.png', 'icon-dark': 'mwid-hail.png', 'icon-night-dark': 'mwid-hail.png', 'icon-light': 'mwil-hail.png', 'icon-night-light': 'mwil-hail.png'}
CONDITIONS['hail'] = {'text': _('Hail'), 'image': 'mwig-hail.png', 'image-night': 'mwig-hail.png', 'icon-dark': 'mwid-hail.png', 'icon-night-dark': 'mwid-hail.png', 'icon-light': 'mwil-hail.png', 'icon-night-light': 'mwil-hail.png'}
CONDITIONS['haze'] = {'text': _('Haze'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['heavy freezing drizzle'] = {'text': _('Heavy freezing drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy intensity drizzle'] = {'text': _('Heavy intensity drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy intensity drizzle rain'] = {'text': _('Heavy intensity drizzle rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy intensity rain'] = {'text': _('Heavy intensity rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy intensity shower rain'] = {'text': _('Heavy intensity shower rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy rain at times'] = {'text': _('Heavy rain at times'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy rain'] = {'text': _('Heavy rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['heavy snow'] = {'text': _('Heavy snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['heavy thunderstorm'] = {'text': _('Heavy thunderstorm'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['hot'] = {'text': _('Hot'), 'image': 'mwig-clear.png', 'image-night': 'mwig-clear-night.png', 'icon-dark': 'mwid-clear.png', 'icon-night-dark': 'mwid-clear-night.png', 'icon-light': 'mwil-clear.png', 'icon-night-light': 'mwil-clear-night.png'}
CONDITIONS['hurricane'] = {'text': _('Hurricane'), 'image': 'mwig-windy.png', 'image-night': 'mwig-windy.png', 'icon-dark': 'mwid-windy.png', 'icon-night-dark': 'mwid-windy.png', 'icon-light': 'mwil-windy.png', 'icon-night-light': 'mwil-windy.png'}
CONDITIONS['ice crystals'] = {'text': _('Ice crystals'), 'image': 'mwig-icy.png', 'image-night': 'mwig-icy.png', 'icon-dark': 'mwid-icy.png', 'icon-night-dark': 'mwid-icy.png', 'icon-light': 'mwil-icy.png', 'icon-night-light': 'mwil-icy.png'}
CONDITIONS['ice pellet showers'] = {'text': _('Ice pellet showers'), 'image': 'mwig-icy.png', 'image-night': 'mwig-icy.png', 'icon-dark': 'mwid-icy.png', 'icon-night-dark': 'mwid-icy.png', 'icon-light': 'mwil-icy.png', 'icon-night-light': 'mwil-icy.png'}
CONDITIONS['ice pellets.png',] = {'text': _('Ice pellets'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['ice pellets'] = {'text': _('Ice pellets'), 'image': 'mwig-icy.png', 'image-night': 'mwig-icy.png', 'icon-dark': 'mwid-icy.png', 'icon-night-dark': 'mwid-icy.png', 'icon-light': 'mwil-icy.png', 'icon-night-light': 'mwil-icy.png'}
CONDITIONS['icy'] = {'text': _('Icy'), 'image': 'mwig-icy.png', 'image-night': 'mwig-icy.png', 'icon-dark': 'mwid-icy.png', 'icon-night-dark': 'mwid-icy.png', 'icon-light': 'mwil-icy.png', 'icon-night-light': 'mwil-icy.png'}
CONDITIONS['intensity drizzle'] = {'text': _('Intensity drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['intensity drizzle rain'] = {'text': _('Intensity drizzle rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['intensity rain'] = {'text': _('Intensity rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['isolated showers'] = {'text': _('Isolated showers'), 'image': 'mwig-chance-of-rain.png', 'image-night': 'mwig-chance-of-rain-night.png', 'icon-dark': 'mwid-chance-of-rain.png', 'icon-night-dark': 'mwid-chance-of-rain-night.png', 'icon-light': 'mwil-chance-of-rain.png', 'icon-night-light': 'mwil-chance-of-rain-night.png'}
CONDITIONS['isolated thunderstorms'] = {'text': _('Isolated thunderstorms'), 'image': 'mwig-chance-of-thunderstorms.png', 'image-night': 'mwig-chance-of-thunderstorms-night.png', 'icon-dark': 'mwid-chance-of-thunderstorms.png', 'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png', 'icon-light': 'mwil-chance-of-thunderstorms.png', 'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'}
CONDITIONS['light drizzle'] = {'text': _('Light drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light freezing rain'] = {'text': _('Light freezing rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light intensity drizzle'] = {'text': _('Light intensity drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light intensity drizzle rain'] = {'text': _('Light intensity drizzle rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light intensity shower rain'] = {'text': _('Light intensity shower rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light rain shower'] = {'text': _('Light rain shower'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light rain'] = {'text': _('Light rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light showers of ice pellets.png',] = {'text': _('Light showers of ice pellets'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light sleet showers.png',] = {'text': _('Light sleet showers'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light sleet'] = {'text': _('Light sleet'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['light snow showers.png',] = {'text': _('Light snow showers'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['light snow'] = {'text': _('Light snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['light thunderstorm'] = {'text': _('Light thunderstorm'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['low drifting sand'] = {'text': _('Low drifting sand'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['low drifting snow'] = {'text': _('Low drifting snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['low drifting widespread dust'] = {'text': _('Low drifting widespread dust'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['mist'] = {'text': _('Mist'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['mixed rain and snow'] = {'text': _('Mixed rain and snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['mixed rain and sleet'] = {'text': _('Mixed rain and sleet'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['mixed snow and sleet'] = {'text': _('Mixed snow and sleet'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['moderate or heavy freezing rain'] = {'text': _('Moderate or heavy freezing rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate or heavy rain in area with thunder'] = {'text': _('Moderate or heavy rain in area with thunder'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['moderate or heavy rain shower'] = {'text': _('Moderate or heavy rain shower'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate or heavy showers of ice pellets'] = {'text': _('Moderate or heavy showers of ice pellets'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate or heavy sleet showers.png',] = {'text': _('Moderate or heavy sleet showers'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate or heavy sleet'] = {'text': _('Moderate or heavy sleet'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['moderate or heavy snow in area with thunder'] = {'text': _('Moderate or heavy snow in area with thunder'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['moderate or heavy snow showers'] = {'text': _('Moderate or heavy snow showers'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate rain at times'] = {'text': _('Moderate rain at times'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate rain'] = {'text': _('Moderate rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['moderate snow'] = {'text': _('Moderate snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['mostly cloudy'] = {'text': _('Mostly cloudy'), 'image': 'mwig-mostly-cloudy.png', 'image-night': 'mwig-mostly-cloudy-night.png', 'icon-dark': 'mwid-mostly-cloudy.png', 'icon-night-dark': 'mwid-mostly-cloudy-night.png', 'icon-light': 'mwil-mostly-cloudy.png', 'icon-night-light': 'mwil-mostly-cloudy-night.png'}
CONDITIONS['mostly sunny'] = {'text': _('Mostly sunny'), 'image': 'mwig-mostly-sunny.png', 'image-night': 'mwig-mostly-sunny-night.png', 'icon-dark': 'mwid-mostly-sunny.png', 'icon-night-dark': 'mwid-mostly-sunny-night.png', 'icon-light': 'mwil-mostly-sunny.png', 'icon-night-light': 'mwil-mostly-sunny-night.png'}
CONDITIONS['not available'] = {'text': _('Not available'), 'image': 'mwig-not-available.png', 'image-night': 'mwig-not-available-night.png', 'icon-dark': 'mwid-not-available.png', 'icon-night-dark': 'mwid-not-available.png', 'icon-light': 'mwil-not-available.png', 'icon-night-light': 'mwil-not-available.png'}
CONDITIONS['overcast'] = {'text': _('Overcast'), 'image': 'mwig-cloudy.png', 'image-night': 'mwig-cloudy.png', 'icon-dark': 'mwid-cloudy.png', 'icon-night-dark': 'mwid-cloudy.png', 'icon-light': 'mwil-cloudy.png', 'icon-night-light': 'mwil-cloudy.png'}
CONDITIONS['partial fog'] = {'text': _('Partial fog'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['partly cloudy'] = {'text': _('Partly cloudy'), 'image': 'mwig-partly-cloudy.png', 'image-night': 'mwig-partly-cloudy-night.png', 'icon-dark': 'mwid-partly-cloudy.png', 'icon-night-dark': 'mwid-partly-cloudy-night.png', 'icon-light': 'mwil-partly-cloudy.png', 'icon-night-light': 'mwil-partly-cloudy-night.png'}
CONDITIONS['partly sunny'] = {'text': _('Partly sunny'), 'image': 'mwig-partly-cloudy.png', 'image-night': 'mwig-partly-cloudy-night.png', 'icon-dark': 'mwid-partly-cloudy.png', 'icon-night-dark': 'mwid-partly-cloudy-night.png', 'icon-light': 'mwil-partly-cloudy.png', 'icon-night-light': 'mwil-partly-cloudy-night.png'}
CONDITIONS['patches of fog'] = {'text': _('Patches of fog'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['patchy freezing drizzle nearby'] = {'text': _('Patchy freezing drizzle nearby'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['patchy heavy snow'] = {'text': _('Patchy heavy snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['patchy light drizzle'] = {'text': _('Patchy light drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['patchy light rain in area with thunder'] = {'text': _('Patchy light rain in area with thunder'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['patchy light rain'] = {'text': _('Patchy light rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['patchy light snow in area with thunder'] = {'text': _('Patchy light snow in area with thunder'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['patchy light snow'] = {'text': _('Patchy light snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['patchy moderate snow'] = {'text': _('Patchy moderate snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['patchy rain nearby'] = {'text': _('Patchy rain nearby'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['patchy sleet nearby'] = {'text': _('Patchy sleet nearby'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['patchy snow nearby'] = {'text': _('Patchy snow nearby'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['ragged thunderstorm'] = {'text': _('Ragged thunderstorm'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['rain and snow'] = {'text': _('Rain and snow'), 'image': 'mwig-rain-and-snow.png', 'image-night': 'mwig-rain-and-snow.png', 'icon-dark': 'mwid-rain-and-snow.png', 'icon-night-dark': 'mwid-rain-and-snow.png', 'icon-light': 'mwil-rain-and-snow.png', 'icon-night-light': 'mwil-rain-and-snow.png'}
CONDITIONS['rain mist'] = {'text': _('Rain mist'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['rain showers'] = {'text': _('Rain showers'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['rain'] = {'text': _('Rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['sand'] = {'text': _('Sand'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['sandstorm'] = {'text': _('Sandstorm'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['scattered clouds'] = {'text': _('Scattered clouds'), 'image': 'mwig-partly-cloudy.png', 'image-night': 'mwig-partly-cloudy-night.png', 'icon-dark': 'mwid-partly-cloudy.png', 'icon-night-dark': 'mwid-partly-cloudy-night.png', 'icon-light': 'mwil-partly-cloudy.png', 'icon-night-light': 'mwil-partly-cloudy-night.png'}
CONDITIONS['scattered showers'] = {'text': _('Scattered showers'), 'image': 'mwig-chance-of-rain.png', 'image-night': 'mwig-chance-of-rain-night.png', 'icon-dark': 'mwid-chance-of-rain.png', 'icon-night-dark': 'mwid-chance-of-rain-night.png', 'icon-light': 'mwil-chance-of-rain.png', 'icon-night-light': 'mwil-chance-of-rain-night.png'}
CONDITIONS['scattered thunderstorms'] = {'text': _('Scattered thunderstorms'), 'image': 'mwig-chance-of-thunderstorms.png', 'image-night': 'mwig-chance-of-thunderstorms-night.png', 'icon-dark': 'mwid-chance-of-thunderstorms.png', 'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png', 'icon-light': 'mwil-chance-of-thunderstorms.png', 'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'}
CONDITIONS['shallow fog'] = {'text': _('Shallow fog'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['showers'] = {'text': _('Showers'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['shower drizzle'] = {'text': _('Shower drizzle'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['shower rain'] = {'text': _('Shower rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['shower snow'] = {'text': _('Shower snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['sleet'] = {'text': _('Sleet'), 'image': 'mwig-rain-and-snow.png', 'image-night': 'mwig-rain-and-snow.png', 'icon-dark': 'mwid-rain-and-snow.png', 'icon-night-dark': 'mwid-rain-and-snow.png', 'icon-light': 'mwil-rain-and-snow.png', 'icon-night-light': 'mwil-rain-and-snow.png'}
CONDITIONS['small hail showers'] = {'text': _('Small hail showers'), 'image': 'mwig-hail.png', 'image-night': 'mwig-hail.png', 'icon-dark': 'mwid-hail.png', 'icon-night-dark': 'mwid-hail.png', 'icon-light': 'mwil-hail.png', 'icon-night-light': 'mwil-hail.png'}
CONDITIONS['small hail'] = {'text': _('Small hail'), 'image': 'mwig-hail.png', 'image-night': 'mwig-hail.png', 'icon-dark': 'mwid-hail.png', 'icon-night-dark': 'mwid-hail.png', 'icon-light': 'mwil-hail.png', 'icon-night-light': 'mwil-hail.png'}
CONDITIONS['smoke'] = {'text': _('Smoke'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['snow blowing snow mist'] = {'text': _('Snow blowing snow mist'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['snow flurries'] = {'text': _('Snow flurries'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['snow grains'] = {'text': _('Snow grains'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['snow showers'] = {'text': _('Snow showers'), 'image': 'mwig-rain-and-snow.png', 'image-night': 'mwig-rain-and-snow.png', 'icon-dark': 'mwid-rain-and-snow.png', 'icon-night-dark': 'mwid-rain-and-snow.png', 'icon-light': 'mwil-rain-and-snow.png', 'icon-night-light': 'mwil-rain-and-snow.png'}
CONDITIONS['snow'] = {'text': _('Snow'), 'image': 'mwig-snow.png', 'image-night': 'mwig-snow.png', 'icon-dark': 'mwid-snow.png', 'icon-night-dark': 'mwid-snow.png', 'icon-light': 'mwil-snow.png', 'icon-night-light': 'mwil-snow.png'}
CONDITIONS['spray'] = {'text': _('Spray'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['squalls'] = {'text': _('Squalls'), 'image': 'mwig-windy.png', 'image-night': 'mwig-windy.png', 'icon-dark': 'mwid-windy.png', 'icon-night-dark': 'mwid-windy.png', 'icon-light': 'mwil-windy.png', 'icon-night-light': 'mwil-windy.png'}
CONDITIONS['storm'] = {'text': _('Storm'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['sunny'] = {'text': _('Sunny'), 'image': 'mwig-clear.png', 'image-night': 'mwig-clear-night.png', 'icon-dark': 'mwid-clear.png', 'icon-night-dark': 'mwid-clear-night.png', 'icon-light': 'mwil-clear.png', 'icon-night-light': 'mwil-clear-night.png'}
CONDITIONS['thunderstorm'] = {'text': _('Thunderstorm'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorms'] = {'text': _('Thunderstorm'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorms and ice pellets'] = {'text': _('Thunderstorms and ice pellets'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorms and rain'] = {'text': _('Thunderstorms and rain'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorms and snow'] = {'text': _('Thunderstorms and snow'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorms with hail'] = {'text': _('Thunderstorms with hail'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorms with small hail'] = {'text': _('Thunderstorms with small hail'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorm with light rain'] = {'text': _('Thunderstorm with light rain'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorm with rain'] = {'text': _('Thunderstorm with rain'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorm with heavy rain'] = {'text': _('Thunderstorm with heavy rain'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorm with light drizzle'] = {'text': _('Thunderstorm with light drizzle'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorm with drizzle'] = {'text': _('Thunderstorm with drizzle'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thunderstorm with heavy drizzle'] = {'text': _('Thunderstorm with heavy drizzle'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['thundery outbreaks in nearby'] = {'text': _('Thundery outbreaks in nearby'), 'image': 'mwig-storm.png', 'image-night': 'mwig-storm.png', 'icon-dark': 'mwid-storm.png', 'icon-night-dark': 'mwid-storm.png', 'icon-light': 'mwil-storm.png', 'icon-night-light': 'mwil-storm.png'}
CONDITIONS['tornado'] = {'text': _('Tornado'), 'image': 'mwig-windy.png', 'image-night': 'mwig-windy.png', 'icon-dark': 'mwid-windy.png', 'icon-night-dark': 'mwid-windy.png', 'icon-light': 'mwil-windy.png', 'icon-night-light': 'mwil-windy.png'}
CONDITIONS['torrential rain shower.png',] = {'text': _('Torrential rain shower'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['tropical storm'] = {'text': _('Tropical storm'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['unknown precipitation'] = {'text': _('Unknown precipitation'), 'image': 'mwig-not-available.png', 'image-night': 'mwig-not-available-night.png', 'icon-dark': 'mwid-not-available.png', 'icon-night-dark': 'mwid-not-available.png', 'icon-light': 'mwil-not-available.png', 'icon-night-light': 'mwil-not-available.png'}
CONDITIONS['unknown'] = {'text': _('Unknown'), 'image': 'mwig-not-available.png', 'image-night': 'mwig-not-available-night.png', 'icon-dark': 'mwid-not-available.png', 'icon-night-dark': 'mwid-not-available.png', 'icon-light': 'mwil-not-available.png', 'icon-night-light': 'mwil-not-available.png'}
CONDITIONS['very heavy rain'] = {'text': _('Very heavy rain'), 'image': 'mwig-rain.png', 'image-night': 'mwig-rain.png', 'icon-dark': 'mwid-rain.png', 'icon-night-dark': 'mwid-rain.png', 'icon-light': 'mwil-rain.png', 'icon-night-light': 'mwil-rain.png'}
CONDITIONS['volcanic ash'] = {'text': _('Volcanic ash'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['widespread dust'] = {'text': _('Widespread dust'), 'image': 'mwig-fog.png', 'image-night': 'mwig-fog-night.png', 'icon-dark': 'mwid-fog.png', 'icon-night-dark': 'mwid-fog-night.png', 'icon-light': 'mwil-fog.png', 'icon-night-light': 'mwil-fog-night.png'}
CONDITIONS['windy'] = {'text': _('Windy'), 'image': 'mwig-windy.png', 'image-night': 'mwig-windy.png', 'icon-dark': 'mwid-windy.png', 'icon-night-dark': 'mwid-windy.png', 'icon-light': 'mwil-windy.png', 'icon-night-light': 'mwil-windy.png'}

#
#http://en.wikipedia.org/wiki/Boxing_the_compass
#
WINDS = {'n': _('North'),
         'north': _('North'),
         'nbe': _('North by east'),
         'nne': _('North-northeast'),
         'nebn': _('Northeast by north'),
         'ne': _('Northeast'),
         'nebe': _('Northeast by east'),
         'ene': _('East-northeast'),
         'ebn': _('East by north'),
         'e': _('East'),
         'east': _('East'),
         'ebs': _('East by south'),
         'ese': _('East-southeast'),
         'sebe': _('Southeast by east'),
         'se': _('Southeast'),
         'sebs': _('Southeast by south'),
         'sse': _('South-southeast'),
         'sbe': _('South by east'),
         's': _('South'),
         'south': _('South'),
         'sbw': _('South by west'),
         'ssw': _('South-southwest'),
         'swbs': _('Southwest by south'),
         'sw': _('Southwest'),
         'swbw': _('Southwest by west'),
         'wsw': _('West-southwest'),
         'wbs': _('West by south'),
         'w': _('West'),
         'west': _('West'),
         'wbn': _('West by north'),
         'wnw': _('West-northwest'),
         'nwbw': _('Northwest by west'),
         'nw': _('Northwest'),
         'nwbn': _('Northwest by north'),
         'nnw': _('North-northwest'),
         'nbw': _('North by west'),
         'variable': _('Variable')}

WINDS2 = [['N', _('North'), 'mwi-wind00.png'],
          ['NBE', _('North by east'), 'mwi-wind01.png'],
          ['NNE', _('North-northeast'), 'mwi-wind02.png'],
          ['NEBN', _('Northeast by north'), 'mwi-wind03.png'],
          ['NE', _('Northeast'), 'mwi-wind04.png'],
          ['NEBE', _('Northeast by east'), 'mwi-wind05.png'],
          ['ENE', _('East-northeast'), 'mwi-wind06.png'],
          ['EBN', _('East by north'), 'mwi-wind07.png'],
          ['E', _('East'), 'mwi-wind08.png'],
          ['EBS', _('East by south'), 'mwi-wind09.png'],
          ['ESE', _('East-southeast'), 'mwi-wind10.png'],
          ['SEBE', _('Southeast by east'), 'mwi-wind11.png'],
          ['SE', _('Southeast'), 'mwi-wind12.png'],
          ['SEBS', _('Southeast by south'), 'mwi-wind13.png'],
          ['SSE', _('South-southeast'), 'mwi-wind14.png'],
          ['SBE', _('South by east'), 'mwi-wind15.png'],
          ['S', _('South'), 'mwi-wind16.png'],
          ['SBW', _('South by west'), 'mwi-wind17.png'],
          ['SSW', _('South-southwest'), 'mwi-wind18.png'],
          ['SWBS', _('Southwest by south'), 'mwi-wind19.png'],
          ['SW', _('Southwest'), 'mwi-wind20.png'],
          ['SWBW', _('Southwest by west'), 'mwi-wind21.png'],
          ['WSW', _('West-southwest'), 'mwi-wind22.png'],
          ['WBS', _('West by south'), 'mwi-wind23.png'],
          ['W', _('West'), 'mwi-wind24.png'],
          ['WBN', _('West by north'), 'mwi-wind25.png'],
          ['WBW', _('West-northwest'), 'mwi-wind26.png'],
          ['NWBW', _('Northwest by west'), 'mwi-wind27.png'],
          ['NW', _('Northwest'), 'mwi-wind28.png'],
          ['NWBN', _('Northwest by north'), 'mwi-wind29.png'],
          ['NNW', _('North-northwest'), 'mwi-wind30.png'],
          ['NBW', _('North by west'), 'mwi-wind31.png']]


def f2c(temperature):
    return (s2f(temperature)-32.0)*5.0/9.0


def degToCompass(num):
    val = int((s2f(num)/11.25)+0.25)
    arr = ['n', 'nbe', 'nne', 'nebn', 'ne', 'nebe', 'ene', 'ebn', 'e', 'ebs',
           'ese', 'sebe', 'se', 'sebs', 'sse', 'sbe', 's', 'sbw', 'ssw',
           'swbs', 'sw', 'swbw', 'wsw', 'wbs', 'w', 'wbn', 'wnw', 'nwbw', 'nw',
           'nwbn', 'nnw', 'nbw']
    return WINDS[arr[(val % 32)]]


def degToCompass2(num):
    val = int((s2f(num) / 11.25) + 0.25)
    return WINDS2[(val % 32)]


def time_is_lower(time1, time2):
    hora1, minutos1 = time1.split(':')
    hora2, minutos2 = time2.split(':')
    hora1 = int(hora1)
    hora2 = int(hora2)
    minutos1 = int(minutos1)
    minutos2 = int(minutos2)
    if hora1 < hora2:
        return True
    elif hora1 == hora2:
        if minutos1 < minutos2:
            return True
    return False


def time_is_upper(time1, time2):
    hora1, minutos1 = time1.split(':')
    hora2, minutos2 = time2.split(':')
    hora1 = int(hora1)
    hora2 = int(hora2)
    minutos1 = int(minutos1)
    minutos2 = int(minutos2)
    if hora1 > hora2:
        return True
    elif hora1 == hora2:
        if minutos1 > minutos2:
            return True
    return False


def get_condition_wwa(condition, tipo):
    if condition in CONDITIONS.keys():
        return CONDITIONS[condition][tipo]
    return CONDITIONS['not available'][tipo]


def get_condition(condition, tipo):
    text = ''
    if condition is not None and len(condition) > 0:
        if condition.startswith('heavy'):
            condition = condition[6:]
            text = _('Heavy')+' '
        elif condition.startswith('light'):
            condition = condition[6:]
            text = _('Light')+' '
        if condition in CONDITIONS.keys():
            return CONDITIONS[condition][tipo]
        else:
            if tipo == 'text':
                return 'Error: %s' % condition
    return CONDITIONS['not available'][tipo]


def get_humidity(text):
    if text is not None and len(text) > 0:
        return text.split(' ')[1].strip()[:-1]
    return ''


def is_day_now(sunrise, sunset, rawOffset):
    now = datetime.time(datetime.utcnow() + timedelta(hours=rawOffset))
    hora = ('%s:%s') % (now.hour, now.minute)
    print('********************************************************')
    print('********************************************************')
    print(('%s << %s << %s') % (sunrise, hora, sunset))
    print('********************************************************')
    print('********************************************************')
    if time_is_lower(sunset, sunrise):
        # The sunset actually occurs on the next day based on UTC
        if time_is_lower(hora, sunrise) and time_is_upper(hora, sunset):
            return False
    else:
        if time_is_lower(hora, sunrise) or time_is_upper(hora, sunset):
            return False
    return True


def get_moon_icon(day):
    moon = Moon(day)
    return moon.icon()


def get_moon_phase(day):
    moon = Moon(day)
    return moon.phase()


def get_key(key, tree, default=None):
    if key.find('|') > -1:
            ans = tree
            for akey in key.split('|'):
                ans = get_key(akey, ans)
            return ans
    else:
        if key in tree.keys():
            return tree[key]
        return default


def get_dayLength(day, longitude, latitude):
    sun = Sun()
    return sun.dayLength(
        day.year, day.month, day.day, s2f(longitude), s2f(latitude))


def get_dayCivilTwilightLength(day, longitude, latitude):
    sun = Sun()
    return sun.dayCivilTwilightLength(
        day.year, day.month, day.day,  s2f(longitude), s2f(latitude))


def get_dawn(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.civilTwilightLocal(
        day.year, day.month, day.day, s2f(longitude), s2f(latitude), rawOffset)
    return '%s' % (ss[0])


def get_dusk(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.civilTwilightLocal(
        day.year, day.month, day.day, s2f(longitude), s2f(latitude), rawOffset)
    return '%s' % (ss[1])


def get_sunrise(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.sunRiseSetLocal(
        day.year, day.month, day.day, s2f(longitude), s2f(latitude), rawOffset)
    return '%s' % (ss[0])


def get_sunset(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.sunRiseSetLocal(
        day.year, day.month, day.day, s2f(longitude), s2f(latitude), rawOffset)
    return '%s' % (ss[1])


def s2f(cadena):
    try:
        value = float(cadena)
    except:
        value = 0.0
    return value


def redondea(valor, digits=0):
    if digits == 0:
        return int(round(valor, digits))
    return round(valor, digits)


def change_temperature(valor, a):
    valor = s2f(valor)
    # initial a in ºF
    if a == 'C':
        valor = 5.0/9.0*(valor - 32.0)
    elif a == 'K':
        valor = 5.0/9.0*(valor - 32.0) + 273.15
    return str(redondea(valor))


def change_temperature2(valor, a):
    valor = s2f(valor)
    # initial a in ºF
    if a == 'C':
        valor = 5.0/9.0*(valor - 32.0)
    elif a == 'K':
        valor = 5.0/9.0*(valor - 32.0) + 273.15
        return '{0} {1}'.format(redondea(valor), a)
    if sys.version_info[0] == 3:
        return '{0} {1:c}{2}'.format(redondea(valor), 176, a)
    return str(redondea(valor))+unichr(176)


def get_wind_chill(temperature, wind_velocity):
    wind_velocity = s2f(wind_velocity)
    temperature = s2f(temperature)
    # temperature ºF
    # wind_velocity mph
    if temperature <= 50.0 and wind_velocity >= 3.0:
        wc = 35.74 + 0.6215 * temperature - 35.76 *\
            math.pow(wind_velocity, 0.16) + 0.4275 * temperature *\
            math.pow(wind_velocity, 0.16)
        return wc - temperature
    return 0.0


def get_wind_icon(wind_direction):
    wind_direction = wind_direction.upper()
    for element in WINDS2:
        if wind_direction == element[0]:
            return element[2]
    return WINDS2[0][2]


def get_wind_condition(wind_velocity, wind_direction, wind_units):
    wind_velocity = s2f(wind_velocity)
    wind_direction = wind_direction.lower()
    if wind_direction in WINDS.keys():
        wind_direction = WINDS[wind_direction]
    wind_velocity = change_velocity(wind_velocity, wind_units)
    if wind_units == 'Beaufort':
        return wind_velocity+' '+_('from')+' '+wind_direction
    else:
        return _('from')+' '+wind_direction+' '+_('at')+' '+wind_velocity
    return _('n/a')


def get_wind_condition2(wind_velocity, wind_direction, wind_units):
    wind_velocity = change_velocity(s2f(wind_velocity), wind_units)
    return '%s (%s)' % (wind_velocity, wind_direction)


def get_feels_like(temperature, humidity, wind_velocity, temperature_units):
    # temperature ºF
    # velocity mph
    temperature = s2f(temperature)
    humidity = s2f(humidity)
    wind_velocity = s2f(wind_velocity)
    hi = get_heat_index(temperature, humidity)
    wc = get_wind_chill(temperature, wind_velocity)
    ta = temperature + hi + wc
    return change_temperature(ta, temperature_units)


def get_dew_point(humidity, temperature, temperature_units):
    # humidity (%)
    # temperature (ºF)
    if humidity and temperature and humidity > 0.0:
        h = s2f(humidity)
        t = s2f(temperature)
        t = 5.0/9.0*(t - 32.0)
        dp = math.pow(h/100.0, 1.0/8.0)*(110.0+t) - 110.0
        dp = redondea(9.0/5.0 * dp + 32)
        return change_temperature(dp, temperature_units)
    return _('n/a')


def get_heat_index(temperature, humidity):
    temperature = s2f(temperature)
    humidity = s2f(humidity)
    if humidity > 0.0 and temperature >= 77.0:
        # temperature ºF
        # humidity over 100
        c1 = -42.379
        c2 = 2.04901523
        c3 = 10.14333127
        c4 = -0.22475541
        c5 = -0.00683783
        c6 = -0.05481717
        c7 = 0.00122874
        c8 = 0.00085282
        c9 = -0.00000199
        hi = c1 + c2 * temperature + c3 * humidity + c4 * temperature *\
            humidity + c5 * math.pow(temperature, 2.0) + c6 *\
            math.pow(humidity, 2.0) + c7 * math.pow(temperature, 2.0) *\
            humidity + c8 * temperature * math.pow(humidity, 2.0) + c9 *\
            math.pow(temperature, 2.0) * math.pow(humidity, 2.0)
        return hi - temperature
    return 0


def change_pressure(valor, a):
    valor = s2f(valor)
    units_u = {'mb': 1, 'in': 0.0294985250737, 'mm': 0.751879699248}
    units_m = {'mb': _('millibar'), 'in': _('inches of mercury'),
               'mm': _('millimeters of mercury')}
    if a in units_u.keys():
        if a == 'in':
            digits = 1
        else:
            digits = 0
        return '%s %s' % (
            locale.str(redondea(valor*units_u[a], digits)), units_m[a])


def change_distance(valor, a):
    valor = s2f(valor)
    units_u = {'mi': 1, 'km': 1.609344}
    units_m = {'mi': _('mi'), 'km': _('km')}
    if a in units_u.keys():
        return '%s %s' % (locale.str(redondea(valor*units_u[a])), units_m[a])


def change_longitude(valor, a):
    valor = s2f(valor)
    units_u = {'in': 1, 'cm': 2.54, 'mm': 25.4}
    units_m = {'in': _('in'), 'cm': _('cm'), 'mm': _('mm')}
    if a in units_u.keys():
        return '%s %s' % (locale.str(redondea(valor*units_u[a])), units_m[a])


def change_velocity(valor, a):
    valor = s2f(valor)
    # initial a in mph
    units_u = {'mph': 1, 'km/h': 1.609344, 'm/s': 0.44704,
               'knots': 0.868976, 'ft/s': 1.466667}
    units_m = {'mph': _('mph'), 'km/h': _('km/h'), 'm/s': _('m/s'),
               'knots': _('knots'), 'ft/s': _('ft/s')}
    if a in units_u.keys():
        return '%s %s' % (locale.str(redondea(valor*units_u[a])), units_m[a])
    if a == 'Beaufort':
        if valor <= 1:
            return _('Calm')
        elif valor <= 3:
            return _('Light air')
        elif valor <= 7:
            return _('Light breeze')
        elif valor <= 12:
            return _('Gentle breeze')
        elif valor <= 17:
            return _('Moderate breeze')
        elif valor <= 24:
            return _('Fresh breeze')
        elif valor <= 30:
            return _('Strong breeze')
        elif valor <= 38:
            return _('High wind')
        elif valor <= 46:
            return _('Gale')
        elif valor <= 54:
            return _('Strong gale')
        elif valor <= 63:
            return _('Storm')
        elif valor <= 72:
            return _('Violent storm')
        elif valor > 72:
            return _('Hurricane')
    return ''


def timeformat(hhmm, AMPM=False):
    """
    This method converts time in 24h format to 12h format
    Example:   "00:32" is "12:32 AM"
    "13:33" is "01:33 PM"
    """

    hh, mm = hhmm.split(":")
    if s2f(mm) == 60.0:
        hh = str(int(s2f(hh)+1.0))
        hhmm = hh + ':00'
    if AMPM:
        ampm = hhmm.split(":")
        if (len(ampm) == 0) or (len(ampm) > 3):
            return hhmm
        # is AM? from [00:00, 12:00[
        hour = int(ampm[0]) % 24
        isam = (hour >= 0) and (hour < 12)
        # 00:32 should be 12:32 AM not 00:32
        if isam:
            ampm[0] = ('12' if (hour == 0) else "%02d" % (hour))
        else:
            ampm[0] = ('12' if (hour == 12) else "%02d" % (hour-12))
        return ': '.join(ampm) + (' AM' if isam else ' PM')
    else:
        return hhmm


class Units():

    def __init__(self, temperature='C', wind='km/h', pressure='mb',
                 visibility='km', snow='cm', rain='mm', ampm=False):
        self.temperature = temperature
        self.wind = wind
        self.pressure = pressure
        self.visibility = visibility
        self.snow = snow
        self.rain = rain
        self.ampm = ampm


class WeatherService():

    def __init__(self, longitude=-0.418, latitude=39.360, units=Units(),
                 key=''):
        if not longitude:
            longitude = 0
        if not latitude:
            latitude = 0
        self.key = key
        self.longitude = longitude
        self.latitude = latitude
        self.timezoneId = geocodeapi.get_timezoneId(latitude, longitude)
        self.units = units

    def get_default_values(self):
        current_conditions = {}
        current_conditions['rawOffset'] =\
            geocodeapi.get_rawOffset(self.timezoneId)
        current_conditions['condition_text'] = _('Not available')
        current_conditions['condition_image'] = 'mwig-not-available.png'
        current_conditions['condition_icon_dark'] = 'mwid-not-available.png'
        current_conditions['condition_icon_light'] = 'mwil-not-available.png'
        current_conditions['temperature'] = _('N/A')
        current_conditions['pressure'] = _('N/A')
        current_conditions['humidity'] = _('N/A')
        current_conditions['dew_point'] = _('N/A')
        current_conditions['wind_condition'] = _('N/A')
        current_conditions['wind_icon'] = None
        #
        current_conditions['heat_index'] = _('N/A')
        current_conditions['windchill'] = _('N/A')
        #
        current_conditions['feels_like'] = _('N/A')
        #
        current_conditions['visibility'] = _('N/A')
        current_conditions['cloudiness'] = _('N/A')
        current_conditions['solarradiation'] = _('N/A')
        current_conditions['UV'] = _('N/A')
        current_conditions['precip_1hr'] = _('N/A')
        current_conditions['precip_today'] = _('N/A')
        #
        dayLength = get_dayLength(
            datetime.today(), self.longitude, self.latitude)
        dayCivilTwilightLength = get_dayCivilTwilightLength(
            datetime.today(), self.longitude, self.latitude)
        if dayLength == 0.0:
            current_conditions['sunrise_time'] = _('Down all day')
            current_conditions['sunset_time'] = _('Down all day')
            current_conditions['sunrise'] = _('Down all day')
            current_conditions['sunset'] = _('Down all day')
            current_conditions['isday'] = False
        elif dayLength == 24.0:
            current_conditions['sunrise_time'] = _('Up all day')
            current_conditions['sunset_time'] = _('Up all day')
            current_conditions['sunrise'] = _('Up all day')
            current_conditions['sunset'] = _('Up all day')
            current_conditions['isday'] = True
        else:
            current_conditions['sunrise_time'] = get_sunrise(
                datetime.today(), self.longitude, self.latitude,
                current_conditions['rawOffset'])
            current_conditions['sunset_time'] = get_sunset(
                datetime.today(), self.longitude, self.latitude,
                current_conditions['rawOffset'])
            current_conditions['isday'] = is_day_now(
                current_conditions['sunrise_time'],
                current_conditions['sunset_time'],
                current_conditions['rawOffset'])
            current_conditions['sunrise'] = timeformat(
                current_conditions['sunrise_time'], self.units.ampm)
            current_conditions['sunset'] = timeformat(
                current_conditions['sunset_time'], self.units.ampm)
        current_conditions['sunrise_time_utc'] = get_sunrise(
            datetime.today(), self.longitude, self.latitude, 0)
        current_conditions['sunset_time_utc'] = get_sunset(
            datetime.today(), self.longitude, self.latitude, 0)
        if dayCivilTwilightLength == 0.0:
            current_conditions['dawn_time'] = _('Down all day')
            current_conditions['dusk_time'] = _('Down all day')
            current_conditions['dawn'] = _('Down all day')
            current_conditions['dusk'] = _('Down all day')
        elif dayLength == 24.0:
            current_conditions['dawn_time'] = _('Up all day')
            current_conditions['dusk_time'] = _('Up all day')
            current_conditions['dawn'] = _('Up all day')
            current_conditions['dusk'] = _('Up all day')
        else:
            current_conditions['dawn_time'] = get_dawn(
                datetime.today(), self.longitude, self.latitude,
                current_conditions['rawOffset'])
            current_conditions['dusk_time'] = get_dusk(
                datetime.today(), self.longitude, self.latitude,
                current_conditions['rawOffset'])
            current_conditions['dawn'] = timeformat(
                current_conditions['dawn_time'], self.units.ampm)
            current_conditions['dusk'] = timeformat(
                current_conditions['dusk_time'], self.units.ampm)
        current_conditions['moon_icon'] = get_moon_icon(datetime.today())
        current_conditions['moon_phase'] = get_moon_phase(datetime.today())
        dayLength = get_dayLength(
            datetime.today(), self.longitude, self.latitude)
        dayCivilTwilightLength = get_dayCivilTwilightLength(
            datetime.today(), self.longitude, self.latitude)
        if current_conditions['sunrise_time'] ==\
                current_conditions['sunset_time']:
            if dayLength > 0:
                current_conditions['sunrise_time'] = _('Up all day')
                current_conditions['sunset_time'] = _('Up all day')
            else:
                current_conditions['sunrise_time'] = _('Down all day')
                current_conditions['sunset_time'] = _('Down all day')
        if current_conditions['dawn_time'] == current_conditions['dusk_time']:
            if dayCivilTwilightLength > 0:
                current_conditions['dawn_time'] = _('Up all day')
                current_conditions['dusk_time'] = _('Up all day')
            else:
                current_conditions['dawn_time'] = _('Down all day')
                current_conditions['dusk_time'] = _('Down all day')

        #
        forecast_conditions = []
        dia = datetime.today()
        undia = timedelta(days=1)
        for i in range(0, 7):
            fc = {}
            fc['day_of_week'] = dia.strftime('%A').capitalize()
            fc['low'] = _('N/A')
            fc['high'] = _('N/A')
            fc['cloudiness'] = _('N/A')
            #
            fc['qpf_allday'] = _('N/A')
            fc['qpf_day'] = _('N/A')
            fc['qpf_night'] = _('N/A')
            fc['snow_allday'] = _('N/A')
            fc['snow_day'] = _('N/A')
            fc['snow_night'] = _('N/A')
            fc['maxwind'] = _('N/A')
            fc['avewind'] = _('N/A')
            fc['wind_icon'] = None
            fc['avehumidity'] = _('N/A')
            fc['maxhumidity'] = _('N/A')
            fc['minhumidity'] = _('N/A')
            #
            fc['condition'] = _('N/A')
            fc['condition_text'] = _('N/A')
            fc['condition_image'] = 'mwig-not-available.png'
            fc['condition_icon'] = 'mwil-not-available.png'
            dayLength = get_dayLength(
                datetime.today(), self.longitude, self.latitude)
            if dayLength == 0.0:
                fc['sunrise'] = _('Down all day')
                fc['sunset'] = _('Down all day')
            elif dayLength == 24.0:
                fc['sunrise'] = _('Up all day')
                fc['sunset'] = _('Up all day')
            else:
                fc['sunrise'] = timeformat(get_sunrise(
                    dia, self.longitude, self.latitude,
                    current_conditions['rawOffset']), self.units.ampm)
                fc['sunset'] = timeformat(get_sunset(
                    dia, self.longitude, self.latitude,
                    current_conditions['rawOffset']), self.units.ampm)
            fc['moon_icon'] = get_moon_icon(dia)
            fc['moon_phase'] = get_moon_phase(dia)
            forecast_conditions.append(fc)
            dia = dia + undia
        #
        forecast_information = {}
        forecast_information['city'] = '...'
        forecast_information['postal_code'] = ''
        forecast_information['latitude_e6'] = ''
        forecast_information['longitude_e6'] = ''
        forecast_information['forecast_date'] = ''
        forecast_information['current_date_time'] = ''
        forecast_information['unit_system'] = 'SI'
        #
        weather_data = {}
        weather_data['current_conditions'] = current_conditions
        weather_data['forecasts'] = forecast_conditions
        weather_data['forecast_information'] = forecast_information
        return weather_data

    def get_weather(self):
        pass

if __name__ == '__main__':
    print(get_condition('light rain', 'image'))
    print(get_condition('heavy rain', 'text'))
    print(degToCompass(9))
    print('Esta es la temperatura ' + change_temperature(20, 'C'))
