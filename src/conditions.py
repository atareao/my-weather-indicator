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

from comun import _

CONDITIONS = {
    'blowing sand': {
        'text': _('Blowing sand'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    },
    'blizzard': {
        'text': _('Blizzard'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    },
    'blowing snow': {
        'text': _('Blowing snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'blowing widespread dust': {
        'text': _('Blowing widespread dust'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    },
    'blustery': {
        'text': _('Blustery'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'chance of a thunderstorm': {
        'text': _('Chance of a thunderstorm'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'chance of flurries': {
        'text': _('Chance of flurries'),
        'image': 'mwig-chance-of-snow.png',
        'image-night': 'mwig-chance-of-snow-night.png',
        'icon-dark': 'mwid-chance-of-snow.png',
        'icon-night-dark': 'mwid-chance-of-snow-night.png',
        'icon-light': 'mwil-chance-of-snow.png',
        'icon-night-light': 'mwil-chance-of-snow-night.png'
    },
    'chance of rain': {
        'text': _('Chance of rain'),
        'image': 'mwig-chance-of-rain.png',
        'image-night': 'mwig-chance-of-rain-night.png',
        'icon-dark': 'mwid-chance-of-rain.png',
        'icon-night-dark': 'mwid-chance-of-rain-night.png',
        'icon-light': 'mwil-chance-of-rain.png',
        'icon-night-light': 'mwil-chance-of-rain-night.png'
    },
    'chance of showers': {
        'text': _('Chance of showers'),
        'image': 'mwig-chance-of-rain.png',
        'image-night': 'mwig-chance-of-rain-night.png',
        'icon-dark': 'mwid-chance-of-rain.png',
        'icon-night-dark': 'mwid-chance-of-rain-night.png',
        'icon-light': 'mwil-chance-of-rain.png',
        'icon-night-light': 'mwil-chance-of-rain-night.png'
    },
    'chance of snow': {
        'text': _('Chance of snow'),
        'image': 'mwig-chance-of-snow.png',
        'image-night': 'mwig-chance-of-snow-night.png',
        'icon-dark': 'mwid-chance-of-snow.png',
        'icon-night-dark': 'mwid-chance-of-snow-night.png',
        'icon-light': 'mwil-chance-of-snow.png',
        'icon-night-light': 'mwil-chance-of-snow-night.png'
    },
    'chance of storm': {
        'text': _('Chance of storm'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'chance of thunderstorms': {
        'text': _('Chance of thunderstorms'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'chance of tstorm': {
        'text': _('Chance of tstorm'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'clear': {
        'text': _('Clear'),
        'image': 'mwig-clear.png',
        'image-night': 'mwig-clear-night.png',
        'icon-dark': 'mwid-clear.png',
        'icon-night-dark': 'mwid-clear-night.png',
        'icon-light': 'mwil-clear.png',
        'icon-night-light': 'mwil-clear-night.png'
    },
    'cloudy': {
        'text': _('Cloudy'),
        'image': 'mwig-cloudy.png',
        'image-night': 'mwig-cloudy.png',
        'icon-dark': 'mwid-cloudy.png',
        'icon-night-dark': 'mwid-cloudy.png',
        'icon-light': 'mwil-cloudy.png',
        'icon-night-light': 'mwil-cloudy.png'
    },
    'cold': {
        'text': _('Cold'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'drizzle': {
        'text': _('Drizzle'),
        'image': 'mwig-light-rain.png',
        'image-night': 'mwig-light-rain.png',
        'icon-dark': 'mwid-light-rain.png',
        'icon-night-dark': 'mwid-light-rain.png',
        'icon-light': 'mwil-light-rain.png',
        'icon-night-light': 'mwil-light-rain.png'
    },
    'drizzle rain': {
        'text': _('Drizzle rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'dust whirls': {
        'text': _('Dust whirls'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'dust': {
        'text': _('Dust'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'extreme rain': {
        'text': _('Extreme rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'fair': {
        'text': _('Fair'),
        'image': 'mwig-clear.png',
        'image-night': 'mwig-clear-night.png',
        'icon-dark': 'mwid-clear.png',
        'icon-night-dark': 'mwid-clear-night.png',
        'icon-light': 'mwil-clear.png',
        'icon-night-light': 'mwil-clear-night.png'
    },
    'flurries': {
        'text': _('Flurries'),
        'image': 'mwig-flurries.png',
        'image-night': 'mwig-flurries.png',
        'icon-dark': 'mwid-flurries.png',
        'icon-night-dark': 'mwid-flurries.png',
        'icon-light': 'mwil-flurries.png',
        'icon-night-light': 'mwil-flurries.png'
    },
    'fog patches': {
        'text': _('Fog patches'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'depositing rime fog': {
        'text': _('Depositing rime fog'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'fog': {
        'text': _('Fog'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'foggy': {
        'text': _('Foggy'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'freezing drizzle': {
        'text': _('Freezing drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'freezing fog.png': {
        'text': _('Freezing fog'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'freezing fog': {
        'text': _('Freezing fog'),
        'image': 'mwig-freezing-drizzle.png',
        'image-night': 'mwig-freezing-drizzle.png',
        'icon-dark': 'mwid-freezing-drizzle.png',
        'icon-night-dark': 'mwid-freezing-drizzle.png',
        'icon-light': 'mwil-freezing-drizzle.png',
        'icon-night-light': 'mwil-freezing-drizzle.png'
    },
    'freezing rain': {
        'text': _('Freezing rain'),
        'image': 'mwig-freezing-drizzle.png',
        'image-night': 'mwig-freezing-drizzle.png',
        'icon-dark': 'mwid-freezing-drizzle.png',
        'icon-night-dark': 'mwid-freezing-drizzle.png',
        'icon-light': 'mwil-freezing-drizzle.png',
        'icon-night-light': 'mwil-freezing-drizzle.png'
    },
    'funnel cloud': {
        'text': _('Funnel cloud'),
        'image': 'mwig-cloudy.png',
        'image-night': 'mwig-cloudy.png',
        'icon-dark': 'mwid-cloudy.png',
        'icon-night-dark': 'mwid-cloudy.png',
        'icon-light': 'mwil-cloudy.png',
        'icon-night-light': 'mwil-cloudy.png'
    },
    'hail showers': {
        'text': _('Hail showers'),
        'image': 'mwig-hail.png',
        'image-night': 'mwig-hail.png',
        'icon-dark': 'mwid-hail.png',
        'icon-night-dark': 'mwid-hail.png',
        'icon-light': 'mwil-hail.png',
        'icon-night-light': 'mwil-hail.png'
    },
    'hail': {
        'text': _('Hail'),
        'image': 'mwig-hail.png',
        'image-night': 'mwig-hail.png',
        'icon-dark': 'mwid-hail.png',
        'icon-night-dark': 'mwid-hail.png',
        'icon-light': 'mwil-hail.png',
        'icon-night-light': 'mwil-hail.png'
    },
    'haze': {
        'text': _('Haze'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'heavy freezing drizzle': {
        'text': _('Heavy freezing drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy intensity drizzle': {
        'text': _('Heavy drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy intensity drizzle rain': {
        'text': _('Heavy drizzle rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy intensity rain': {
        'text': _('Heavy rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy intensity shower rain': {
        'text': _('Heavy shower rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy rain at times': {
        'text': _('Heavy rain at times'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy rain': {
        'text': _('Heavy rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'heavy snow': {
        'text': _('Heavy snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'heavy thunderstorm': {
        'text': _('Heavy thunderstorm'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'hot': {
        'text': _('Hot'),
        'image': 'mwig-clear.png',
        'image-night': 'mwig-clear-night.png',
        'icon-dark': 'mwid-clear.png',
        'icon-night-dark': 'mwid-clear-night.png',
        'icon-light': 'mwil-clear.png',
        'icon-night-light': 'mwil-clear-night.png'
    },
    'hurricane': {
        'text': _('Hurricane'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    },
    'ice crystals': {
        'text': _('Ice crystals'),
        'image': 'mwig-icy.png',
        'image-night': 'mwig-icy.png',
        'icon-dark': 'mwid-icy.png',
        'icon-night-dark': 'mwid-icy.png',
        'icon-light': 'mwil-icy.png',
        'icon-night-light': 'mwil-icy.png'
    },
    'ice pellet showers': {
        'text': _('Ice pellet showers'),
        'image': 'mwig-icy.png',
        'image-night': 'mwig-icy.png',
        'icon-dark': 'mwid-icy.png',
        'icon-night-dark': 'mwid-icy.png',
        'icon-light': 'mwil-icy.png',
        'icon-night-light': 'mwil-icy.png'
    },
    'ice pellets.png': {
        'text': _('Ice pellets'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'ice pellets': {
        'text': _('Ice pellets'),
        'image': 'mwig-icy.png',
        'image-night': 'mwig-icy.png',
        'icon-dark': 'mwid-icy.png',
        'icon-night-dark': 'mwid-icy.png',
        'icon-light': 'mwil-icy.png',
        'icon-night-light': 'mwil-icy.png'
    },
    'icy': {
        'text': _('Icy'),
        'image': 'mwig-icy.png',
        'image-night': 'mwig-icy.png',
        'icon-dark': 'mwid-icy.png',
        'icon-night-dark': 'mwid-icy.png',
        'icon-light': 'mwil-icy.png',
        'icon-night-light': 'mwil-icy.png'
    },
    'intensity drizzle': {
        'text': _('Heavy drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'intensity drizzle rain': {
        'text': _('Heavy drizzle rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'intensity rain': {
        'text': _('Heavy rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'intensity shower rain': {
        'text': _('Heavy shower rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'isolated showers': {
        'text': _('Isolated showers'),
        'image': 'mwig-chance-of-rain.png',
        'image-night': 'mwig-chance-of-rain-night.png',
        'icon-dark': 'mwid-chance-of-rain.png',
        'icon-night-dark': 'mwid-chance-of-rain-night.png',
        'icon-light': 'mwil-chance-of-rain.png',
        'icon-night-light': 'mwil-chance-of-rain-night.png'
    },
    'isolated thundershowers': {
        'text': _('Isolated thundershowers'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'isolated thunderstorms': {
        'text': _('Isolated thunderstorms'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'light drizzle': {
        'text': _('Light drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light freezing rain': {
        'text': _('Light freezing rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light intensity drizzle': {
        'text': _('Light drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light intensity drizzle rain': {
        'text': _('Light drizzle rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light intensity shower rain': {
        'text': _('Light shower rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light rain shower': {
        'text': _('Light rain shower'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light rain': {
        'text': _('Light rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light showers of ice pellets.png': {
        'text': _('Light showers of ice pellets'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light sleet showers.png': {
        'text': _('Light sleet showers'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light sleet': {
        'text': _('Light sleet'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'light snow showers.png': {
        'text': _('Light snow showers'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'light snow': {
        'text': _('Light snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'light thunderstorm': {
        'text': _('Light thunderstorm'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'low drifting sand': {
        'text': _('Low drifting sand'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'low drifting snow': {
        'text': _('Low drifting snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'low drifting widespread dust': {
        'text': _('Low drifting widespread dust'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'mist': {
        'text': _('Mist'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'mixed rain and snow': {
        'text': _('Mixed rain and snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'mixed rain and sleet': {
        'text': _('Mixed rain and sleet'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'mixed snow and sleet': {
        'text': _('Mixed snow and sleet'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'moderate or heavy freezing rain': {
        'text': _('Moderate or heavy freezing rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate or heavy rain in area with thunder': {
        'text': _('Moderate or heavy rain in area with thunder'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'moderate or heavy rain shower': {
        'text': _('Moderate or heavy rain shower'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate or heavy showers of ice pellets': {
        'text': _('Moderate or heavy showers of ice pellets'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate or heavy sleet showers.png': {
        'text': _('Moderate or heavy sleet showers'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate or heavy sleet': {
        'text': _('Moderate or heavy sleet'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'moderate or heavy snow in area with thunder': {
        'text': _('Moderate or heavy snow in area with thunder'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'moderate or heavy snow showers': {
        'text': _('Moderate or heavy snow showers'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate rain at times': {
        'text': _('Moderate rain at times'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate rain': {
        'text': _('Moderate rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'moderate snow': {
        'text': _('Moderate snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'mostly cloudy': {
        'text': _('Mostly cloudy'),
        'image': 'mwig-mostly-cloudy.png',
        'image-night': 'mwig-mostly-cloudy-night.png',
        'icon-dark': 'mwid-mostly-cloudy.png',
        'icon-night-dark': 'mwid-mostly-cloudy-night.png',
        'icon-light': 'mwil-mostly-cloudy.png',
        'icon-night-light': 'mwil-mostly-cloudy-night.png'
    },
    'mostly sunny': {
        'text': _('Mostly sunny'),
        'image': 'mwig-mostly-sunny.png',
        'image-night': 'mwig-mostly-sunny-night.png',
        'icon-dark': 'mwid-mostly-sunny.png',
        'icon-night-dark': 'mwid-mostly-sunny-night.png',
        'icon-light': 'mwil-mostly-sunny.png',
        'icon-night-light': 'mwil-mostly-sunny-night.png'
    },
    'not available': {
        'text': _('Not available'),
        'image': 'mwig-not-available.png',
        'image-night': 'mwig-not-available-night.png',
        'icon-dark': 'mwid-not-available.png',
        'icon-night-dark': 'mwid-not-available.png',
        'icon-light': 'mwil-not-available.png',
        'icon-night-light': 'mwil-not-available.png'
    },
    'overcast': {
        'text': _('Overcast'),
        'image': 'mwig-cloudy.png',
        'image-night': 'mwig-cloudy.png',
        'icon-dark': 'mwid-cloudy.png',
        'icon-night-dark': 'mwid-cloudy.png',
        'icon-light': 'mwil-cloudy.png',
        'icon-night-light': 'mwil-cloudy.png'
    },
    'partial fog': {
        'text': _('Partial fog'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'partly cloudy': {
        'text': _('Partly cloudy'),
        'image': 'mwig-partly-cloudy.png',
        'image-night': 'mwig-partly-cloudy-night.png',
        'icon-dark': 'mwid-partly-cloudy.png',
        'icon-night-dark': 'mwid-partly-cloudy-night.png',
        'icon-light': 'mwil-partly-cloudy.png',
        'icon-night-light': 'mwil-partly-cloudy-night.png'
    },
    'partly sunny': {
        'text': _('Partly sunny'),
        'image': 'mwig-partly-cloudy.png',
        'image-night': 'mwig-partly-cloudy-night.png',
        'icon-dark': 'mwid-partly-cloudy.png',
        'icon-night-dark': 'mwid-partly-cloudy-night.png',
        'icon-light': 'mwil-partly-cloudy.png',
        'icon-night-light': 'mwil-partly-cloudy-night.png'
    },
    'patches of fog': {
        'text': _('Patches of fog'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'patchy freezing drizzle nearby': {
        'text': _('Patchy freezing drizzle nearby'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'patchy heavy snow': {
        'text': _('Patchy heavy snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'patchy light drizzle': {
        'text': _('Patchy light drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'patchy light rain in area with thunder': {
        'text': _('Patchy light rain in area with thunder'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'patchy light rain': {
        'text': _('Patchy light rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'patchy light snow in area with thunder': {
        'text': _('Patchy light snow in area with thunder'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'patchy light snow': {
        'text': _('Patchy light snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'patchy moderate snow': {
        'text': _('Patchy moderate snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'patchy rain nearby': {
        'text': _('Patchy rain nearby'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'patchy sleet nearby': {
        'text': _('Patchy sleet nearby'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'patchy snow nearby': {
        'text': _('Patchy snow nearby'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'ragged thunderstorm': {
        'text': _('Ragged thunderstorm'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'rain and snow': {
        'text': _('Rain and snow'),
        'image': 'mwig-rain-and-snow.png',
        'image-night': 'mwig-rain-and-snow.png',
        'icon-dark': 'mwid-rain-and-snow.png',
        'icon-night-dark': 'mwid-rain-and-snow.png',
        'icon-light': 'mwil-rain-and-snow.png',
        'icon-night-light': 'mwil-rain-and-snow.png'
    },
    'rain mist': {
        'text': _('Rain mist'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'rain showers': {
        'text': _('Rain showers'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'rain': {
        'text': _('Rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'sand': {
        'text': _('Sand'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'sandstorm': {
        'text': _('Sandstorm'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'scattered clouds': {
        'text': _('Scattered clouds'),
        'image': 'mwig-partly-cloudy.png',
        'image-night': 'mwig-partly-cloudy-night.png',
        'icon-dark': 'mwid-partly-cloudy.png',
        'icon-night-dark': 'mwid-partly-cloudy-night.png',
        'icon-light': 'mwil-partly-cloudy.png',
        'icon-night-light': 'mwil-partly-cloudy-night.png'
    },
    'scattered showers': {
        'text': _('Scattered showers'),
        'image': 'mwig-chance-of-rain.png',
        'image-night': 'mwig-chance-of-rain-night.png',
        'icon-dark': 'mwid-chance-of-rain.png',
        'icon-night-dark': 'mwid-chance-of-rain-night.png',
        'icon-light': 'mwil-chance-of-rain.png',
        'icon-night-light': 'mwil-chance-of-rain-night.png'
    },
    'scattered thunderstorms': {
        'text': _('Scattered thunderstorms'),
        'image': 'mwig-chance-of-thunderstorms.png',
        'image-night': 'mwig-chance-of-thunderstorms-night.png',
        'icon-dark': 'mwid-chance-of-thunderstorms.png',
        'icon-night-dark': 'mwid-chance-of-thunderstorms-night.png',
        'icon-light': 'mwil-chance-of-thunderstorms.png',
        'icon-night-light': 'mwil-chance-of-thunderstorms-night.png'
    },
    'shallow fog': {
        'text': _('Shallow fog'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'showers': {
        'text': _('Showers'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'shower drizzle': {
        'text': _('Shower drizzle'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'shower rain': {
        'text': _('Shower rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'shower snow': {
        'text': _('Shower snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'sleet': {
        'text': _('Sleet'),
        'image': 'mwig-rain-and-snow.png',
        'image-night': 'mwig-rain-and-snow.png',
        'icon-dark': 'mwid-rain-and-snow.png',
        'icon-night-dark': 'mwid-rain-and-snow.png',
        'icon-light': 'mwil-rain-and-snow.png',
        'icon-night-light': 'mwil-rain-and-snow.png'
    },
    'small hail showers': {
        'text': _('Small hail showers'),
        'image': 'mwig-hail.png',
        'image-night': 'mwig-hail.png',
        'icon-dark': 'mwid-hail.png',
        'icon-night-dark': 'mwid-hail.png',
        'icon-light': 'mwil-hail.png',
        'icon-night-light': 'mwil-hail.png'
    },
    'small hail': {
        'text': _('Small hail'),
        'image': 'mwig-hail.png',
        'image-night': 'mwig-hail.png',
        'icon-dark': 'mwid-hail.png',
        'icon-night-dark': 'mwid-hail.png',
        'icon-light': 'mwil-hail.png',
        'icon-night-light': 'mwil-hail.png'
    },
    'smoke': {
        'text': _('Smoke'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'snow blowing snow mist': {
        'text': _('Snow blowing snow mist'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'snow flurries': {
        'text': _('Snow flurries'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'snow grains': {
        'text': _('Snow grains'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'snow showers': {
        'text': _('Snow showers'),
        'image': 'mwig-rain-and-snow.png',
        'image-night': 'mwig-rain-and-snow.png',
        'icon-dark': 'mwid-rain-and-snow.png',
        'icon-night-dark': 'mwid-rain-and-snow.png',
        'icon-light': 'mwil-rain-and-snow.png',
        'icon-night-light': 'mwil-rain-and-snow.png'
    },
    'snow': {
        'text': _('Snow'),
        'image': 'mwig-snow.png',
        'image-night': 'mwig-snow.png',
        'icon-dark': 'mwid-snow.png',
        'icon-night-dark': 'mwid-snow.png',
        'icon-light': 'mwil-snow.png',
        'icon-night-light': 'mwil-snow.png'
    },
    'spray': {
        'text': _('Spray'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'squalls': {
        'text': _('Squalls'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    },
    'storm': {
        'text': _('Storm'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'sunny': {
        'text': _('Sunny'),
        'image': 'mwig-clear.png',
        'image-night': 'mwig-clear-night.png',
        'icon-dark': 'mwid-clear.png',
        'icon-night-dark': 'mwid-clear-night.png',
        'icon-light': 'mwil-clear.png',
        'icon-night-light': 'mwil-clear-night.png'
    },
    'thunderstorm': {
        'text': _('Thunderstorm'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorms': {
        'text': _('Thunderstorm'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorms and ice pellets': {
        'text': _('Thunderstorms and ice pellets'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorms and rain': {
        'text': _('Thunderstorms and rain'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorms and snow': {
        'text': _('Thunderstorms and snow'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorms with hail': {
        'text': _('Thunderstorms with hail'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorms with small hail': {
        'text': _('Thunderstorms with small hail'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorm with light rain': {
        'text': _('Thunderstorm with light rain'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorm with rain': {
        'text': _('Thunderstorm with rain'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorm with heavy rain': {
        'text': _('Thunderstorm with heavy rain'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorm with light drizzle': {
        'text': _('Thunderstorm with light drizzle'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorm with drizzle': {
        'text': _('Thunderstorm with drizzle'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thunderstorm with heavy drizzle': {
        'text': _('Thunderstorm with heavy drizzle'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'thundery outbreaks in nearby': {
        'text': _('Thundery outbreaks in nearby'),
        'image': 'mwig-storm.png',
        'image-night': 'mwig-storm.png',
        'icon-dark': 'mwid-storm.png',
        'icon-night-dark': 'mwid-storm.png',
        'icon-light': 'mwil-storm.png',
        'icon-night-light': 'mwil-storm.png'
    },
    'tornado': {
        'text': _('Tornado'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    },
    'torrential rain shower.png': {
        'text': _('Torrential rain shower'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'tropical storm': {
        'text': _('Tropical storm'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'unknown precipitation': {
        'text': _('Unknown precipitation'),
        'image': 'mwig-not-available.png',
        'image-night': 'mwig-not-available-night.png',
        'icon-dark': 'mwid-not-available.png',
        'icon-night-dark': 'mwid-not-available.png',
        'icon-light': 'mwil-not-available.png',
        'icon-night-light': 'mwil-not-available.png'
    },
    'unknown': {
        'text': _('Unknown'),
        'image': 'mwig-not-available.png',
        'image-night': 'mwig-not-available-night.png',
        'icon-dark': 'mwid-not-available.png',
        'icon-night-dark': 'mwid-not-available.png',
        'icon-light': 'mwil-not-available.png',
        'icon-night-light': 'mwil-not-available.png'
    },
    'very heavy rain': {
        'text': _('Very heavy rain'),
        'image': 'mwig-rain.png',
        'image-night': 'mwig-rain.png',
        'icon-dark': 'mwid-rain.png',
        'icon-night-dark': 'mwid-rain.png',
        'icon-light': 'mwil-rain.png',
        'icon-night-light': 'mwil-rain.png'
    },
    'volcanic ash': {
        'text': _('Volcanic ash'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'widespread dust': {
        'text': _('Widespread dust'),
        'image': 'mwig-fog.png',
        'image-night': 'mwig-fog-night.png',
        'icon-dark': 'mwid-fog.png',
        'icon-night-dark': 'mwid-fog-night.png',
        'icon-light': 'mwil-fog.png',
        'icon-night-light': 'mwil-fog-night.png'
    },
    'windy': {
        'text': _('Windy'),
        'image': 'mwig-windy.png',
        'image-night': 'mwig-windy.png',
        'icon-dark': 'mwid-windy.png',
        'icon-night-dark': 'mwid-windy.png',
        'icon-light': 'mwil-windy.png',
        'icon-night-light': 'mwil-windy.png'
    }
}
#
# http://en.wikipedia.org/wiki/Boxing_the_compass
#
WINDS = {
    'n': _('North'),
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
    'variable': _('Variable')
}

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
          ['WNW', _('West-northwest'), 'mwi-wind26.png'],
          ['NWBW', _('Northwest by west'), 'mwi-wind27.png'],
          ['NW', _('Northwest'), 'mwi-wind28.png'],
          ['NWBN', _('Northwest by north'), 'mwi-wind29.png'],
          ['NNW', _('North-northwest'), 'mwi-wind30.png'],
          ['NBW', _('North by west'), 'mwi-wind31.png']]

