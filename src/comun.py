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

import os
import locale
import logging
import gettext
import requests
from check_connection import check_connectivity
import urllib.request
import urllib.parse
import urllib.error

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ = '$24/09/2011'
__copyright__ = 'Copyright (c) 2011 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'

logger = logging.getLogger(__name__)


def is_package():
    return __file__.find('src') < 0


PARAMS = {'first-time': True,
          'version': '',
          'main-location': True,
          'autolocation': False,
          'location': '',
          'latitude': 0,
          'longitude': 0,
          'timezone': '',
          'show-temperature': True,
          'show-notifications': True,
          'second-location': False,
          'location2': '',
          'latitude2': 0,
          'longitude2': 0,
          'timezone2': '',
          'show-temperature2': True,
          'show-notifications2': True,
          'temperature': 'C',
          'pressure': 'mbar',
          'visibility': 'km',
          'wind': 'km/h',
          'snow': 'cm',
          'rain': 'mm',
          '24h': True,
          'refresh': 1,
          'icon-light': True,
          'wwo-key': '',
          'wu-key': '',
          'widget1': False,
          'widget2': False,
          'onwidget1hide': False,
          'onwidget2hide': False,
          'onwidget1top': False,
          'onwidget2top': False,
          'showintaskbar1': False,
          'showintaskbar2': False,
          'onalldesktop1': True,
          'onalldesktop2': True,
          'skin1': '/usr/share/my-weather-indicator/skins/little',
          'skin2': '/usr/share/my-weather-indicator/skins/little',
          'wp1-x': 0,
          'wp1-y': 0,
          'wp2-x': 0,
          'wp2-y': 0,
          'http-proxy': '',
          'http-port': 0,
          'https-proxy': '',
          'https-port': 0
          }

APP = 'my-weather-indicator'
APP_CONF = APP + '.conf'
APPNAME = 'My-Weather-Indicator'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APP_CONF)
#########################################

# check if running from source
if is_package():
    ROOTDIR = '/opt/extras.ubuntu.com/my-weather-indicator/share/'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    LOGOSDIR = os.path.join(APPDIR, 'logos')
    ICONDIR = os.path.join(APPDIR, 'icons')
    IMAGESDIR = os.path.join(APPDIR, 'images')
    SOCIALDIR = os.path.join(APPDIR, 'social')
    WIMAGESDIR = os.path.join(APPDIR, 'wimages')
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    STYLEDIR = os.path.join(APPDIR, 'style')
    ICON = os.path.join(ROOTDIR, 'pixmaps/my-weather-indicator.png')
    AUTOSTART = os.path.join(APPDIR, 'my-weather-indicator-autostart.desktop')
    AEMETDB = os.path.join(APPDIR, 'spain-data.db')
else:
    ROOTDIR = os.path.abspath(os.path.dirname(__file__))
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    DATADIR = os.path.normpath(os.path.join(ROOTDIR, '../data'))
    STYLEDIR = DATADIR
    LOGOSDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/logos'))
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
    IMAGESDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/images'))
    SOCIALDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/social'))
    WIMAGESDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/wimages'))
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    ICON = os.path.join(IMAGESDIR, 'my-weather-indicator.png')
    AUTOSTART = os.path.join(DATADIR, 'my-weather-indicator-autostart.desktop')
    AEMETDB = os.path.join(DATADIR, 'spain-data.db')

f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'
CSS_FILE = os.path.join(STYLEDIR, 'style.css')
HTML = os.path.join(APPDIR, 'openweathermap', 'openweathermap.html')
HTML_WAI = os.path.join(APPDIR, 'whereami', 'whereami.html')
HTML_GRAPH = os.path.join(APPDIR, 'graph', 'graph.html')
GOOGLELOGO = os.path.join(LOGOSDIR, 'wgooglelogo.png')
UNDERGROUNDLOGO = os.path.join(LOGOSDIR, 'wundergroundlogo.png')
UNDERGROUNDWEB = 'http://www.wunderground.com/?apiref=6563686488165a78'
YAHOOLOGO = os.path.join(LOGOSDIR, 'wyahoologo.png')
YAHOOWEB = 'http://weather.yahoo.com/'
WOLRDWEATHERONLINE = os.path.join(LOGOSDIR, 'worldonlinelogo.png')
WOLRDWEATHERONLINEWEB = 'http://www.worldweatheronline.com/'
OPENWEATHERMAPLOGO = os.path.join(LOGOSDIR, 'wopenweathermaplogo.png')
OPENWEATHERMAPWEB = 'http://openweathermap.org/'
####
try:
    current_locale, encoding = locale.getdefaultlocale()
    if current_locale:
        LANG = current_locale.split("_")[0]
        language = gettext.translation(APP, LANGDIR, [current_locale])
        language.install()
        _ = language.gettext
    else:
        LANG = "en"
        raise Exception("No current locale")
except Exception as e:
    logger.error(e)
    _ = str
APPNAME = _(APPNAME)


def read_from_url(url):
    try:
        url = url.replace(' ', '%20')
        ans = requests.get(url, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.text
    except Exception as e:
        logger.error(e)
    return None


def read_json_from_url(url):
    try:
        url = url.replace(' ', '%20')
        ans = requests.get(url, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.json()
        else:
            raise Exception("Error accessing url: {} with {}".format(
                url, ans.status_code))
    except Exception as e:
        logger.error(e)
    return None


def internet_on():
    return check_connectivity()


if __name__ == '__main__':
    logger.info(internet_on())
